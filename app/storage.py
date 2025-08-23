import os

# garante que o arquivo fique em app/data/
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

csv_path = os.path.join(data_dir, "inscricoes.csv")


def inicializar_csv():
    """Cria o arquivo com cabeçalho se ainda não existir"""
    if not os.path.exists(csv_path):
        arq = open(csv_path, "w", encoding="utf-8")
        arq.write("nome,email\n")
        arq.close()


def escrever_csv(nome: str, email: str):
    """Adiciona um novo registro ao CSV"""
    # Sanitiza vírgulas para evitar bagunça no formato CSV
    nome = nome.replace(",", " ")
    email = email.replace(",", " ")

    arq = open(csv_path, "a", encoding="utf-8")
    arq.write(f"{nome},{email}\n")
    arq.close()


def ler_csv():
    """Lê os registros do CSV como lista de dicionários"""
    dados = []
    if os.path.exists(csv_path):
        arq = open(csv_path, "r", encoding="utf-8")
        linhas = arq.read().splitlines()
        arq.close()

        # ignora cabeçalho
        for linha in linhas[1:]:
            partes = linha.split(",")
            if len(partes) >= 2:  # garante que há nome e email
                nome = partes[0].strip()
                email = partes[1].strip()
                dados.append({"nome": nome, "email": email})

    return dados