import json

from flask import Flask, jsonify, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from database import session, Log
import datetime
import os


app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather Bot Logs API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger_json():
    return send_from_directory(os.getcwd(), 'swagger.json')


@app.route('/logs', methods=['GET'])
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    start_str = request.args.get('start')
    end_str = request.args.get('end')

    logs = session.query(Log)

    if start_str:
        start = datetime.datetime.fromisoformat(start_str)
        logs = logs.filter(Log.timestamp >= start)
    if end_str:
        end = datetime.datetime.fromisoformat(end_str)
        logs = logs.filter(Log.timestamp <= end)

    total_logs = logs.count()
    res_logs = logs.offset((page - 1) * per_page).limit(per_page).all()

    log_list = []
    for log in res_logs:
        decoded_response = json.loads(f'"{log.response}"')
        log_list.append(
            {
                'user_id': log.user_id,
                'command': log.command,
                'response': decoded_response,
                'timestamp': log.timestamp.isoformat()
            }
        )

    return jsonify(
        {
            'total_logs': total_logs,
            'page': page,
            'per_page': per_page,
            'logs': log_list
        }
    )


@app.route('/logs/<int:user_id>', methods=['GET'])
def get_user_logs(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    start_str = request.args.get('start')
    end_str = request.args.get('end')

    logs = session.query(Log).filter_by(user_id=user_id)

    if start_str:
        start = datetime.datetime.fromisoformat(start_str)
        logs = logs.filter(Log.timestamp >= start)
    if end_str:
        end = datetime.datetime.fromisoformat(end_str)
        logs = logs.filter(Log.timestamp <= end)

    total_logs = logs.count()
    res_logs = logs.offset((page - 1) * per_page).limit(per_page).all()

    log_list = []
    for log in res_logs:
        decoded_response = json.loads(f'"{log.response}"')
        log_list.append(
            {
                'user_id': log.user_id,
                'command': log.command,
                'response': decoded_response,
                'timestamp': log.timestamp.isoformat()
            }
        )

    return jsonify(
        {
            'total_logs': total_logs,
            'page': page,
            'per_page': per_page,
            'logs': log_list
        }
    )


def run_rest_api():
    app.run(port=5000)
