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
        
        config['USER_ID'] = user_info['id']
        config['ACCESS_TOKEN'] = res_data['access_token']
        
        try:
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            return """
            <h1>Success!</h1>
            <p><b>config.json</b> has been updated with the new User ID and Access Token.</p>
            <p>You can now close this tab.</p>
            """
        except Exception as e:
            return f"<h1>File Error</h1><p>Could not write to config.json: {str(e)}</p>", 500
    else:
        return f"<h1>OAuth Error</h1><p>{res_data}</p>", 400

if __name__ == '__main__':
    app.run(port=5000)