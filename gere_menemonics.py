from mnemonic import Mnemonic

# Função para gerar mnemônicos
def generate_mnemonics():
    # Linguagens disponíveis na biblioteca mnemonic
    languages = ["english", "japanese", "korean", "spanish", "chinese_simplified", "chinese_traditional", "french", "italian"]

    # Listas para armazenar mnemônicos de cada tipo
    mnemonics_12 = []
    mnemonics_18 = []
    mnemonics_24 = []

    for language in languages:
        mnemo = Mnemonic(language)
        
        # Gerar mnemônicos de 12, 18 e 24 palavras
        mnemonics_12.append(mnemo.generate(strength=128))
        mnemonics_18.append(mnemo.generate(strength=192))
        mnemonics_24.append(mnemo.generate(strength=256))

    # Função para exibir mnemônicos
    def print_mnemonics(mnemonics, label):
        print(f"\nMnemônicos de {label} palavras:")
        for mnemonic in mnemonics:
            print(mnemonic)

    # Exibir mnemônicos de 12, 18 e 24 palavras
    print_mnemonics(mnemonics_12, "12")
    print_mnemonics(mnemonics_18, "18")
    print_mnemonics(mnemonics_24, "24")

# Executar a função para gerar e exibir os mnemônicos
if __name__ == "__main__":
    generate_mnemonics()
