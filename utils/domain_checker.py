import logging
import json
import os
import time

import pandas

from utils.rkn_data import ParserClient


logger = logging.getLogger(__name__)


class DomainChecker:
    def __init__(self, user_pash_file):
        self.name_file_rkn = ParserClient().file_name
        self.user_path_file = user_pash_file
        self.result_file = 'intersection.txt'

    def find_intersections(self) -> set[str]:
        set_txt = self._get_data_rkn_file()
        set_xlsx = self._get_data_user_file()
        intersection = set_txt.intersection(set_xlsx)
        self._write_result_to_file(intersection)
        return intersection

    def _get_data_rkn_file(self) -> set[str]:
        with open(self.name_file_rkn, 'r', encoding='utf-8') as f:
            data_txt = json.load(f)
            set_txt = set(data_txt.values())
            return set_txt

    def _get_data_user_file(self) -> set[str]:
        df_xlsx = pandas.read_excel(self.user_path_file)
        set_xlsx = set(df_xlsx.iloc[:, 0])
        return set_xlsx

    def _write_result_to_file(self, intersection) -> None:
        if os.path.exists(self.result_file):
            get_time = time.strftime('%Y.%m.%d_%H-%M')
            self.result_file = f"intersection_{get_time}.txt"
        with open(self.result_file, 'w', encoding='utf-8') as f:
            for item in intersection:
                f.write(f"{item}\n")
