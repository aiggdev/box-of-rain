import logging
import json
from os import lseek
import uuid
import requests
import bleach


def read_data_from_json(file_name: str) -> dict:

    try:
        file = open(file_name, 'r')
        data_file = json.load(file)
    except:
        logging.error(f'read_data_from_json failed loading json file.')
    finally:
        file.close()

    if data_file:
        return data_file
    logging.error('error : folder_data was empty.')
    return []


def write_list_to_file(data: list, file_name: str) -> bool:

    try:
        with open(file_name, 'a+') as outfile:
            outfile.write('\n'.join(data))
        return True
    except:
        return False


def write_file_to_json(data: str, file_name: str) -> bool:

    j_data = json.dumps(data)

    try:
        with open(file_name, 'a+') as outfile:
            outfile.write("\n")
            json.dump(j_data, outfile)
        return True
    except:
        return False


def write_dict_to_json(data: dict, file_name: str) -> bool:

    #j_data = json.dumps(data, indent = 4)

    try:
        with open(file_name, 'a+') as outfile:
            outfile.write("\n")
            json.dump(data, outfile)
        return True
    except:
        return False


def strip_nbs(place: str) -> str:
    return place.replace("\u00a0", " ")


def create_uuid():
    u = str(uuid.uuid4())
    return u[::-1]


def check_url(url):
    prepared_request = requests.PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return bleach.clean(prepared_request.url)
    except requests.exceptions.MissingSchema:
        raise Exception
