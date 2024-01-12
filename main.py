# wow_mounts.py
import requests
import toml
from pprint import pprint

def load_credentials():
    with open("credentials.toml", "r") as file:
        config = toml.load(file)
        return config["credentials"]["client_id"], config["credentials"]["client_secret"]

def authenticate():
    client_id, client_secret = load_credentials()

    auth_url = "https://eu.battle.net/oauth/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(auth_url, data=data)
    response.raise_for_status()

    return response.json()["access_token"]

def get_mounts(access_token, region="eu"):
    mounts_url = f"https://{region}.api.blizzard.com/data/wow/mount/index"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Battlenet-Namespace": "static-" + region,
    }

    response = requests.get(mounts_url, headers=headers)
    response.raise_for_status()

    return response.json()

def main():
    try:
        access_token = authenticate()

        mounts_data = get_mounts(access_token)

        pprint(mounts_data)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
