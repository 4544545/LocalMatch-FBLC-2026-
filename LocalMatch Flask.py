from flask import Flask, render_template, redirect, session, url_for, request, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "b7f8c9a2e41d6b0a9c7f1e5b3d8a2c6e"  # DEV ONLY

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # DEV ONLY

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]

CREDENTIALS_PATH = os.path.join(
    os.path.dirname(__file__),
    "client_secret_2_851189569494-ebcd8bplvt0fjng5qu83h4ugsv6nbbl7.apps.googleusercontent.com.json"
)


@app.route("/")
def home():
    return render_template("starting_page.html", logged_in=session.get("logged_in"), user=session.get("user"))


@app.route("/login")
def log_in():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=url_for("callback", _external=True)
    )
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    session["state"] = state
    return redirect(auth_url)


#authornization for the person / sign up system 
@app.route("/callback")
def callback():
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        state=session["state"],
        redirect_uri=url_for("callback", _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    service = build("people", "v1", credentials=creds)
    profile = service.people().get(
        resourceName="people/me",
        personFields="names,emailAddresses"
    ).execute()

    # Store user info in session
    session["logged_in"] = True
    session["user"] = {
        "name": profile["names"][0]["displayName"],
        "email": profile["emailAddresses"][0]["value"]
    }

    return redirect(url_for("main"))


# def check_db_connection()


#route to get buisness information 
@app.route("/main")
def main():
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ID, Name, Type, ActiveDeals, Rating, ReviewCount, Location, Latitude, Longitude
        FROM Business
    """)
    rows = cursor.fetchall()

    # Convert sqlite3.Row → dict
    data_list = [dict(row) for row in rows]

    print("Number of businesses:", len(data_list)) 
    print("Numeber of reviews:",)
    if data_list:
        print("First business:", data_list[0:2])


    cursor.close()
    connection.close()

    return render_template("main.html", data_list=data_list)

@app.route("/reviews/<int:business_id>")
def reviews(business_id):
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ID, ReviewText, Rating 
        FROM Reviews
        WHERE BusinessID = ?
    """, (business_id,))
    rows = cursor.fetchall()
    review_list = [dict(row) for row in rows]

    cursor.close()
    connection.close()
    return jsonify(review_list)

# --------------------------
# Add a new review
# --------------------------
@app.route("/reviews/add", methods=["POST"])
def add_review():
    data = request.json
    business_id = data.get("business_id")
    text = data.get("review_text")
    rating = data.get("rating")

    if not business_id or not text or not rating:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    connection = sqlite3.connect("localMatch.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Reviews (BusinessID, ReviewText, Rating)
        VALUES (?, ?, ?)
    """, (business_id, text, rating))

    # Update ReviewCount and average Rating in Business table
    cursor.execute("""
        SELECT COUNT(*), AVG(Rating) FROM Reviews WHERE BusinessID = ?
    """, (business_id,))
    count, avg_rating = cursor.fetchone()
    cursor.execute("""
        UPDATE Business SET ReviewCount = ?, Rating = ? WHERE ID = ?
    """, (count, avg_rating, business_id))

    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"status": "success"})

# --------------------------
# Add a favorite
# --------------------------
@app.route("/favorites/add", methods=["POST"])
def add_favorite():
    data = request.json
    business_id = data.get("business_id")
    if not business_id:
        return jsonify({"status": "error"}), 400

    connection = sqlite3.connect("localMatch.db")
    cursor = connection.cursor()

    # Check if already favorite
    cursor.execute("SELECT * FROM Favorites WHERE BusinessID = ?", (business_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Favorites (BusinessID) VALUES (?)", (business_id,))
        connection.commit()

    cursor.close()
    connection.close()
    return jsonify({"status": "success"})

# --------------------------
# Get all favorites
# --------------------------
@app.route("/favorites")
def get_favorites():
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT b.ID, b.Name, b.Type, b.ActiveDeals, b.Rating, b.ReviewCount, b.Location, b.Latitude, b.Longitude
        FROM Business b
        JOIN Favorites f ON f.BusinessID = b.ID
    """)
    rows = cursor.fetchall()
    fav_list = [dict(row) for row in rows]

    cursor.close()
    connection.close()
    return jsonify(fav_list)

    
@app.route("/api/data")
def api_data():
    connection = sqlite3.connect("localMatch.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Business")
    rows = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    print("here",rows)

    return {"data_list": rows}  # now JS can fetch it

if __name__ == "__main__":
    app.run(debug=True)
