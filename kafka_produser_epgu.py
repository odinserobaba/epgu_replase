import os
import json
from kafka import KafkaProducer

kafka_broker = 'test-kafka1.fsrar.ru:9092'
topic_name = 'test-smev-leveler-in-request'

producer = KafkaProducer(
    bootstrap_servers=kafka_broker,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def send_json_files_to_kafka(folder_path):

    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f)) and f.endswith(f'create_new.json')]

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        producer.send(topic_name, json_data)
        print(f'Successfully sent {file_name} to Kafka topic {topic_name}')

    producer.flush()


folder_path = '/home/ldapusers/Serobaba/license/jsonsepgu'


send_json_files_to_kafka(folder_path)
