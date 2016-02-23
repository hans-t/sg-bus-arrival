from flask import Flask
from flask import render_template
from flask import jsonify

from arrivals import get_bus_arrivals_data
import settings


app = Flask(
    import_name=__name__,
    static_folder=settings.STATIC_FOLDER,
    template_folder=settings.HTML_TEMPLATE_FOLDER,
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/bus/<bus_stop_id>')
def arrivals_data(bus_stop_id):
    return jsonify(**get_bus_arrivals_data(bus_stop_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')