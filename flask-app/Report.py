import os
import uuid

import boto3
import pdfkit
from dateutil import parser
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from Client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
load_dotenv(".env")
jinja_template = os.environ.get('JINJA_TEMPLATE')
temp_path = os.environ.get('TEMP_PATH')
output_pdf_location = os.environ.get('OUTPUT_PDF_LOCATION')


class Report:
    report_data = None

    def __init__(self, reports):
        self.report_data = reports

    def write_pdf(self):
        template_name = "report"
        created_date = self.report_data['report']['created']

        x = parser.parse(f"{created_date[0]}/{created_date[1]}/{created_date[2]}")
        response_rates = {
            "student_name": self.report_data['student']['fullname']['name'],
            "student_email": self.report_data['student']['email']['address'],
            "report_created": x.strftime("%d/%m/%Y"),
            "collected_errors": self.report_data['collectedErrors'],
            "error_length": len(self.report_data['collectedErrors']),
            "fixes": self.report_data['essayFix']
        }

        env = Environment(loader=FileSystemLoader(jinja_template))
        template = env.get_template(f'{template_name}_sample.html')

        output_from_parsed_template = template.render(data=response_rates)

        with open(f"{temp_path}{template_name}.html", "w") as fh:
            fh.write(output_from_parsed_template)

        # options = {
        #     'margin-bottom': '0.75in'
        # }

        out_pdf = f'{temp_path}{template_name}.pdf'
        pdfkit.from_file(f'{temp_path}{template_name}.html',
                         out_pdf)

        # report_id = self.report_data['report']['id']
        report_id = self.report_data['report']['name']

        client = Client()
        output_file_name = f'reports/{report_id}.pdf'
        client.put_to_bucket(out_pdf, output_file_name)

        # presigned_url = client.get_presigned_url(output_file_name)

        return output_file_name
