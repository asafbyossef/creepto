# Gets top coin data from coinmarketcap API.
import json
from configparser import ConfigParser
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

config_object = ConfigParser()
config_object.read("resources/config.ini")
coinmarket_config = config_object["COINMARKET"]

URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
parameters = {"start": "1", "limit": "200", "convert": "USD"}
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": coinmarket_config["api_token"],
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(URL, params=parameters)
    data = json.loads(response.text)
    with open("../resources/currencies_200.json", "w") as file:
        json.dump(data, file)
except (ConnectionError, Timeout, TooManyRedirects) as exc:
    print(exc)
