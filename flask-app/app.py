import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from Report import Report

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(".env")
app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "Welcome!"


@app.route('/generate', methods=['POST'])
def pdf_handler():
    x_api_key = request.headers.get('x-api-key')
    if x_api_key == os.environ.get('X_API_KEY'):
        req_body = request.get_json()

        report = Report(req_body)

        output_file_name = report.write_pdf()

        response = jsonify(
            reportPresignedUrl=output_file_name
        ), 200

        return response

    else:
        return jsonify(
            message="Key not found"
        ), 401


@app.route('/common', methods=['POST'])
def common():
    x_api_key = request.headers.get('x-api-key')
    if x_api_key == os.environ.get('X_API_KEY'):
        req_body = request.get_json()

        report = Report(req_body)

        output_file_name = report.write_common()

        response = jsonify(
            reportPresignedUrl=output_file_name
        ), 200

        return response

    else:
        return jsonify(
            message="Key not found"
        ), 401


if __name__ == '__main__':
    app.run(port=6000)
