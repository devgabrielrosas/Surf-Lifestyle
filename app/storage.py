import os

csv_path = os.path.join(os.path.dirname(__file__), 'inscricoes.csv')

def inicializar_csv():
    """cria o arquivo com cabeçalho se ainda não existir"""
    if not os.path.exists(csv_path):
        arq = open(csv_path, 'w', encoding='utf-8')
        arq.write("NOME,EMAIL\n")
        arq.close()

def escrever_csv(nome: str, email: str):
    """adiciona um novo registro ao CSV"""
    arq = open(csv_path, 'a', encoding='utf-8')
    arq.write(f"{nome},{email}\n")
    arq.close()

def ler_csv():
    """lê os registros do CSV como lista de dicionários"""
    dados = []
    if os.path.exists(csv_path):
        arq = open(csv_path, 'r', encoding='utf-8')
        linhas = arq.read().splitlines()[1:]  # ignora o cabeçalho
        arq.close()

        for linha in linhas:
            partes = linha.split(',')
            nome = partes[0]
            email = partes[1]
            dados.append({'nome': nome, 'email': email})

    return dados