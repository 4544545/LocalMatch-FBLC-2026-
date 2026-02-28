# Business Review Mapping Platform

A full-stack web application that allows users to explore businesses on an interactive map, view reviews, filter results, and submit new reviews in real time.

This project integrates a Python Flask backend, SQL database, and a dynamic HTML/CSS/JavaScript frontend.

## Features

- Interactive map with business markers
- Sidebar with  filtering
- Business search functionality
- Review submission
- Reviews stored in SQL database
- Flask API routes for data handling
- Clean frontend layout with separated CSS

##  Tech Used

**Frontend**
- HTML5
- CSS3
- JavaScript
- Leaflet 

**Backend**
- Python
- Flask
- REST API routes

**Database**
- SQL 



## How It Works

1. Flask connects to the SQL database.
2. Businesses and reviews are fetched using API routes.
3. Data is sent to the frontend as JSON.
4. JavaScript dynamically renders:
   - Map markers
   - Business details
   - Reviews
5. When a user submits a review:
   - It is sent to Flask via POST request
   - Stored in the SQL database
   - Instantly rendered on the page



## Future Improvements

- User authentication system
- Star rating visualization
- Sorting by highest/lowest rating
- Pagination for large datasets
- Cloud deployment (Render / Railway / AWS)

---

## ▶Installation

1. Clone the repository:

2. Navigate into the project folder:

3. Install dependencies:

4. Run the Flask app:

5. Open in browser:

git clone https://github.com/4544545/LocalMatch-FBLC-2026-.git
cd repository-name
pip install -r requirements.txt
python app.py

then open(example of how it should look like)
http://127.0.0.1:5000/
