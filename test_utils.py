import os
import shutil
import subprocess
import paramiko
def run_bash_command(command):
    """
    Выполняет указанную команду Bash и возвращает ее вывод.
    
    Args:
        command (str): Команда Bash, которую нужно выполнить.
    
    Returns:
        str: Вывод выполненной команды.
    """
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        return None

def clear_folder(folder_path):
    """
    Очищает указанную папку от всех файлов.
    
    Args:
        folder_path (str): Путь к папке, которую нужно очистить.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def replase_values_in_file(replace_values):
    # Функция для замены значений в файле
    def replace_values_in_file(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
            for key, value in replace_values.items():
                file_content = file_content.replace(key, value)

        new_file_path = os.path.join(
            'out', os.path.relpath(file_path, 'template_tmp'))
        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

        with open(new_file_path, 'w') as new_file:
            new_file.write(file_content)

    # Обход всех файлов в папке и ее подпапках
    for foldername, subfolders, filenames in os.walk('template_tmp'):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            # Можете изменить расширение файла по вашему усмотрению
            if file_path.endswith('.xml'):
                replace_values_in_file(file_path)

    for foldername, subfolders, filenames in os.walk('template_tmp'):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            # Можете изменить расширение файла по вашему усмотрению
            if file_path.endswith('.json'):
                replace_values_in_file(file_path)



def execute_ssh_commands_to_file(commands, vm_details, jhost_details, log_file_path):
    try:
        vm = paramiko.SSHClient()
        vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        vm.connect(vm_details['hostname'], username=vm_details['username'],
                   password=vm_details['password'])

        vm_transport = vm.get_transport()
        dest_addr = (jhost_details['hostname'], 22)
        local_addr = (vm_details['hostname'], 22)
        vm_channel = vm_transport.open_channel(
            "direct-tcpip", dest_addr, local_addr)

        jhost = paramiko.SSHClient()
        jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        jhost.connect(jhost_details['hostname'], username=jhost_details['username'],
                      password=jhost_details['password'], sock=vm_channel)

        with open(log_file_path, 'a') as log_file:
            for c in commands:
                stdin, stdout, stderr = jhost.exec_command(c, get_pty=True)
                while True:
                    line = stdout.readline()
                    if not line:
                        break
                    log_file.write(line)

        jhost.close()
        vm.close()
        return True
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False