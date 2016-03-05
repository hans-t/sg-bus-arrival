from flask import Flask
from flask import send_from_directory
from flask import jsonify

import bus_stop
import settings


app = Flask(
    import_name=__name__,
    static_folder=settings.STATIC_FOLDER,
    static_url_path=settings.STATIC_URL_PATH,
    template_folder=settings.HTML_TEMPLATE_FOLDER,
)


@app.route('/')
def index():
    return send_from_directory(settings.STATIC_FOLDER, 'html/index.html')


@app.route('/api/bus_stop/<bus_stop_id>')
def arrivals_data(bus_stop_id):
    return jsonify(**bus_stop.get_info(bus_stop_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)