import base64
import json
from google.cloud import bigquery

# Inicializa o cliente do BigQuery para se comunicar com o banco de dados
client = bigquery.Client()
# Define o caminho completo da tabela onde os dados serão salvos
table_id = "seu-projeto-gcp.dados_sensores.sensor_data_table"

def process_sensor_data(event, context):
    """
    Esta função é o "gatilho" do nosso pipeline.
    Ela é ativada sempre que uma nova mensagem é publicada no Pub/Sub.

    Args:
        event (dict): Os dados da mensagem do Pub/Sub, incluindo o conteúdo.
        context (google.cloud.functions.Context): Metadados da função.
    """
    
    # Verifica se a mensagem tem dados. Se não, a função para.
    if 'data' not in event:
        print("Mensagem sem dados. Ignorando.")
        return
        
    # Decodifica a mensagem do Pub/Sub.
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    # Converte a mensagem decodificada (agora uma string JSON) para um objeto Python
    data = json.loads(pubsub_message)
    
    # Prepara os dados para inserção no BigQuery.
    # O BigQuery espera uma lista de dicionários.
    rows_to_insert = [data]
    
    # Insere os dados na tabela do BigQuery
    # A função insert_rows_json() é usada para inserir múltiplos registros de uma vez.
    errors = client.insert_rows_json(table_id, rows_to_insert)
    
    # Verifica se houve algum erro na inserção
    if errors:
        print(f"Erro ao inserir dados: {errors}")
    else:
        print(f"Dados inseridos com sucesso para a máquina {data['machine_id']}")

