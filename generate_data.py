#Instala bibliotecas
!pip install google-cloud-pubsub
!pip install google-cloud-bigquery
!pip install google-auth
!pip install --upgrade google-api-core
!pip install google-cloud-core

#Autenticação
from google.colab import auth

auth.authenticate_user()


#Implementa loop para gerar dados
import json
import time
import random
import datetime
from google.cloud import pubsub_v1

project_id = 'manutencao-preditiva-gcp'
topic_id = 'sensor-data-topic'

# Criação do cliente de publicação
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def generate_sensor_data(machine_id):
    """
    Função para gerar dados simulados de um sensor.
    Adiciona um pouco de aleatoriedade e anomalias para simular um cenário real.
    """
    timestamp = datetime.datetime.now().isoformat()
    # Adiciona anomalia na temperatura com 10% de chance
    temperatura = round(random.uniform(50, 80) + (random.uniform(10, 20) if random.random() > 0.9 else 0), 2)
    # Adiciona anomalia na vibração com 5% de chance
    vibracao = round(random.uniform(2.0, 5.0) + (random.uniform(3, 5) if random.random() > 0.95 else 0), 2)
    rpm = round(random.uniform(1000, 1500), 2)
    
    # Define o status baseado nas anomalias
    status = "anomalia" if temperatura > 90 or vibracao > 7.5 else "normal"
    
    data = {
        "machine_id": machine_id,
        "timestamp": timestamp,
        "temperatura": temperatura,
        "vibracao": vibracao,
        "rpm": rpm,
        "status": status
    }
    return data

# Loop para gerar e enviar os dados
# Execute esta célula e ela ficará rodando até que você a interrompa manualmente (botão 'stop')
print(f"Iniciando a geração e envio de dados para o tópico: {topic_path}")
try:
    while True:
        for machine_id in ["maquina-01", "maquina-02", "maquina-03"]:
            sensor_data = generate_sensor_data(machine_id)
            data_json = json.dumps(sensor_data).encode("utf-8")
            
            # Publica a mensagem no tópico do Pub/Sub
            future = publisher.publish(topic_path, data_json)
            print(f"Dados enviados para {machine_id}. ID da mensagem: {future.result()}")
        
        time.sleep(1) # Intervalo de 1 segundo entre cada envio
except Exception as e:
    print(f"Ocorreu um erro: {e}")
