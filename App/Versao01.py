import requests
import json
from decimal import Decimal, ROUND_HALF_UP

class ConversorMoedas:
    def __init__(self, usar_api=True):
        """
        Inicializa o conversor de moedas.
        
        Args:
            usar_api (bool): Se True, usa API para taxas atualizadas. 
                            Se False, usa taxas pré-definidas.
        """
        self.usar_api = usar_api
        self.taxas_pre_definidas = {
            'USD': {'EUR': 0.85, 'BRL': 5.20, 'USD': 1.0},
            'EUR': {'USD': 1.18, 'BRL': 6.12, 'EUR': 1.0},
            'BRL': {'USD': 0.19, 'EUR': 0.16, 'BRL': 1.0}
        }
        self.moedas_suportadas = ['USD', 'EUR', 'BRL']
    
    def obter_taxa_api(self, moeda_origem, moeda_destino):
        """
        Obtém taxa de câmbio atual da API.
        
        Args:
            moeda_origem (str): Moeda de origem (ex: 'USD')
            moeda_destino (str): Moeda de destino (ex: 'BRL')
            
        Returns:
            float: Taxa de câmbio
        """
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{moeda_origem}"
            resposta = requests.get(url, timeout=5)
            
            if resposta.status_code == 200:
                dados = resposta.json()
                return dados['rates'].get(moeda_destino)
            else:
                print("❌ Erro na API. Usando taxas pré-definidas.")
                return self.taxas_pre_definidas[moeda_origem].get(moeda_destino)
                
        except (requests.RequestException, KeyError, json.JSONDecodeError):
            print("❌ Erro de conexão. Usando taxas pré-definidas.")
            return self.taxas_pre_definidas[moeda_origem].get(moeda_destino)
    
    def obter_taxa_conversao(self, moeda_origem, moeda_destino):
        """
        Obtém a taxa de conversão entre duas moedas.
        """
        if moeda_origem not in self.moedas_suportadas or moeda_destino not in self.moedas_suportadas:
            raise ValueError(f"❌ Moeda não suportada. Use: {', '.join(self.moedas_suportadas)}")
        
        if self.usar_api:
            print("🔗 Obtendo taxas atualizadas da API...")
            taxa = self.obter_taxa_api(moeda_origem, moeda_destino)
            if taxa is None:
                print("⚠️  API não retornou taxa. Usando valores pré-definidos.")
                taxa = self.taxas_pre_definidas[moeda_origem][moeda_destino]
        else:
            print("💾 Usando taxas pré-definidas...")
            taxa = self.taxas_pre_definidas[moeda_origem][moeda_destino]
        
        return taxa
    
    def converter(self, valor, moeda_origem, moeda_destino):
        """
        Converte um valor de uma moeda para outra.
        
        Args:
            valor (float): Valor a ser convertido
            moeda_origem (str): Moeda de origem
            moeda_destino (str): Moeda de destino
            
        Returns:
            Decimal: Valor convertido com 2 casas decimais
        """
        if valor < 0:
            raise ValueError("❌ O valor não pode ser negativo")
        
        taxa = self.obter_taxa_conversao(moeda_origem, moeda_destino)
        valor_convertido = Decimal(str(valor)) * Decimal(str(taxa))
        
        # Arredonda para 2 casas decimais com arredondamento correto
        valor_arredondado = valor_convertido.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        return valor_arredondado
    
    def listar_moedas_suportadas(self):
        """Retorna lista de moedas suportadas."""
        return self.moedas_suportadas.copy()

def mostrar_menu():
    """Mostra o menu de opções."""
    print("\n" + "="*50)
    print("🏦  CONVERSOR DE MOEDAS - MeuConvers$r")
    print("="*50)
    print("Moedas suportadas: USD, EUR, BRL")
    print("\nEscolha o modo de operação:")
    print("1. 💰 Usar taxas pré-definidas (rápido)")
    print("2. 🌐 Usar taxas atualizadas da API (preciso)")
    print("3. 🚪 Sair")
    print("="*50)

def interface_conversor(usar_api):
    """Interface do conversor."""
    conversor = ConversorMoedas(usar_api=usar_api)
    
    modo = "API 🌐" if usar_api else "PRÉ-DEFINIDAS 💰"
    print(f"\n💡 Modo selecionado: {modo}")
    
    while True:
        try:
            print(f"\n📊 Conversão ({modo})")
            print("Digite 'voltar' para retornar ao menu principal")
            
            # Entrada do usuário
            valor_input = input("\n💵 Digite o valor a converter: ").strip()
            
            if valor_input.lower() == 'voltar':
                break
            
            valor = float(valor_input)
            moeda_origem = input("🔄 Moeda de origem (USD/EUR/BRL): ").upper().strip()
            moeda_destino = input("🎯 Moeda de destino (USD/EUR/BRL): ").upper().strip()
            
            # Conversão
            resultado = conversor.converter(valor, moeda_origem, moeda_destino)
            taxa = conversor.obter_taxa_conversao(moeda_origem, moeda_destino)
            
            # Exibe resultado
            print(f"\n" + "✅" * 20)
            print(f"💱 RESULTADO DA CONVERSÃO:")
            print(f"📥 {valor:.2f} {moeda_origem} = 📤 {resultado} {moeda_destino}")
            print(f"💹 Taxa de câmbio: 1 {moeda_origem} = {taxa:.4f} {moeda_destino}")
            print(f"🔧 Modo: {modo}")
            print("✅" * 20)
            
            # Pergunta se quer fazer outra conversão
            continuar = input("\n🔄 Fazer outra conversão? (s/n): ").lower().strip()
            if continuar != 's':
                break
                
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

def main():
    """Função principal com menu interativo."""
    while True:
        mostrar_menu()
        
        try:
            opcao = input("\n📝 Escolha uma opção (1-3): ").strip()
            
            if opcao == '1':
                interface_conversor(usar_api=False)
            elif opcao == '2':
                interface_conversor(usar_api=True)
            elif opcao == '3':
                print("\n👋 Obrigado por usar o MeuConvers$r! Até logo!")
                break
            else:
                print("❌ Opção inválida! Escolha 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()