# **Pipeline de Manutenção Preditiva em Tempo Real**

### **Análise de Dados de Sensores para Previsão de Falhas**

## **1\. Visão Geral**

Este projeto demonstra um pipeline de engenharia de dados em tempo real, focado na **manutenção preditiva de máquinas industriais**. O objetivo é simular a coleta de dados de sensores (temperatura, vibração, RPM) e, em seguida, processar e analisar esses dados em tempo real para detectar anomalias e prever potenciais falhas. A solução é completamente baseada em serviços **serverless** do Google Cloud Platform (GCP), garantindo escalabilidade, baixo custo e alta confiabilidade.

## **2\. Arquitetura da Solução**

O pipeline é modular e desacoplado, com cada componente servindo a uma função específica:

1. **Geração e Ingestão de Dados:** Um script Python simula os dados de telemetria e os envia continuamente para um tópico do Pub/Sub.
2. **Processamento e Análise:** Uma Cloud Function é acionada por cada mensagem do Pub/Sub. Ela decodifica os dados, aplica uma lógica para identificar anomalias e prepara os dados para o armazenamento.
3. **Armazenamento de Dados:** Os dados processados são inseridos em uma tabela no BigQuery, um data warehouse escalável e de alto desempenho.
4. **Visualização e Insights:** O Looker Studio se conecta ao BigQuery para criar um dashboard em tempo real, permitindo o monitoramento do estado das máquinas.

## **3\. Tecnologias Utilizadas**

- **Google Cloud Pub/Sub:** Serviço de mensageria assíncrona, usado para a ingestão de dados em tempo real.
- **Google Cloud Functions:** Plataforma de computação "sem servidor" que hospeda a lógica de processamento e análise.
- **Google BigQuery:** Data warehouse para armazenamento e consulta dos dados de telemetria.
- **Google Looker Studio:** Ferramenta de Business Intelligence (BI) para criar dashboards interativos.
- **Python:** Linguagem de programação utilizada para a simulação de dados e a lógica da Cloud Function.
- **Google Cloud CLI (gcloud):** Ferramenta de linha de comando usada para implantar a função e gerenciar o projeto.

## **4\. Como Executar o Projeto**

Siga os passos abaixo para replicar o pipeline em sua própria conta do GCP.

### **Passo 4.1. Configuração do Ambiente**

1. Tenha uma conta no Google Cloud Platform e um projeto ativo.
2. Habilite as APIs de **Cloud Pub/Sub**, **Cloud Functions**, e **BigQuery** no seu projeto.
3. Crie um tópico no Pub/Sub chamado sensor-data-topic.
4. Crie um dataset no BigQuery chamado dados_sensores e uma tabela chamada sensor_data_table com o seguinte esquema:
    - machine_id (STRING)
    - timestamp (TIMESTAMP)
    - temperatura (FLOAT)
    - vibracao (FLOAT)
    - rpm (FLOAT)
    - status (STRING)

### **Passo 4.2. Geração de Dados (Script Python)**

O script generate_data.py simula os dados dos sensores. Você pode executá-lo em um ambiente local ou no Google Colab.

### **Passo 4.3. Implantação da Cloud Function**

A Cloud Function é o coração do pipeline de processamento. Para implantá-la, use o Google Cloud Shell, um terminal pré-configurado no seu navegador.

1. Abra o Cloud Shell no console do GCP.
2. Crie os arquivos main.py e requirements.txt com os códigos fornecidos.
3. Execute o comando de implantação abaixo. 

gcloud functions deploy process_sensor_data_v3 --runtime python310 --trigger-topic sensor-data-topic --entry-point process_sensor_data --region us-central1

### **Passo 4.4. Visualização no Looker Studio**

1. Acesse o Looker Studio e crie um novo relatório.
2. Conecte-se à fonte de dados **BigQuery** e selecione a tabela sensor_data_table.
3. Crie um **gráfico de série temporal** para a temperatura ao longo do timestamp para visualizar os dados em tempo real.

## **5\. Desafios e Aprendizados**

- **Erros de Permissão (403):** Resolvidos ao atribuir os papéis corretos (como roles/editor) à conta do usuário, um passo fundamental para garantir a segurança e a capacidade de gerenciamento do projeto.
- **Erros de Esquema (no such field):** Falhas na inserção de dados no BigQuery, que exigiram uma validação rigorosa dos nomes dos campos e dos tipos de dados para garantir que o formato enviado pelo Pub/Sub fosse uma correspondência exata do esquema da tabela.
- **Implantação:** A confusão entre os serviços **Cloud Functions** e **Cloud Run** foi resolvida usando o **Cloud Shell** e o gcloud, demonstrando proficiência em ferramentas de linha de comando para contornar problemas na interface gráfica.