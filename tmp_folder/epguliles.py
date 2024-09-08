import os
import re
import json
import uuid
import logging
from glob import glob

# Настройка логирования
log_file = 'process.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler(log_file), logging.StreamHandler()])

# Функция для генерации случайных UUID
def generate_uuid():
    return str(uuid.uuid4())

# Функция для замены содержимого в строке по заданному шаблону
def replace_content(content, rules):
    for pattern, command, value in rules:
        if command == "uuid":
            replacement = generate_uuid()
        elif command == "any":
            replacement = value
        else:
            continue
        content = re.sub(pattern, f'"{replacement}"', content)
    return content

# Функция для обработки файла
def process_file(filename, rules, output_folder):
    logging.info(f'Processing file: {filename}')
    try:
        # Создание папки для выходных данных, если ее нет
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            logging.info(f'Output folder created: {output_folder}')
        
        # Чтение исходного файла
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        # Замена содержимого
        updated_content = replace_content(content, rules)

        # Создание нового имени файла с добавлением суффикса '_new'
        base_name = os.path.basename(filename)
        new_filename = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_new{os.path.splitext(base_name)[1]}")

        # Запись обновленного содержимого в новый файл
        with open(new_filename, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        logging.info(f'File saved as: {new_filename}')
    except Exception as e:
        logging.error(f'Error processing file {filename}: {e}')

# Функция для создания компактного JSON
def create_compact_json(data, output_folder):
    json_filename = os.path.join(output_folder, "result.json")
    try:
        with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, separators=(',', ':'))
        logging.info(f'Compact JSON saved as: {json_filename}')
    except Exception as e:
        logging.error(f'Error saving JSON file: {e}')

# Функция для чтения параметров из файла конфигурации
def read_parameters(file_path):
    rules = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(' ')
                    if len(parts) >= 3:
                        filename_pattern = parts[0]
                        pattern = parts[1].strip('"')
                        command = parts[2]
                        value = parts[3] if len(parts) > 3 else ""
                        rules.append((pattern, command, value))
        logging.info(f'Read {len(rules)} rules from configuration file.')
    except Exception as e:
        logging.error(f'Error reading parameters file {file_path}: {e}')
    return rules

# Основная часть программы
def main(params_file, output_base_folder):
    # Чтение параметров из файла конфигурации
    rules = read_parameters(params_file)

    if not rules:
        logging.error('No rules found or error reading the parameters file.')
        return

    # Обработка каждого файла в соответствии с параметрами
    for rule in rules:
        filename_pattern, _, _ = rule
        for filename in glob(filename_pattern):
            logging.info(f'Processing file pattern: {filename_pattern}')
            output_folder = os.path.join(output_base_folder, os.path.basename(filename))
            process_file(filename, rules, output_folder)

            # Создание компактного JSON с результатами
            example_data = {
                "original_file": filename,
                "rules": rules
            }
            create_compact_json(example_data, output_folder)
# Пример использования
if __name__ == "__main__":
    params_folder = "/media/nuanred/2f0ac1ec-7485-4ab7-aac0-7be94188d9a6/mnt/EPGU/parameters_folder/test.st"
    input_folder = "/media/nuanred/2f0ac1ec-7485-4ab7-aac0-7be94188d9a6/mnt/EPGU/input_files_folder/"
    output_base_folder = "/media/nuanred/2f0ac1ec-7485-4ab7-aac0-7be94188d9a6/mnt/EPGU/output_folders/"
    
    # Запуск основной программы
    main(params_folder,  output_base_folder)
