import re

def read_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) < 2:
            raise ValueError("O arquivo de credenciais não contém informações suficientes.")
        username = lines[0].strip().split(':')[-1].strip()
        password = lines[1].strip().split(':')[-1].strip()
        return username, password

def read_dados_boats(file_path):
    dados_boats = []  # Inicializa uma lista vazia para armazenar os dados dos barcos
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Verifique se a linha contém "NAME:" e "MMSI:" antes de processá-la
            if "NAME:" in line and "MMSI:" in line:
                name = line.split("NAME: ")[1].split(",")[0].strip()
                mmsi = line.split("MMSI: ")[1].strip()
                dados_boats.append({'name': name, 'mmsi': mmsi})  # Adiciona os dados à lista
    return dados_boats

def to_convert(dms_str):
    # Usando expressões regulares para extrair os valores numéricos e a direção
    match = re.match(r'(\d+)°(\d+\.\d+)′\s*([NSEW])', dms_str)
    if match:
        degrees = float(match.group(1))
        minutes = float(match.group(2))
        direction = match.group(3)
        
        # Convertendo os graus e minutos para decimal
        decimal_degrees = degrees + (minutes / 60.0)
        
        # Verificando a direção (N, S, E, W) e aplicando o sinal correto para latitude ou longitude
        if direction == 'S' or direction == 'W':
            decimal_degrees = -decimal_degrees
        
        return decimal_degrees
    else:
        return None