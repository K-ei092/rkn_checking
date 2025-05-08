import logging
import json
import os
import re
import time

import pandas

from lexicon.lexicon import LEXICON_DCh
from utils.parser import ParserClient


logger = logging.getLogger(__name__)


class DomainChecker:
    result_file_rkn = 'intersection_rkn.txt'
    result_file_mnj = 'intersection_mnj.txt'

    def __init__(self, user_pash_file):
        self.name_file_rkn = ParserClient.file_name_rkn
        self.name_file_mnj = ParserClient.file_name_mnj
        self.user_path_file = user_pash_file

    def find_intersections_rkn(self) -> set[str]:
        set_txt = self._get_data_rkn_file()
        self.set_xlsx = self._get_data_user_file()
        intersection_rkn = set_txt.intersection(self.set_xlsx)
        self._write_result_rnk_to_file(intersection_rkn)
        return intersection_rkn

    def _get_data_rkn_file(self) -> set[str]:
        with open(self.name_file_rkn, 'r', encoding='utf-8') as f:
            data_txt = json.load(f)
            set_txt = set(data_txt.values())
            return set_txt

    def _get_data_user_file(self) -> set[str]:
        df_xlsx = pandas.read_excel(self.user_path_file)
        set_xlsx = set(df_xlsx.iloc[:, 0])
        return set_xlsx

    def _write_result_rnk_to_file(self, intersection) -> None:
        if os.path.exists(self.result_file_rkn):
            get_time = time.strftime('%Y.%m.%d_%H-%M')
            self.result_file_rkn = f"intersection_rkn_{get_time}.txt"
        with open(self.result_file_rkn, 'w', encoding='utf-8') as f:
            for item in intersection:
                f.write(f"{item}\n")

    def find_intersections_mnj(self) -> set[str]:
        self.set_csv = self._get_data_mnj_file()
        intersections_mnj = self._find_matching_lines()
        return intersections_mnj

    def _get_data_mnj_file(self) -> set[str]:
        df_csv = pandas.read_csv(self.name_file_mnj, delimiter=';', header=None)
        set_xlsx = set(df_csv.iloc[:, 1])
        return set_xlsx

    def _find_matching_lines(self) -> set[str]:
        matched_lines = set()
        for line in self.set_csv:
            extremist_urls = self.extract_urls(line)
            if not extremist_urls:
                continue
            for user_site in self.set_xlsx:
                for extr_url in extremist_urls:
                    user_site = str(user_site).strip()
                    if extr_url.endswith('/') and not user_site.endswith('/'):
                        user_site = user_site + '/'
                    if user_site == extr_url:
                        matched_lines.add(LEXICON_DCh["matching_line"].format(site=user_site, line=line))
                        break
        self._write_result_mnj_to_file(matched_lines)
        return matched_lines

    @staticmethod
    def extract_urls(text):
        pattern = r'https?://(?:www.)?([^ ,)]+)'
        matches = re.findall(pattern, text)
        excluded_domains = ['vk.com', 'ok.ru', 'vkontakte.ru', 'my.mail.ru', 'youtube.com']
        if any(domain in match for match in matches for domain in excluded_domains):
            return []
        else:
            return matches

    def _write_result_mnj_to_file(self, intersection) -> None:
        if os.path.exists(self.result_file_mnj):
            get_time = time.strftime('%Y.%m.%d_%H-%M')
            self.result_file_mnj = f"intersection_mnj_{get_time}.txt"
        with open(self.result_file_mnj, 'w', encoding='utf-8') as f:
            for item in intersection:
                f.write(f"{item}\n")
