from mnemonic import Mnemonic
import itertools
import multiprocessing
from queue import SimpleQueue
import time

# Função para calcular o número total de combinações possíveis
def calculate_total_combinations(wordlist, num_words):
    return len(wordlist) * (len(wordlist) ** (num_words - 1))

# Função para gerar mnemônicos com uma palavra inicial específica
def generate_mnemonic_with_initial(queue, language, initial_word, num_words):
    mnemo = Mnemonic(language)
    wordlist = mnemo.wordlist
    
    for comb in itertools.product(wordlist, repeat=num_words - 1):
        mnemonic = [initial_word] + list(comb)
        queue.put(' '.join(mnemonic))

# Função para exibir mnemônicos
def print_mnemonics(queue, total_combinations, label):
    print(f"\nMnemônicos de {label} palavras:")
    count = 0
    while count < total_combinations:
        mnemonic = queue.get()
        print(mnemonic)
        count += 1

# Função para gerar mnemônicos com todas as palavras iniciais
def generate_mnemonics(language):
    mnemo = Mnemonic(language)
    wordlist = mnemo.wordlist

    for num_words in [12, 18, 24]:
        total_combinations = calculate_total_combinations(wordlist, num_words)
        queue = SimpleQueue()

        # Multiprocessing pool
        processes = []
        for word in wordlist:
            p = multiprocessing.Process(target=generate_mnemonic_with_initial, args=(queue, language, word, num_words))
            processes.append(p)
            p.start()

        # Start a process to print mnemonics
        printer = multiprocessing.Process(target=print_mnemonics, args=(queue, total_combinations, str(num_words)))
        printer.start()

        for p in processes:
            p.join()
        
        printer.join()

# Executar a função para gerar e exibir os mnemônicos
if __name__ == "__main__":
    start_time = time.time()
    languages = ["english", "japanese", "korean", "spanish", "chinese_simplified", "chinese_traditional", "french", "italian"]
    for language in languages:
        generate_mnemonics(language)
    end_time = time.time()
    print(f"Tempo total: {end_time - start_time} segundos")
