from flask import Flask, render_template
from catch_data import data_capture

app = Flask(__name__)

#for data in list_of_pins:
#    print(data)

@app.route('/')
def map():
    list_of_pins = data_capture()
    print(list_of_pins)  # Check the data in console
    return render_template('map.html', dados_exportar=list_of_pins)

if __name__ == '__main__':
    app.run(debug=True)