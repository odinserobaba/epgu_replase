import json
import uuid
import os
import logging
from datetime import datetime
import unittest

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JsonProcessor:
    def __init__(self, input_file, output_file):
        """
        Конструктор класса, инициализирует пути к входному и выходному файлам.
        """
        self.input_file = input_file
        self.output_file = output_file

    def load_json(self):
        """
        Загружает JSON файл. Если файл не найден или некорректный, выбрасывает исключение.
        """
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Файл {self.input_file} не найден.")
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logging.info(f"Файл {self.input_file} успешно загружен.")
            return data
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка при чтении JSON: {e}")
            raise

    def save_json(self, data):
        """
        Сохраняет JSON в компактной форме в указанный выходной файл. Заменяет файл, если он существует.
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, separators=(',', ':'))
            logging.info(f"Файл {self.output_file} успешно сохранен.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении файла: {e}")
            raise

    def replace_fields(self, data):
        """
        Заменяет указанные поля в JSON, генерируя UUID для некоторых полей и задавая фиксированные значения для других.
        """
        current_date = "2024-09-04"
        current_timestamp = "2024-09-04T10:31:20.508+0300"

        try:
            data["id"] = str(uuid.uuid4())
            data["requestId"] = str(uuid.uuid4())
            data["xsltId"] = 10
            data["responseId"] = str(uuid.uuid4())
            data["messageId"] = str(uuid.uuid4())
            data["orderID"] = "3501540284"
            data["statementDate"] = current_date
            data["issueDate"] = current_date
            data["date"] = current_date
            data["requestTimestamp"] = current_timestamp
            data["updateTimestamp"] = current_timestamp
            data["fullName"] = "CenterInformVR"
            data["shortName"] = "CenterInformVR"

            logging.info("Поля успешно заменены.")
        except KeyError as e:
            logging.error(f"Ошибка при замене полей: {e}")
            raise

        return data

    def process(self):
        """
        Основной метод для загрузки, обработки и сохранения JSON файла.
        """
        try:
            # Шаг 1: Загрузка JSON
            data = self.load_json()

            # Шаг 2: Замена полей
            updated_data = self.replace_fields(data)

            # Шаг 3: Сохранение JSON
            self.save_json(updated_data)

            return updated_data
        except Exception as e:
            logging.error(f"Ошибка в процессе обработки: {e}")
            raise


# Unit тесты
class TestJsonProcessor(unittest.TestCase):

    def setUp(self):
        """
        Метод setUp выполняется перед каждым тестом. Создает временные файлы для тестирования.
        """
        # Входные данные для теста
        self.input_data = {
            "id": "",
            "requestId": "",
            "xsltId": 0,
            "responseId": "",
            "messageId": "",
            "orderID": "",
            "statementDate": "",
            "issueDate": "",
            "date": "",
            "requestTimestamp": "",
            "updateTimestamp": "",
            "fullName": "",
            "shortName": ""
        }

        self.input_file = 'test_input.json'
        self.output_file = 'test_output.json'

        # Записываем тестовый входной файл
        with open(self.input_file, 'w', encoding='utf-8') as file:
            json.dump(self.input_data, file)

        self.processor = JsonProcessor(self.input_file, self.output_file)

    def test_replace_fields(self):
        """
        Тестируем, что поля корректно заменяются и что UUID генерируются для нужных полей.
        """
        updated_data = self.processor.replace_fields(self.input_data.copy())

        self.assertTrue(uuid.UUID(updated_data["id"]))
        self.assertTrue(uuid.UUID(updated_data["requestId"]))
        self.assertEqual(updated_data["xsltId"], 10)
        self.assertTrue(uuid.UUID(updated_data["responseId"]))
        self.assertTrue(uuid.UUID(updated_data["messageId"]))
        self.assertEqual(updated_data["orderID"], "3501540284")
        self.assertEqual(updated_data["statementDate"], "2024-09-04")
        self.assertEqual(updated_data["issueDate"], "2024-09-04")
        self.assertEqual(updated_data["date"], "2024-09-04")
        self.assertEqual(updated_data["requestTimestamp"], "2024-09-04T10:31:20.508+0300")
        self.assertEqual(updated_data["updateTimestamp"], "2024-09-04T10:31:20.508+0300")
        self.assertEqual(updated_data["fullName"], "CenterInformVR")
        self.assertEqual(updated_data["shortName"], "CenterInformVR")

    def test_process(self):
        """
        Тестируем полный процесс обработки JSON файла: загрузку, замену полей и сохранение.
        """
        updated_data = self.processor.process()

        # Проверяем, что файл был сохранён и содержимое совпадает с обработанными данными
        with open(self.output_file, 'r', encoding='utf-8') as file:
            saved_data = json.load(file)

        self.assertEqual(updated_data, saved_data)

    def tearDown(self):
        """
        Метод tearDown выполняется после каждого теста для очистки.
        Удаляет временные файлы, созданные для тестов.
        """
        os.remove(self.input_file)
        os.remove(self.output_file)


if __name__ == '__main__':
    unittest.main()
