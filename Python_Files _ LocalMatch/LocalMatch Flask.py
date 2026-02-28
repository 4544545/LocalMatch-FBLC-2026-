from flask import Flask, render_template, redirect, session, url_for, request, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import sqlite3
import requests

app = Flask(__name__)

# Essential for encrypting the user's session data
app.secret_key = "b7f8c9a2e41d6b0a9c7f1e5b3d8a2c6e"  

# Allows OAuth to work over HTTP during local development
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  

# What information we want to request from the user's Google account
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]

# Path to your Google Cloud Console credentials file
CREDENTIALS_PATH = os.path.join(
    os.path.dirname(__file__),
    "client_secret_2_851189569494-ebcd8bplvt0fjng5qu83h4ugsv6nbbl7.apps.googleusercontent.com.json"
)

# AUTHENTICATION ROUTES
@app.route("/")
def home():
    # Renders the initial landing/security page.
    return render_template("starting_page.html", logged_in=session.get("logged_in"), user=session.get("user"))

@app.route("/login")
def log_in():
    # Initiates the Google OAuth login.
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=url_for("callback", _external=True)
    )
    auth_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    session["state"] = state
    return redirect(auth_url)

@app.route("/callback")
def callback():
    # Handles the return from Google, fetches the token, and stores user profile in session.
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        state=session["state"],
        redirect_uri=url_for("callback", _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    # Use the Google People API to get the user's name and email
    service = build("people", "v1", credentials=creds)
    profile = service.people().get(
        resourceName="people/me",
        personFields="names,emailAddresses"
    ).execute()

    session["logged_in"] = True
    session["user"] = {
        "name": profile["names"][0]["displayName"],
        "email": profile["emailAddresses"][0]["value"]
    }
    return redirect(url_for("main"))


# DATA & MAP ROUTES
@app.route("/main")
def main():
    # Fetches all business locations from SQLite to display markers on the map.
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row  # Enables access by column name
    cursor = connection.cursor()

    cursor.execute("SELECT ID, Name, Type, ActiveDeals, Rating, ReviewCount, Location, Latitude, Longitude FROM Business")
    rows = cursor.fetchall()
    data_list = [dict(row) for row in rows]

    cursor.close()
    connection.close()
    return render_template("main.html", data_list=data_list)

@app.route("/reviews/<int:business_id>")
def reviews(business_id):
    # API endpoint to fetch specific reviews for one business.
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT ID, ReviewText, Rating FROM Reviews WHERE BusinessID = ?", (business_id,))
    review_list = [dict(row) for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    return jsonify(review_list)

@app.route("/reviews/add", methods=["POST"])
def add_review():
    # Handles review submission and automatically updates the Business average rating.
    data = request.json
    business_id, text, rating = data.get("business_id"), data.get("review_text"), data.get("rating")

    if not business_id or not text or not rating:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    connection = sqlite3.connect("localMatch.db")
    cursor = connection.cursor()
    
    # 1. Insert the new review
    cursor.execute("INSERT INTO Reviews (BusinessID, ReviewText, Rating) VALUES (?, ?, ?)", (business_id, text, rating))

    # 2. Re-calculate the average rating and review count for this business
    cursor.execute("SELECT COUNT(*), AVG(Rating) FROM Reviews WHERE BusinessID = ?", (business_id,))
    count, avg_rating = cursor.fetchone()
    
    # 3. Save the new averages back into the Business table
    cursor.execute("UPDATE Business SET ReviewCount = ?, Rating = ? WHERE ID = ?", (count, avg_rating, business_id))

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"status": "success"})

# FAVORITES & DASHBOARD
@app.route("/favorites/add", methods=["POST"])
def add_favorite():

    # Adds a business ID to the user's favorites list if not already present.
    business_id = request.json.get("business_id")
    connection = sqlite3.connect("localMatch.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM Favorites WHERE BusinessID = ?", (business_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Favorites (BusinessID) VALUES (?)", (business_id,))
        connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"status": "success"})

@app.route("/favorites")
def get_favorites():
    # API endpoint that joins Business and Favorites tables to return full favorite data.
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT b.* FROM Business b
        JOIN Favorites f ON f.BusinessID = b.ID
    """)
    fav_list = [dict(row) for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    return jsonify(fav_list)

@app.route("/dashboard")
def dashboard():
    # Renders the Business Analytics page with performance stats.
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    cursor.execute("SELECT Name, Rating, ReviewCount, ActiveDeals FROM Business ORDER BY Rating DESC")
    business_stats = [dict(row) for row in cursor.fetchall()]
    
    cursor.close()
    connection.close()
    return render_template("dashboard.html", stats=business_stats)

# SECURITY & UTILITIES
@app.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    # Server-side validation for Google reCAPTCHA 
    RECAPTCHA_SECRET_KEY = "6Ld0iXQsAAAAANJfiMCQ4XpIFvVp0EGGRc0EpBc1"
    token = request.get_json().get('token')

    # Send the token to Google's servers for verification
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={'secret': RECAPTCHA_SECRET_KEY, 'response': token}
    )
    
    result = response.json()
    return jsonify({"success": result.get('success')})

if __name__ == "__main__":
    app.run(debug=True)