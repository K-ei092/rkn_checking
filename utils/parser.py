import logging
import os
import time

import requests
from requests import Response

logger = logging.getLogger(__name__)


class ParserClient:
    url_rkn = 'https://rknweb.ru/api/v2/domains/'
    url_mnj = 'https://minjust.gov.ru/uploaded/files/exportfsm.csv'
    file_name_rkn = 'rkn_domains.txt'
    file_name_mnj = 'minjust.csv'

    def __init__(self, resource_rkn: bool):
        self.session = None
        self.url: str = self.url_rkn if resource_rkn else self.url_mnj
        self.file_name = self.file_name_rkn if resource_rkn else self.file_name_mnj

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
        }

    def open_session(self):
        self.session = requests.Session()
        return self.session

    def get_response(self, my_session, timeout) -> str | None:
        for attempt in range(3):
            try:
                response = my_session.get(url=self.url, headers=self.headers, timeout=timeout, verify=False)
                response_code = response.status_code
                response.raise_for_status()  # Вызывает исключение для ошибок HTTP
                if response_code == 200:
                    return self._write_file(response=response)
                time.sleep(3)
            except requests.exceptions.Timeout:
                logger.exception("Время ожидания ответа сайта истекло.")
                raise "Время ожидания ответа сайта истекло."
            except requests.exceptions.RequestException as e:
                logger.exception(f"Ошибка при запросе: {e}")
                raise "Ошибка при выполнении запроса."
            except ValueError:
                logger.exception("Ошибка при обработке ответа сайта.")
                raise "Ошибка при обработке ответа сайта."
            except Exception as e:
                logger.exception(f"Ошибка при запросе на сайт: {e}", exc_info=True)
                raise f"Ошибка при запросе на сайт: {e}"

    def _write_file(self, response: Response) -> str | None:
        try:
            if os.path.exists(self.file_name):
                os.remove(self.file_name)
            mode = 'w+' if self.file_name_rkn else 'wb+'
            data = response.text if self.file_name_rkn else response.content
            encoding = 'utf-8' if self.file_name_rkn else None
            with open(self.file_name, mode=mode, encoding=encoding) as file:
                    file.write(data)
                    file.close()
            return self.file_name
        except Exception as e:
            logger.exception(f"Ошибка при сохранении данных: {e}", exc_info=True)
            raise f"Ошибка при сохранении данных: {e}"


# Пример использования:
if __name__ == "__main__":
    parser_client = ParserClient(True)
    session = parser_client.open_session()
    file_name = parser_client.get_response(session, timeout=30)
    print(file_name)