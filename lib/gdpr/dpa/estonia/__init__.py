import os
import math
import requests
import json
import datetime
import hashlib

from .. import DPA

from bs4 import BeautifulSoup

from ...services.links_from_soup_service import links_from_soup_service
from ...services.filename_from_path_service import filename_from_path_service
from ...services.pdf_to_text_service import pdf_to_text_service

from ...specifications import pdf_file_extension_specification
from ...specifications import page_fully_rendered_specification
from ...specifications import gdpr_retention_specification

from ...modules.pagination import Pagination
from ...policies import bulk_collect_location_policy
from ...policies import gdpr_policy

class Estonia(DPA):
    def __init__(self):
        iso_code='EE'
        super().__init__(iso_code)

    def get_docs(self, path):
        if bulk_collect_location_policy.is_allowed(path) is False:
            raise ValueError('Bulk collect path is illegal: ' + path)

        source = self.sources[0]

        host = source['host']
        start_path = source['start_path']
        target_element = source['target_element']
        render_type = source['render_type']

        # for each page in pages.. do as the last stage.
        try:
            results_response = requests.request('GET', host + start_path)
            results_html = results_response.content
            results_soup = BeautifulSoup(results_html, 'html.parser')

            result_dates = []
            date_areas = results_soup.find_all('span', class_=target_element['date'].split('.')[-1])
            for date_area in date_areas:
                date_prefix = date_area.get_text()
                date_prefix = date_prefix.replace(' ', '')

                date_str = date_prefix.split('-')[0]
                date_str = date_str.strip()

                tmp = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                result_date = datetime.date(tmp.year, tmp.month, tmp.day)

                result_dates.append(result_date)

            pagination = Pagination()
            pagination.add_link(host + start_path)

            pagination_links = links_from_soup_service(results_soup, target_element=target_element['pagination'])
            for pagination_link in pagination_links:
                page_url = pagination_link[1]
                pagination.add_link(host + page_url)

            folder_name = self.country.replace(' ', '-').lower()
            root_path = path + '/' + folder_name

        except:
            print("Something went wrong.")

        while pagination.has_next():
            page_url = pagination.get_next()
            try:
                results_response = requests.request('GET', page_url)
                results_html = results_response.content
                results_soup = BeautifulSoup(results_html, 'html.parser')
            except:
                print("Something went wrong.")

            result_links = links_from_soup_service(results_soup, target_element=target_element['results'])

            if len(result_links) != len(result_dates):
                continue

            for i in range(len(result_links)):
                result_date = result_dates[i]
                if gdpr_retention_specification.is_satisfied_by(result_date) is False:
                    continue

                result_link = result_links[i]
                result_title = result_link[0]
                result_url = result_link[1]

                try:
                    document_response = requests.request('GET', host + result_url)
                    document_html = document_response.content
                    document_soup = BeautifulSoup(document_html, 'html.parser')
                except:
                    print("Something went wrong.")

                document_folder = result_title
                document_folder_md5 = hashlib.md5(document_folder.encode()).hexdigest()

                dirpath = root_path + '/' + document_folder_md5
                try:
                    os.makedirs(dirpath)
                except FileExistsError:
                    print('file already exists, continue.')

                language_code = 'et'

                document_links = links_from_soup_service(document_soup, target_element=target_element['document'])
                document_link = document_links[0]

                try:
                    pdf_url = document_link[1]
                    pdf_response = requests.request('GET', pdf_url)
                    pdf_content = pdf_response.content

                    with open(dirpath + '/' + language_code + '.pdf', 'wb') as f:
                        f.write(pdf_content)

                    pdf_text = pdf_to_text_service(dirpath + '/' + language_code + '.pdf')

                    with open(dirpath + '/' + language_code + '.txt', 'w') as f:
                        f.write(pdf_text)
                except:
                    print("Oops! pdf could not be downloaded.")

            pagination_links = links_from_soup_service(results_soup, target_element=target_element['pagination'])
            for pagination_link in pagination_links:
                page_url = pagination_link[1]
                pagination.add_link(host + page_url)

        return True
