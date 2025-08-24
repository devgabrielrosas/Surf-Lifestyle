import os


# inscrições.csv :

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


# agendamento.csv :
def caminho_pasta_dados(app_root=None):
    """Retorna a pasta data dentro do pacote app. Se app_root for None, tenta usar __file__."""
    if app_root:
        raiz = app_root
    else:
        raiz = os.path.dirname(os.path.abspath(__file__))  # será app/
    pasta = os.path.join(raiz, "data")
    if not os.path.exists(pasta):
        try:
            os.makedirs(pasta, exist_ok=True)
        except Exception:
            # se falhar, elevar exceção para quem chamou tratar
            raise
    return pasta

def caminho_arquivo_csv(app_root=None):
    """Caminho completo do CSV (app/data/agendamento.csv)."""
    pasta = caminho_pasta_dados(app_root)
    return os.path.join(pasta, "agendamento.csv")

def garantir_csv_existe(app_root=None):
    """Cria o CSV com cabeçalho se não existir."""
    caminho = caminho_arquivo_csv(app_root)
    if not os.path.exists(caminho):
        f = open(caminho, "w", encoding="utf-8")
        f.write("nome,telefone,data,hora,criado_em\n")
        f.close()
    return caminho

def ler_agendamentos(app_root=None):
    """Lê e retorna lista de dicionários (sem usar csv lib)."""
    caminho = caminho_arquivo_csv(app_root)
    agendamentos = []
    if not os.path.exists(caminho):
        return agendamentos
    f = open(caminho, "r", encoding="utf-8")
    linhas = f.read().splitlines()
    f.close()
    for linha in linhas[1:]:
        if not linha.strip():
            continue
        partes = linha.split(",")
        nome = partes[0].strip() if len(partes) > 0 else ""
        telefone = partes[1].strip() if len(partes) > 1 else ""
        data_field = partes[2].strip() if len(partes) > 2 else ""
        hora_field = partes[3].strip() if len(partes) > 3 else ""
        criado_em = partes[4].strip() if len(partes) > 4 else ""
        agendamentos.append({
            "nome": nome,
            "telefone": telefone,
            "data": data_field,
            "hora": hora_field,
            "criado_em": criado_em
        })
    return agendamentos

def salvar_agendamento(registro: dict, app_root=None):
    """
    Anexa registro ao CSV. Registro deve conter nome, telefone, data, hora, criado_em.
    Substitui vírgulas básicas para evitar quebra de colunas.
    Retorna caminho do arquivo salvo para verificação.
    """
    caminho = caminho_arquivo_csv(app_root)
    # sanitização simples
    nome = (registro.get("nome") or "").replace(",", " ")
    telefone = (registro.get("telefone") or "").replace(",", " ")
    data_field = (registro.get("data") or "").replace(",", " ")
    hora_field = (registro.get("hora") or "").replace(",", " ")
    criado_em = (registro.get("criado_em") or "").replace(",", " ")

    # cria cabeçalho caso não exista
    if not os.path.exists(caminho):
        fhead = open(caminho, "w", encoding="utf-8")
        fhead.write("nome,telefone,data,hora,criado_em\n")
        fhead.close()

    f = open(caminho, "a", encoding="utf-8")
    f.write(f"{nome},{telefone},{data_field},{hora_field},{criado_em}\n")
    f.close()
    return caminho