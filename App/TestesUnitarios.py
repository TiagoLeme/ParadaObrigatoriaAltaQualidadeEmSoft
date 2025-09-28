import unittest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from conversor_moedas import ConversorMoedas

class TestConversorMoedas(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.conversor_api = ConversorMoedas(usar_api=True)
        self.conversor_pre_definido = ConversorMoedas(usar_api=False)
    
    def test_listar_moedas_suportadas(self):
        """Testa se retorna lista correta de moedas suportadas."""
        moedas = self.conversor_api.listar_moedas_suportadas()
        self.assertEqual(moedas, ['USD', 'EUR', 'BRL'])
    
    def test_conversao_usd_para_eur_pre_definida(self):
        """Testa conversão USD para EUR com taxas pré-definidas."""
        resultado = self.conversor_pre_definido.converter(100, 'USD', 'EUR')
        self.assertEqual(resultado, Decimal('85.00'))
    
    def test_conversao_eur_para_brl_pre_definida(self):
        """Testa conversão EUR para BRL com taxas pré-definidas."""
        resultado = self.conversor_pre_definido.converter(50, 'EUR', 'BRL')
        self.assertEqual(resultado, Decimal('306.00'))
    
    def test_conversao_brl_para_usd_pre_definida(self):
        """Testa conversão BRL para USD com taxas pré-definidas."""
        resultado = self.conversor_pre_definido.converter(100, 'BRL', 'USD')
        self.assertEqual(resultado, Decimal('19.00'))
    
    def test_conversao_mesma_moeda(self):
        """Testa conversão quando origem e destino são a mesma moeda."""
        resultado = self.conversor_pre_definido.converter(100, 'USD', 'USD')
        self.assertEqual(resultado, Decimal('100.00'))
    
    def test_arredondamento_correto(self):
        """Testa se o arredondamento está funcionando corretamente."""
        # Teste com valor que precisa de arredondamento
        resultado = self.conversor_pre_definido.converter(1.555, 'USD', 'USD')
        self.assertEqual(resultado, Decimal('1.56'))
        
        resultado = self.conversor_pre_definido.converter(1.554, 'USD', 'USD')
        self.assertEqual(resultado, Decimal('1.55'))
    
    def test_precisao_duas_casas_decimais(self):
        """Testa se o resultado sempre tem 2 casas decimais."""
        resultados = [
            self.conversor_pre_definido.converter(10, 'USD', 'EUR'),
            self.conversor_pre_definido.converter(7.5, 'EUR', 'BRL'),
            self.conversor_pre_definido.converter(3.14159, 'BRL', 'USD')
        ]
        
        for resultado in resultados:
            # Converte para string e verifica casas decimais
            partes = str(resultado).split('.')
            self.assertEqual(len(partes[1]), 2)
    
    def test_valor_negativo(self):
        """Testa se rejeita valores negativos."""
        with self.assertRaises(ValueError):
            self.conversor_pre_definido.converter(-100, 'USD', 'EUR')
    
    def test_moeda_nao_suportada(self):
        """Testa se rejeita moedas não suportadas."""
        with self.assertRaises(ValueError):
            self.conversor_pre_definido.converter(100, 'JPY', 'USD')
        
        with self.assertRaises(ValueError):
            self.conversor_pre_definido.converter(100, 'USD', 'JPY')
    
    @patch('conversor_moedas.requests.get')
    def test_conversao_com_api_sucesso(self, mock_get):
        """Testa conversão usando API com sucesso."""
        # Mock da resposta da API
        mock_resposta = MagicMock()
        mock_resposta.status_code = 200
        mock_resposta.json.return_value = {
            'rates': {
                'BRL': 5.25,
                'EUR': 0.92
            }
        }
        mock_get.return_value = mock_resposta
        
        resultado = self.conversor_api.converter(100, 'USD', 'BRL')
        self.assertEqual(resultado, Decimal('525.00'))
    
    @patch('conversor_moedas.requests.get')
    def test_conversao_com_api_falha(self, mock_get):
        """Testa conversão quando API falha (deve usar taxas pré-definidas)."""
        # Mock de falha na API
        mock_get.side_effect = Exception("Erro de conexão")
        
        # Deve usar taxas pré-definidas como fallback
        resultado = self.conversor_api.converter(100, 'USD', 'BRL')
        self.assertEqual(resultado, Decimal('520.00'))
    
    def test_taxas_pre_definidas_consistencia(self):
        """Testa se as taxas pré-definidas são consistentes."""
        taxas = self.conversor_pre_definido.taxas_pre_definidas
        
        # Verifica se todas as moedas têm taxa para si mesmas = 1.0
        for moeda in self.conversor_pre_definido.moedas_suportadas:
            self.assertEqual(taxas[moeda][moeda], 1.0)
    
    def test_conversao_valor_zero(self):
        """Testa conversão com valor zero."""
        resultado = self.conversor_pre_definido.converter(0, 'USD', 'EUR')
        self.assertEqual(resultado, Decimal('0.00'))

if __name__ == '__main__':
    unittest.main()