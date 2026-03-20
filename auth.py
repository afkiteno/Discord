from flask import Flask, request
import requests
import json

app = Flask(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REDIRECT_URI = config['REDIRECT_URI']

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code found.", 400

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post("https://discord.com/api/v10/oauth2/token", data=data)
    res_data = response.json()
    
    if "access_token" in res_data:
        user_info = requests.get("https://discord.com/api/v10/users/@me", headers={
            "Authorization": f"Bearer {res_data['access_token']}"
        }).json()
        
        return f"""
        <h1>Success!</h1>
        <p><b>User ID:</b> {user_info['id']}</p>
        <p><b>Access Token:</b> {res_data['access_token']}</p>
        """
    else:
        return f"Error: {res_data}", 400

if __name__ == '__main__':
    app.run(port=5000)