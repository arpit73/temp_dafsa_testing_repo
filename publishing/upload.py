import requests
from requests.exceptions import HTTPError
import prepare_tlds
import os
import tempfile
import shutil

COMMIT_HASH_URL = "https://api.github.com/repos/publicsuffix/list/commits/master"

LIST_URL = "https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat"

PSL_LOCATION = "./psl.dat"

DAFSA_OUTPUT = "./etld_data.inc"

exists = os.path.isfile(PSL_LOCATION)

#TODO Change condition later

if not exists:
    response = requests.get(LIST_URL, stream=True)
    print(response._content)
    with open(PSL_LOCATION, "wb") as psl:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                psl.write(chunk)
            else:
                print("Error!!!")

prepare_tlds.main(DAFSA_OUTPUT, PSL_LOCATION)


def get_latest_hash(url):
    try:
        response = requests.get(url)
        return  response.json()['sha']
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}") 
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        print("Failed")
 
latest_hash = get_latest_hash(COMMIT_HASH_URL)
print(latest_hash)

def get_dafsa_creation_scripts():
    dirpath = tempfile.mkdtemp()
    # ... do stuff with dirpath
    shutil.rmtree(dirpath)
def check_last_stored_hash():
    pass

# while(True):
#     current_hash = get_latest_hash()
#     if(last_hash!=current_hash):
#         # download()
#         # dafsa()
#     sleep(5*60)
