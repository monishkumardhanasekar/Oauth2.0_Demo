#  OAuth 2.0 Flask Demo

## 🔐 What is OAuth 2.0?

OAuth 2.0 is an open standard for authorization. It allows third-party applications to access user data without exposing user credentials.

Instead of sharing passwords, OAuth provides a **secure, token-based system** to grant limited access to user data (such as profile or email). This is widely used by platforms like **Google, Facebook, Microsoft** for login and API access.

---

## ⚙️ Project Setup

### 1. Set Up Google API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Go to **APIs & Services > Library**.
4. Enable the **Google+ API** (or "People API").
5. Go to **APIs & Services > Credentials**.
6. Click **Create Credentials > OAuth 2.0 Client ID**.
7. Set Application type to **Web application**.
8. Add the following **Redirect URI**:

   ```
   http://localhost:5000/callback
   ```
9. Copy the **Client ID** and **Client Secret**.

### 2. Create a `.env` File

Inside your project directory:

```
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:5000/callback
```

---

## 📦 Install Dependencies

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required libraries:

```bash
pip install flask requests python-dotenv
```

---

## ▶️ How to Run and Test

1. Start the Flask server:

```bash
python app.py
```

2. Open your browser and go to:

```
http://localhost:5000
```

3. Click **Login with Google**.

4. You’ll be redirected to the Google login and consent screen.

5. Upon success, you’ll be redirected back and see your **profile details**.

---

## 👀 What Happens When You Sign In?

Once you log in using your Google account, the app displays something like:

```
Logged in as John Doe
```

```json
{
  "email": "johndoe@example.com",
  "name": "John Doe",
  "id": "123456789"
}
```

This means:

* You authenticated using Google.
* The app received your name, email, and user ID securely using OAuth 2.0.
* No password was shared or stored.

---

## 🧠 Code Explanation

### `app.py` Routes

* `/` → Homepage with a **Login with Google** link.
* `/login` → Redirects to Google’s OAuth 2.0 authorization endpoint.
* `/callback` → Handles Google’s response and processes user data.

### Authorization Flow

1. User clicks **Login with Google**.
2. Redirected to Google OAuth page.
3. User grants permission.
4. Google sends an **authorization code** to `/callback`.
5. App exchanges the code for an **access token**.
6. App fetches **user profile** using the access token.
7. User’s name and email are displayed.

---

## 🔄 Flow Diagram

```
User --> Homepage --> Click "Login with Google"
     --> Google Consent Screen
     --> Authorization Code sent to /callback
     --> App exchanges for Access Token
     --> App fetches profile info
     --> App displays name and email
```

---

## ✅ Verifying It Works

* If you see a login page → OAuth works.
* If redirected back with your **Google name and email** displayed → Token exchange and data fetch works.
* If any error occurs, double-check:

  * `.env` values
  * Redirect URI matches Google credentials
  * Google+ API is enabled

---

## Conclusion

This project demonstrates a minimal, working example of **OAuth 2.0 with Google** using **Flask**. It's secure, extensible, and useful for adding third-party login to your apps.

---
