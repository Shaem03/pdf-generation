import os

import pdfkit
from dateutil import parser
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

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
        x = parser.parse(self.report_data['report']['created'])
        response_rates = {
            "student_name": self.report_data['student']['fullname']['name'],
            "student_email": self.report_data['student']['email']['address'],
            "report_created": x.strftime("%d/%m/%Y"),
            "collected_errors": self.report_data['collectedErrors'],
            "fixes": self.report_data['essayFix']
        }

        env = Environment(loader=FileSystemLoader(jinja_template))
        template = env.get_template(f'{template_name}_sample.html')

        output_from_parsed_template = template.render(data=response_rates)

        with open(f"{temp_path}{template_name}.html", "w") as fh:
            fh.write(output_from_parsed_template)

        pdfkit.from_file(f'{temp_path}{template_name}.html',
                         f'{temp_path}{template_name}.pdf')

        return f'{temp_path}{template_name}.pdf'
