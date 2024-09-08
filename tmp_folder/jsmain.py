import re
import glob
import logging
import uuid
import random
import json

# Настройка логирования
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_LEVEL = logging.INFO
LOG_FILE = 'log.log'
LOG_MODE = 'a'

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL, filename=LOG_FILE, filemode=LOG_MODE)

def make_compact_json(json_data):
    return json.dumps(json_data, separators=(',', ':'))

def process_file(filename, rules):
    logging.info(f"Начало обработки файла: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
    except FileNotFoundError:
        logging.error(f"Файл {filename} не найден.")
        return

    # Применение правил
    if rules:
        logging.info(f"Применение правил к тексту: {text}")
        text = apply_rules(text, rules)
        logging.info(f"Текст после применения правил: {text}")

    # Генерация нового имени файла
    base, ext = filename.rsplit('.', 1)
    new_filename = f"{base}-new.json"

    # Запись измененного текста в новый файл
    try:
        with open(new_filename, 'w', encoding='utf-8') as new_file:
            new_file.write(make_compact_json(json.loads(text)))
        logging.info(f"Текст успешно записан в файл: {new_filename}")
    except Exception as e:
        logging.error(f"Ошибка записи текста в файл {new_filename}: {e}")

def apply_rules(text, rules):
    json_data = json.loads(text)
    for pattern, command, key_match, value_match in rules:
        # Используем более точные регулярные выражения для ключей
        pattern = f'"{key_match}":\s*"([^"]+)"'
        if command == 'uuid':
            new_value = str(uuid.uuid4())
            json_data = replace_value(json_data, key_match, new_value)
            logging.info(f"Замена {key_match}: на {new_value}")
        elif command == 'random':
            min_val, max_val = map(int, value_match.split('-'))
            new_value = str(random.randint(min_val, max_val))
            json_data = replace_value(json_data, key_match, new_value)
            logging.info(f"Замена {key_match}: на {new_value}")
        elif command == 'calc':
            result = str(eval(value_match))
            json_data = replace_value(json_data, key_match, result)
            logging.info(f"Замена {key_match}: на {result}")
        elif command == 'any':
            json_data = replace_value(json_data, key_match, value_match)
            logging.info(f"Замена {key_match}: на {value_match}")
    return json.dumps(json_data)

def replace_value(data, key, new_value):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                data[k] = new_value
            elif isinstance(v, (dict, list)):
                data[k] = replace_value(v, key, new_value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (dict, list)):
                data[i] = replace_value(item, key, new_value)
    return data

def parse_rules(rules_filename):
    logging.info(f"Начало парсинга правил из файла: {rules_filename}")
    rules_dict = {}

    try:
        with open(rules_filename, 'r') as file:
            current_filename = None
            rules = []

            for line in file:
                line = line.strip()
                if line.startswith('filename = '):
                    if current_filename:
                        rules_dict[current_filename] = rules
                        rules = []
                    current_filename = line.split(' = ')[1].strip("'")
                elif line:
                    parts = line.split(' ', 3)
                    key_pattern, _, command, value_match = parts
                    key_pattern = key_pattern + ' ' + _
                    rules.append((key_pattern, command, key_pattern, value_match.strip('"')))
            if current_filename:
                rules_dict[current_filename] = rules
    except FileNotFoundError:
        logging.error(f"Файл {rules_filename} не найден.")
        return {}

    logging.info(f"Завершение парсинга правил из файла: {rules_filename}")
    return rules_dict

def main(rules_filename='/media/nuanred/2f0ac1ec-7485-4ab7-aac0-7be94188d9a6/mnt/EPGU/repo/scripts/epgu_test.nr'):
    rules_dict = parse_rules(rules_filename)
    print(rules_filename)
    for filename_pattern, rules in rules_dict.items():
        for filename in glob.glob(filename_pattern):
            if filename:  # Проверяем, что файл найден
                print(filename)
                process_file(filename, rules)
            else:
                logging.warning(f"Файл по шаблону {filename_pattern} не найден.")

if __name__ == "__main__":
    logging.info("Начало выполнения скрипта")
    main('/media/nuanred/2f0ac1ec-7485-4ab7-aac0-7be94188d9a6/mnt/EPGU/repo/scripts/epgu_test.nr')
    logging.info("Завершение выполнения скрипта")