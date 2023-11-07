def read_credentials_from_file(file_path):
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

