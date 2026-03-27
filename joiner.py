import requests
import time
import json

with open('config.json', 'r') as f:
    config = json.load(f)

USER_ID = config['USER_ID']
ACCESS_TOKEN = config['ACCESS_TOKEN']
TOKEN = config['TOKEN']
SERVER_IDS = config['SERVER_IDS']

def bulk_join():
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "access_token": ACCESS_TOKEN
    }

    for server_id in SERVER_IDS:
        url = f"https://discord.com/api/v10/guilds/{server_id}/members/{USER_ID}"
        
        try:
            response = requests.put(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                print(f"Successfully joined: {server_id}")
            elif response.status_code == 204:
                print(f"Already in server: {server_id}")
            elif response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                print(f"Rate limited! Waiting {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                print(f"Failed {server_id}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error joining {server_id}: {e}")

        time.sleep(3)

    print("\nFinished joining all servers.")

if __name__ == "__main__":
    bulk_join()