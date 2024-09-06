import uuid
from typing import Tuple, List, Dict, Union
import logging
import pprint
import re

# Настройка логирования
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_LEVEL = logging.INFO
LOG_FILE = 'log.log'
LOG_MODE = 'a'

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL,
                    filename=LOG_FILE, filemode=LOG_MODE)


def replace_match(text: str = '', pattern: str = '', replace_value: str = ''):
    try:
        match = re.search(pattern, text)
        if match:
            return_text = text.replace(match.group(1), str(replace_value))
        else:
            logging.info(f"По паттерну: {pattern} не найдено в {text}")
            return_text = text
    except re.error as e:
        logging.error(f"replace_match: Ошибка в шаблоне {pattern} - {e}")
    except Exception as e:
        logging.error(f"replace_match: Неизвестная ошибка - {e}")

    return return_text


def parse_command(command: Dict[str, list], text: str) -> str:
    pprint.pprint(type(command))
    if command:
        try:
            for k, v in command.items():
                if re.search(v[2], text):
                    if v[0] == "uuid4":
                        try:
                            uuid4 = str(uuid.uuid4())
                            logging.info(f"Меняем в {text} на uuid4 {uuid4}")
                            out_text = replace_match(text, v[2], uuid4)
                            return out_text
                        except Exception as e:
                            logging.error(
                                f"Ошибка при uuid4: {command} {text} v[2]: {v[2]} uuid4: {uuid4} {e}")

                    elif v[1] == "replace":
                        try:
                            logging.info(f"Меняем в {text} на {v[0]}")
                            out_text = replace_match(text, v[2], v[0])
                            return out_text
                        except Exception as e:
                            logging.error(
                                f"Ошибка при replace: {command} {text} v[2]: {v[2]}  {e}")

        except Exception as e:
            logging.error(
                f"Ошибка при чтении или замене ключа: {command} {text} - {e}")
        finally:
            logging.info(f"parse_command finally: {command} {text}")

    # Если замена не производилась, возвращаем исходный текст
    return text


text = '"id": "5583b1cb-612a-43f1-8011-7f07d1cf3238",'
command_dict: Dict[str, list] = {
    'id': ["uuid4", "any", '"id": "([^"]+)"']
}
print(parse_command(command_dict, text))
