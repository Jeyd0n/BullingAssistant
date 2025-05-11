import yaml
import sys
from typing import Dict
from loguru import logger
import time
import redis
import requests


sys.path.append('../')


def get_config() -> Dict:
    '''
    Load configuration settings from a local YAML file.

    This function reads a YAML configuration file located at `app/config.yaml` and parses its
    contents into a Python dictionary. The configuration typically includes folder paths and
    other parameters required across the OCR pipeline.

    Logging is used to track the status of loading the file. If the file is not found or
    cannot be opened, an error is raised.

    Returns
    -------
    Dict
        A dictionary containing the configuration parameters loaded from the YAML file.

    Raises
    ------
    FileExistsError
        If the configuration file `app/config.yaml` is not found or cannot be opened.

    Notes
    -----
    Make sure the file `config.yaml` exists in the `app` directory. The expected relative path
    from the current working directory is `app/config.yaml`.


    '''
    try:
        with open('app/config.yaml', 'r') as config:
            logger.info('Config was succesfuly open')
            return yaml.safe_load(stream=config)
    except:
        logger.warning('Not found config.yaml file')
        raise FileExistsError('You should add config.yaml file to ./app folder')
    

def wait_for_redis(host, port, retries=10, delay=3):
    for i in range(retries):
        try:
            client = redis.Redis(host=host, port=port)
            if client.ping():
                print("Redis is ready")

                return
        except redis.exceptions.ConnectionError:
            print(f"⏳ Waiting for Redis... retry {i+1}")
            time.sleep(delay)

    raise RuntimeError("❌ Redis не доступен.")


def wait_for_chroma(host, port, retries=10, delay=3):
    url = f"http://{host}:{port}"
    for i in range(retries):
        try:
            r = requests.get(url)
            if r.ok:
                print("Chroma is ready.")

                return
        except requests.exceptions.RequestException:
            print(f"⏳ Waiting for Chroma... retry {i+1}")
            time.sleep(delay)

    raise RuntimeError("❌ Chroma не доступна.")
