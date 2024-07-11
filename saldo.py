import requests
import concurrent.futures
from UserAgenter import UserAgent  # Importe a classe UserAgent

# Base URLs para consulta
base_urls = [
    "https://mempool.jednadvacet.org/api/address/",
    "https://mempool.blocktrainer.de/api/address/",
    "https://mempool.space/api/address/",
    "https://blockstream.info/api/address/",
    "https://btcscan.org/api/address/"
]

# Instância da classe UserAgent para gerar user agents aleatórios
agent = UserAgent()

def get_wallet_balance(url):
    try:
        # Gerar um user agent aleatório
        headers = {'User-Agent': agent.RandomAgent()}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança uma exceção para erros HTTP

        data = response.json()
        if "address" in data and "chain_stats" in data:
            address = data["address"]
            funded_txo_sum = data["chain_stats"].get("funded_txo_sum", 0)
            spent_txo_sum = data["chain_stats"].get("spent_txo_sum", 0)
            balance = (funded_txo_sum - spent_txo_sum) / 100_000_000  # Convertendo para BTC
            return address, balance
        else:
            print(f"Formato de resposta inesperado para URL: {url}")
            return None
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP ao consultar {url}: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de conexão ao consultar {url}: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout ao consultar {url}: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erro ao consultar {url}: {err}")
    except ValueError as ve:
        print(f"Erro ao processar resposta JSON para URL {url}: {ve}")
    except Exception as e:
        print(f"Erro inesperado ao consultar {url}: {e}")
    return None

def get_wallet_addresses():
    source = input("Deseja inserir os endereços manualmente (M) ou importar de um arquivo (A)? ").upper()
    
    if source == 'M':
        user_input = input("Insira os endereços das wallets (separados por vírgulas, espaços ou linhas):\n")
        addresses = [addr.strip() for addr in user_input.replace('\n', ',').replace(' ', ',').split(',') if addr.strip()]
    elif source == 'A':
        filename = input("Digite o nome do arquivo TXT contendo os endereços das wallets (um por linha):\n")
        try:
            with open(filename, 'r') as file:
                addresses = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado.")
            addresses = []
    else:
        print("Opção inválida. Por favor, escolha M para manual ou A para importar de arquivo.")
        addresses = []

    return addresses

def main():
    addresses = get_wallet_addresses()
    if not addresses:
        return  # Se não houver endereços válidos, sai do programa

    urls = [f"{base_urls[i % len(base_urls)]}{address}" for i, address in enumerate(addresses)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_url = {executor.submit(get_wallet_balance, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                if result:
                    address, balance = result
                    print(f"Address: {address}, Balance: {balance:.8f} BTC")
            except Exception as e:
                print(f"Erro ao processar a URL {url}: {e}")

if __name__ == "__main__":
    main()
