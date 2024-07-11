import requests
import concurrent.futures

# Base URLs para consulta
base_urls = [
    "https://mempool.jednadvacet.org/api/address/",
    "https://mempool.blocktrainer.de/api/address/",
    "https://mempool.space/api/address/",
    "https://blockstream.info/api/address/",
    "https://btcscan.org/api/address/"
]

def get_wallet_balance(url):
    try:
        response = requests.get(url)
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
    except Exception as e:
        print(f"Erro ao consultar {url}: {e}")
        return None

def get_wallet_addresses():
    user_input = input("Insira os endereços das wallets (separados por vírgulas, espaços ou linhas):\n")
    addresses = [addr.strip() for addr in user_input.replace('\n', ',').replace(' ', ',').split(',') if addr.strip()]
    return addresses

def main():
    addresses = get_wallet_addresses()
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
