# Prova 2 - M9

A atividade consiste numa fila capaz de receber dados sobre a qualidade do ar e salvá-los num banco de dados SQLite.

## Explicação

A solução consiste de três partes: configuração do dados, envio dos dados (producer) e recebimento dos dados (consumer).

### Configuração dos dados

Nós possuímos um arquivo json que contém as informações de id do sensor e de tipo de poluente que está sendo monitorado. Assim, facilitando a mudança para demais sensores e poluentes.

Os dados enviados estão localizados em um arquivo csv e o timestamp é recolhido no momento do envio.

### Producer

No producer, temos as etapas para definição do formato que o dado será enviado, como a definição da configuração presente no json em um classe, a leitura do dado no csv para a adição no nosso json de envio e a definição do nosso timestamp.

Após isso, temos a conexão com a nossa fila do Kafka e por meio de um producer é possível enviar os dados para a fila.

```
# Configurações do produtor
producer_config = {
    'bootstrap.servers': 'localhost:29092,localhost:39092',
    'client.id': 'python-producer'
}

# Criar produtor
producer = Producer(**producer_config)
```

```
def publicar(dado):
    message = dado
    producer.produce(topic, message.encode('utf-8'), callback=delivery_callback)
    print(f"Publicado")
```

### Consumer
O consumer recebe os dados e faz um POST numa rota de dados, assim, eles serão salvos num banco de dados SQLite .
```
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
        requests.post('http://localhost:5000/dados', json=json.loads(msg.value().decode('utf-8')))
        print(f'Recebido: {msg.value().decode("utf-8")}')
except KeyboardInterrupt:
    pass
finally:
    # Fechar consumidor
    consumer.close()
```

## Como rodar

Para colocar em funcionamento, é necessário estar com o docker desktop aberto, para então criar os containers:

```
docker-compose up -d
```

Após isso, instale o kafta:

```
pip install confluent-kafka
```

Inicie o consumer e o backend:

```
python3 consumer.py
python3 backend.py
```

Então, será possível enviar os dados com o producer:

```
python3 producer.py
```