import csv
import datetime
import json
from confluent_kafka import Producer, Consumer, KafkaError

class Configuracao:
    def __init__(self, idSensor, tipoPoluente):
        self.idSensor = idSensor
        self.tipoPoluente = tipoPoluente

# Configurações do produtor
producer_config = {
    'bootstrap.servers': 'localhost:29092,localhost:39092',
    'client.id': 'python-producer'
}

# Criar produtor
producer = Producer(**producer_config)

# Função de callback para confirmação de entrega
def delivery_callback(err, msg):
    if err:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def criar_json(dado):
    formatacao_json = {
        "idSensor": configuracao.idSensor,
        "timestamp": datetime.datetime.now().isoformat(),
        "tipoPoluente": configuracao.tipoPoluente,
        "nivel": dado
    }

    dado = json.dumps(formatacao_json)

    return dado

def leitura_csv():
    with open('dados.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            dado = criar_json(row)
            publicar(dado)
    

def configurar():
    with open('config.json', 'r') as arquivo:
        leitura = json.load(arquivo)
        return Configuracao(leitura['idSensor'], leitura['tipoPoluente'])

topic = 'test_topic'

def publicar(dado):
    message = dado
    producer.produce(topic, message.encode('utf-8'), callback=delivery_callback)
    print(f"Publicado")

configuracao = configurar()
leitura_csv()

# Aguardar a entrega de todas as mensagens
producer.flush()