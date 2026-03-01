# LocalMatch — Business Discovery Platform

A full-stack web platform that helps users **discover, evaluate, and support small local businesses** in their community. Built for the **Byte-Sized Business Boost (FBLC 2026)** competition.

LocalMatch combines an  Leaflet map, a verified review system, real-time filtering, and Google OAuth authentication — all powered by a Python Flask backend and SQLite database.



## What It Does

Small businesses struggle with visibility. LocalMatch solves this by giving users a single platform to:

- **Find** local businesses on a live interactive map centred on the GTA
- **Filter** by service category, rating, or active deals — instantly, with no page reload
- **Read & write reviews** that are verified (CAPTCHA-gated) to keep feedback trustworthy
- **Bookmark** favourite businesses that stay  across sessions
- **View a business dashboard** with ratings, review counts, and deal information


Tech Stack
**Frontend**, HTML5, CSS3,  JavaScript
**Map**, Leaflet.js + MapTiler tile layer 
 **Backend**, Python 3, Flask 
**Database**, SQLite (via Python's built-in `sqlite3`)
**Authentication**, Google OAuth 2.0 (`google-auth-oauthlib`) 
**Bot Prevention**, CAPTCHA on the entry page 



Features

- Interactive map*— Leaflet markers created once on load; filtering only shows/hides them 
-  Live search + filtering — search by name, type, or location; filter by category; sort by rating or deals
- Review system — submit star ratings + written reviews; average recalculated on every insert
-  Favourites tab — bookmark businesses; favourites stay in the database
- Google OAuth login — no passwords stored; Google handles authentication
- CAPTCHA — Box CAPTCHA on the starting page prevents bot submissions
- Business dashboard — overview of all businesses with ratings and review counts



## 📁 Project Structure

```
LocalMatch/
│
├── LocalMatch Flask.py                   # Flask app — all routes and database logic
├── localMatch.db            # SQLite database
├── localMatch Database.py   # Script to seed the database with initial business data

├── templates/
│   ├── starting_page.html   # Entry page with CAPTCHA + Google OAuth login
│   ├── main.html            # Main app — map, sidebar, search, reviews, favorites
│   └── dashboard.html       # Business analytics view
│
└── static/
    ├── main_style.css       # Styles for the main app
    └── starting_style.css   # Styles for the starting page
```



▶️ How to Run Locally

### Prerequisites

Make sure you have the following installed:
- **Python 3.8 or higher** — [Download here](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** — [Download here](https://git-scm.com/)



#Step 1 — Clone the repository

```bash
git clone https://github.com/4544545/LocalMatch-FBLC-2026-.git
cd LocalMatch-FBLC-2026-
```

---

Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, google-auth-oauthlib, and all other required packages.

---

### Step 3 — Set up the database

Run this **once** to create the SQLite database:

```bash
python "localMatch Database.py"
```

You should see a `localMatch.db` file appear in the project folder. If it already exists, skip this step.

---

### Step 4 — Run the Flask app

```bash
python app.py
```

You should see output like this in your terminal:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### Step 5 — Open in your browser

Go to:

```
http://127.0.0.1:5000
```

You will land on the **starting page**. Solve the CAPTCHA, then sign in with Google to access the full platform.

---

## ⚙️ How It Works (Under the Hood)

```
SQLite Database
      ↓
Flask queries and formats the data
      ↓
HTML page receives it via {{ data_list | tojson }}
      ↓
JavaScript reads the array and:
   → Places one Leaflet marker per business (stored as b.marker)
   → Populates the sidebar directory
   → Wires search, filter, and sort to a single applyFilters() function
      ↓
When a review is submitted:
   → POST request sent to /reviews/add
   → Flask inserts into Reviews table
   → Flask runs SELECT AVG(Rating) and updates the Business table
   → Frontend re-renders the business detail with fresh data
```

---

## 🚀 Future Improvements

- [ ] Geolocation — "Sort by distance from me" using the Haversine formula
- [ ] Color-coded map markers by rating (green / amber / red)
- [ ] AI-powered review spam detection
- [ ] Business owner analytics dashboard (review trends over time)
- [ ] Mobile app (Android / iOS)
- [ ] Cloud deployment on Render or Railway
- [ ] Business self-registration (no manual DB seeding)




This project was built for academic and competition purposes.
