import datetime
from functions.catch_data import data_capture
from functions.map_export import create_map
from functions.send_emails import attach_and_send
import os 


date = datetime.date.today()
date_format = date.strftime("%d_%m_%y")
list_of_pins = data_capture()

archive_name = f'templates/pin_map_{date_format}.html'

mapa = create_map(list_of_pins)
mapa.save(f'templates/pin_map_{date_format}.html')

attach_and_send(date_format)

if os.path.exists(archive_name):
    os.remove(archive_name)
    print(f'Arquivo {archive_name} foi removido com sucesso.')
else:
    print(f'O arquivo {archive_name} não existe.')