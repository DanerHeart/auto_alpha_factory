import numpy
import json
import requests
from os.path import expanduser
from requests.auth import HTTPBasicAuth

brain_credentials_path = "./brain_credentials.txt"
wq_brain_api_auth = "https://api.worldquantbrain.com/authentication"
wq_brain_api_simulations = "https://api.worldquantbrain.com/simulations"

# load credentials
with open(brain_credentials_path) as f:
    credentials = json.load(f)

username, password = credentials


sess = requests.Session()
sess.auth = HTTPBasicAuth(username, password)

resp = sess.post(wq_brain_api_auth)

simulation_data = {
    "type": "REGULAR",
    "settings": {
        "instrumentType": "EQUITY",
        "region": "USA",
        "universe": "TOP3000",
        "delay": 1,
        "decay": 0,
        "neutralization": "INDUSTRY",
        "truncation": 0.08,
        "pasteurization": "ON",
        "unitHandling": "VERIFY",
        "nanHandling": "OFF",
        "language": "FASTEXPR",
        "visualization": False
    },
    "regular": "liabilities/assets"
}

from time import sleep
sim_resp = sess.post(
    wq_brain_api_simulations,
    json=simulation_data
)

sim_progress_url = sim_resp.headers['Location']

while True:
    sim_progress_resp = sess.get(sim_progress_url)
    retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
    if retry_after_sec == 0:
        break

    sleep(retry_after_sec)
alpha_id = sim_progress_resp.json()["alpha"]
print(alpha_id)
