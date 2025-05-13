import os
import json
import requests
from flask import Flask, redirect, request, session, url_for
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with secure secret in production

# OAuth 2.0 config
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
USER_INFO = "https://www.googleapis.com/oauth2/v1/userinfo"
SCOPE = "email profile"

# Load role-based access data from users.json
with open('users.json') as f:
    ROLES = json.load(f)

@app.route('/')
def home():
    user = session.get('user')
    if user:
        return f'''
            <h2>Welcome, {user['name']}!</h2>
            <p>You are logged in as: <strong>{user['email']}</strong></p>
            <p>Your role is: <strong>{user['role']}</strong></p>
            <a href="/dashboard">Go to Dashboard</a><br>
            <a href="/logout">Logout</a>
        '''
    else:
        return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    return redirect(f"{AUTH_URI}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPE}&access_type=offline")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization code not found.", 400

    # Exchange code for access token
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(TOKEN_URI, data=data)
    token_json = token_response.json()

    access_token = token_json.get('access_token')
    if not access_token:
        return "Failed to retrieve access token.", 400

    # Fetch user info from Google
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info = requests.get(USER_INFO, headers=headers).json()

    email = user_info.get('email')
    role = ROLES.get(email, 'guest')  # Default to guest if not found

    # Store in session
    session['user'] = {
        'name': user_info.get('name'),
        'email': email,
        'role': role
    }

    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('home'))

    if user['role'] == 'admin':
        return f"<h1>Admin Dashboard</h1><p>Welcome, {user['name']}!</p><p>Access to all features.</p><a href='/logout'>Logout</a>"
    elif user['role'] == 'user':
        return f"<h1>User Dashboard</h1><p>Welcome, {user['name']}!</p><p>Limited access granted.</p><a href='/logout'>Logout</a>"
    else:
        return f"<h1>Guest Access</h1><p>Welcome, {user['name']}!</p><p>No special permissions.</p><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
