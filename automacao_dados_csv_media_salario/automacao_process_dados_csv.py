import pandas as pd
import logging
import os
import glob

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs_gerados.txt"),  # Salva logs em arquivo
        logging.StreamHandler()  # Exibe logs no console
    ]
)
logger = logging.getLogger(__name__)
log_path = os.path.abspath("logs_gerados.txt")
logging.FileHandler(log_path)
print(f"Log salvo em: {log_path}")

FORMATOS_SUPORTADOS = {
    "csv": pd.read_csv,
    "xlsx": pd.read_excel,
    "xls": pd.read_excel,
    "json": pd.read_json,
    "parquet": pd.read_parquet,
    "html": pd.read_html,   # Suporte para HTML
    "feather": pd.read_feather, # Formato Feather
}

def encontrar_arquivo(inicio_nome: str):
    arquivos = glob.glob(f"{inicio_nome}.*")
    for arquivo in arquivos:
        extensao = arquivo.split(".")[-1].lower()
        if extensao in FORMATOS_SUPORTADOS:
            return arquivo, extensao
    return None, None

def carregar_arquivo(nome_inicial: str):
    """Carrega automaticamente um arquivo suportado pelo Pandas."""
    nome_arquivo, extensao = encontrar_arquivo(nome_inicial)

    if not nome_arquivo:
        logger.error(f"Nenhum arquivo suportado encontrado com o início '{nome_inicial}'.")
        return None

    try:
        dtypes = {"Nome": "string","Idade": "int8","Salário": "float32",}

        df = FORMATOS_SUPORTADOS[extensao](nome_arquivo, dtype = dtypes)

        if df.empty:
            raise ValueError("O arquivo carregado está vazio.")

        # 🔹 Agora `df` existe! Podemos validar suas colunas e valores
        if len(df.columns) < 3:
            raise ValueError(f"Esperado ≥3 colunas, encontrado {len(df.columns)}: {list(df.columns)}")

        if "Salário" not in df.columns:
            raise KeyError("Coluna 'Salário' não encontrada no arquivo.")

        if (df["Salário"] < 0).any():
            raise ValueError("Salário não pode ser negativo.")

        for index, nome in df["Nome"].items():
            if pd.isna(nome) or nome == "":
                raise ValueError(f"O campo 'Nome' na linha {index} está nulo ou vazio.")    

        logger.info(f"Arquivo '{nome_arquivo}' carregado com sucesso.")
        return df

    except Exception as e:
        logger.error(f"Erro ao carregar '{nome_arquivo}': {e}")
        return None

def processar_salarios(df: pd.DataFrame):
    """Calcula a média salarial e salva os salários acima da média em um novo CSV."""
    try:
        media_salarial = df["Salário"].mean()
        logger.info(f"Média salarial calculada: {media_salarial:.2f}")

        df_acima_media = df[df["Salário"] > media_salarial]
        df_acima_media.to_csv("salarios_acima_da_media.csv", index=False)

        logger.info("Arquivo 'salarios_acima_da_media.csv' gerado com sucesso.")

    except Exception as e:
        logger.error(f"Erro inesperado ao processar os dados: {e}")

if __name__ == "__main__":
    df_dados = carregar_arquivo("dados")

    if df_dados is not None:
        processar_salarios(df_dados)

def gerar_relatorio (df: pd.DataFrame):
    try:
        dfresolve = pd.read_csv('salarios_acima_da_media.csv')
        all_func = dfresolve.shape[0]
        
        max_sal = dfresolve["Salário"].idxmax()
        nomeMax=dfresolve.loc[max_sal]

            # Criar o conteúdo do relatório
        relatorio = f"""
RELATÓRIO DE SALÁRIOS

Total de Funcionários: {all_func}

Funcionário com Maior Salário:
{nomeMax.to_string(index=True)}

------------------------------
"""
        
        with open("relatorio.txt", "w", encoding="utf-8") as file :
            file.write(relatorio)
        logger.info("Relatorio gerado com sucesso")
    except Exception as e :
        logger.error(f"Erro ao gerar relatorio: {e}")
gerar_relatorio(df_dados)
