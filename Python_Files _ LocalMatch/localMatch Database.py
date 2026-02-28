import sqlite3

connection = sqlite3.connect('localMatch.db')
cursor = connection.cursor()

# Wipe old tables so data doesn't duplicate on multiple runs 
cursor.execute('DROP TABLE IF EXISTS Favorites')
cursor.execute('DROP TABLE IF EXISTS Reviews')
cursor.execute('DROP TABLE IF EXISTS Business')

# Create Business table
cursor.execute('''
    CREATE TABLE Business (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Type TEXT,
        ActiveDeals TEXT,
        Rating REAL,
        ReviewCount INTEGER,
        Location TEXT,
        Latitude REAL,
        Longitude REAL
    )
''')

# Insert 10 businesses
businesses = [
    ('SummitBuild Contractors', 'Construction', 'Free project estimates', 4.1, 52, 'Brampton, 4722 Wisteria Lane', 43.685096740722656, -79.75885772705078),
    ('PrimeCare Home Services', 'Home Services', 'Winter maintenance discount', 3.8, 41, 'Brampton, 189 Blue Heron Drive', 43.812523, -79.680081),
    ('Maple Leaf Roofing', 'Construction', 'No deals at the moment', 4.2, 48, 'Mississauga 904 Jasper Court', 43.802612, -79.560701),
    ('Bright Minds Tutoring', 'Education', 'First session free', 4.7, 132, 'Brampton 55 Copperhead Road', 43.688853, -79.671848),
    ('Pulse Fitness Studio', 'Fitness', 'Student membership deal', 4.5, 89, 'Vaughan 12321 Sycamore Terrace', 43.653093, -79.658126),
    ('Urban Bites Cafe', 'Food & Beverage', 'No deals at the moment', 4.1, 214, 'Toronto 8870 Marigold Way', 43.665016, -79.564817),
    ('TechFix Solutions', 'Technology Repair', 'Free diagnostics', 4.6, 167, 'Brampton 14 Shadow Ridge Pass', 43.696797, -79.782994),
    ('GreenScape Lawn Care', 'Landscaping', 'Spring cleanup deal', 4.0, 73, 'Caledon 602 East Windmill Blvd', 43.649119, -79.751434),
    ('NorthStar Auto Repair', 'Automotive', 'No deals at the moment', 4.3, 156, 'Mississauga 21 Baker Hollow', 43.712681, -79.787111),
    ('Harmony Wellness Clinic', 'Health & Wellness', 'New client promo', 4.8, 201, 'Toronto 3390 Ironwood Circle', 43.775184, -79.695175)
]
cursor.executemany(
    "INSERT INTO Business (Name, Type, ActiveDeals, Rating, ReviewCount, Location, Latitude, Longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    businesses
)

# Create Reviews table
cursor.execute('''
    CREATE TABLE Reviews (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BusinessID INTEGER,
        ReviewText TEXT,
        Rating REAL,
        FOREIGN KEY (BusinessID) REFERENCES Business(ID)
    )
''')

# Insert sample reviews (match IDs 1 through 10)
reviews_data = [
    (1, "Reliable and professional team.", 4.3),
    (1, "Finished the project on time.", 4.5),
    (1, "Good quality work, a bit pricey.", 4.0),

    (2, "Friendly staff and quick service.", 4.1),
    (2, "Affordable but not always punctual.", 3.8),
    (2, "Excellent winter maintenance service.", 4.3),

    (3, "Roof repair done efficiently.", 4.6),
    (3, "Professional and experienced team.", 4.4),
    (3, "Good quality materials.", 4.3),

    (4, "Excellent tutors, very patient.", 4.8),
    (4, "Helped me improve my grades.", 4.7),
    (4, "Flexible scheduling.", 4.6),

    (5, "Clean facilities and good equipment.", 4.5),
    (5, "Friendly trainers.", 4.6),
    (5, "Great student discounts.", 4.4),

    (6, "Delicious food and coffee.", 4.3),
    (6, "Cozy atmosphere.", 4.4),
    (6, "Friendly staff.", 4.5),

    (7, "Fixed my laptop quickly.", 4.6),
    (7, "Great customer service.", 4.7),
    (7, "Reasonable pricing.", 4.5),

    (8, "Beautiful landscaping work.", 4.3),
    (8, "Reliable and punctual team.", 4.2),
    (8, "Good seasonal offers.", 4.1),

    (9, "Quick and reliable service.", 4.5),
    (9, "Good pricing for oil changes.", 4.4),
    (9, "Friendly mechanics.", 4.3),

    (10, "Excellent care and attention.", 4.8),
    (10, "Friendly and knowledgeable staff.", 4.9),
    (10, "Clean and welcoming environment.", 4.7)
]
cursor.executemany(
    "INSERT INTO Reviews (BusinessID, ReviewText, Rating) VALUES (?, ?, ?)",
    reviews_data
)

# Create Favorites table
cursor.execute('''
    CREATE TABLE Favorites (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BusinessID INTEGER UNIQUE,
        FOREIGN KEY (BusinessID) REFERENCES Business(ID)
    )
''')

connection.commit()
connection.close()
print("Database complete")