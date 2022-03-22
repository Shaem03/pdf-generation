import itertools
import os
import uuid

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
        self.env = Environment(loader=FileSystemLoader(jinja_template))
        self.client = Client()

    def write_pdf(self):
        template_name = "report"
        created_date = self.report_data['report']['created']

        x = parser.parse(f"{created_date[0]}/{created_date[1]}/{created_date[2]}")
        # x = parser.parse(created_date)

        response_rates = {
            "report_name": self.report_data['report']['name'],
            "student_name": self.report_data['student']['fullname']['name'],
            "student_email": self.report_data['student']['email']['address'],
            "report_created": x.strftime("%d/%m/%Y"),
            "collected_errors": self.report_data['collectedErrors'],
            "error_length": len(self.report_data['collectedErrors']),
            "fixes": self.report_data['essayFix'],
            "language_score": self.report_data['essay']['languageScore'],
            "content_score": self.report_data['essay']['contentScore'],
            "feedback": self.report_data['essay']['feedback']
        }

        template = self.env.get_template(f'{template_name}_sample.html')

        output_from_parsed_template = template.render(data=response_rates)

        with open(f"{temp_path}{template_name}.html", "w") as fh:
            fh.write(output_from_parsed_template)

        out_pdf = f'{temp_path}{template_name}.pdf'
        pdfkit.from_file(f'{temp_path}{template_name}.html',
                         out_pdf)

        # report_id = self.report_data['report']['id']
        report_id = self.report_data['report']['name']

        output_file_name = f'reports/{report_id}.pdf'
        self.client.put_to_bucket(out_pdf, output_file_name)

        # presigned_url = client.get_presigned_url(output_file_name)

        return output_file_name

    def write_common(self, report_type):
        common_arr = {}
        template_name = "common_error"
        collected_errors_rrr = []
        if report_type['student'] != "null":
            title_name = self.report_data['content'][0]['student']['fullname']['name']
        else:
            assignment_name = self.report_data['content'][0]["report"]['name'].split("_")
            title_name = " ".join(assignment_name[:-1])

        for val in self.report_data['content']:
            for vv in val["collectedErrors"]:
                assig_name = val['report']['name'].split("_")
                vv["name"] = " ".join(assig_name[:-1]) if report_type['student'] != "null" else \
                    val["student"]["fullname"]["name"]
                collected_errors_rrr.append(vv)

        # collesscted_errors = [val['collectedErrors'] for val in self.report_data['content']]
        # merged = list(itertools.chain(*collesscted_errors))
        err_types = set([val['fixType'] for val in collected_errors_rrr])
        for val in err_types:
            all_words = list(filter(lambda person: person['fixType'] == val, collected_errors_rrr))
            sorted_words = sorted(all_words, key=lambda d: d['replacedWord'])
            set_common_words = {}

            for value in sorted_words:
                replaced_word = value['replacedWord']
                corr_err = list(filter(lambda person: person['replacedWord'] == replaced_word, sorted_words))

                if replaced_word in set_common_words:
                    cont = set_common_words[replaced_word]["count"] + value['count']
                    set_common_words[replaced_word]["count"] = cont
                else:
                    set_common_words[replaced_word] = {
                        "all": corr_err,
                        "count": value['count']
                    }

            common_arr[val] = set_common_words

        response_rates = {
            "title": title_name,
            "collected_errors": common_arr,
            "col_name": report_type['student'] != "null"
        }

        template = self.env.get_template(f'{template_name}_sample.html')

        output_from_parsed_template = template.render(data=response_rates)

        with open(f"{temp_path}{template_name}.html", "w") as fh:
            fh.write(output_from_parsed_template)

        out_pdf = f'{temp_path}{template_name}.pdf'
        pdfkit.from_file(f'{temp_path}{template_name}.html',
                         out_pdf)

        # report_id = self.report_data['report']['id']
        report_id = self.report_data["content"][0]["student"]["fullname"]["name"]

        output_file_name = f'reports-common/{report_id}.pdf'
        self.client.put_to_bucket(out_pdf, output_file_name)

        return output_file_name
