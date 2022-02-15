import os

from flask import Flask, request, jsonify, send_file
from Report import Report

app = Flask(__name__)


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

        response = send_file(
            filename_or_fp=output_file_name,
            attachment_filename=output_file_name
        ), 200
        return response

    else:
        return jsonify(
            message="Key not found"
        ), 401


if __name__ == '__main__':
    app.run()
