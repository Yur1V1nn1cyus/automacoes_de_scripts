import pandas as pd
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs_gerados.txt'),  # Salva logs em arquivo
        logging.StreamHandler()  # Exibe logs no console
    ]
)
logger = logging.getLogger(__name__)


def verif_up_mean_sal():
    """
    Lê um arquivo CSV, calcula a média dos salários e gera um novo arquivo CSV
    com os salários acima da média.
    """
    try:
        # Lê o arquivo CSV
        ler_csv = pd.read_csv('dados.csv')
        logger.info("Arquivo lido com sucesso.")
    except FileNotFoundError:
        logger.error("Arquivo 'dados.csv' não encontrado.")
        return
    except Exception as e:
        logger.error(f"Erro inesperado ao ler o arquivo: {e}")
        return

    try:
        # Calcula a média dos salários
        calculo_media_sal = ler_csv['Salário'].mean()
        logger.info(f"Média salarial calculada: {calculo_media_sal:.2f}")

        # Filtra salários acima da média
        df_acima_da_media = ler_csv[ler_csv['Salário'] > calculo_media_sal]

        # Salva o resultado em um novo arquivo CSV
        df_acima_da_media.to_csv('salarios_acima_da_media.csv', index=False)
        logger.info("Arquivo 'salarios_acima_da_media.csv' gerado com sucesso.")
    except KeyError:
        logger.error("Coluna 'Salário' não encontrada no arquivo CSV.")
    except Exception as e:
        logger.error(f"Erro inesperado ao processar os dados: {e}")


if __name__ == "__main__":
    verif_up_mean_sal()