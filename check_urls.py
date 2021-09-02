import pandas as pd
import lib
import requests
from lxml.html import fromstring
import time
import logging

df = pd.read_csv('data/urls_three_clean.csv')
# json_data = lib.read_data_from_json('data/alt-search-data.json')
# df = pd.DataFrame(json_data['data'])

logger = logging.getLogger(__name__)
log_format = "%(levelname)s:%(name)s - %(asctime)s - %(message)s"


def try_request(url: str):

    r = requests.get(url)

    for i in range(5):
        result = r

        if r.status_code == 200:
            print(f'200 for: {url}')
            return result
        else:
            logger.info(f"reqg {r} {result}")
            time.sleep(1)
            print('went to sleep')
            r = requests.get(url)
            result = r
    else:
        raise Exception(f"Error calling requests: Url {url} "
                        f"gave status code {r.status_code}, headers "
                        f"{r.headers} and response {result}. Attempt: {i}")


if __name__ == "__main__":

    url_list = df['url']
    title_list = []
    failed_urls = []

    for u in url_list:
        try:
            response = try_request(u)
            if response:
                tree = fromstring(response.content)
                title = str(tree.findtext('.//title'))
                title_list.append(title)
                print(f'got response - title: {title}.')
                # sc_list.append(response.status_code)
            else:
                title_list.append('error')
                failed_urls.append(u)
                print(f'else - got no title')
        except:
            title_list.append('error')
            failed_urls.append(u)
            print(f'except - got no title.')

    df['title'] = title_list
    df.to_csv('from_vsc.csv')

    if len(failed_urls) != 0:
        lib.write_file_to_json(failed_urls, 'failed_urls.json')
