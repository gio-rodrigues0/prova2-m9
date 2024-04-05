from confluent_kafka import Producer, Consumer, KafkaError
import requests
import json

# Configurações do consumidor
consumer_config = {
    'bootstrap.servers': 'localhost:29092,localhost:39092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
}

topic = 'test_topic'

# Criar consumidor
consumer = Consumer(**consumer_config)

# Assinar tópico
consumer.subscribe([topic])

# Consumir mensagens
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        dict = json.loads(msg.value().decode('utf-8'))
        requests.post('http://localhost:5000/dados', json=json.loads(msg.value().decode('utf-8')))
        print(f"Tipo de sensor: {dict['idSensor']} \n Tipo de poluente: {dict['tipoPoluente']} \n Nível de poluente: {dict['nivel']} \n Timestamp: {dict['timestamp']}")
except KeyboardInterrupt:
    pass
finally:
    # Fechar consumidor
    consumer.close()