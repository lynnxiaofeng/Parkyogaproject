'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/contexts/

In the terminal, navigate to the project folder just above the miltontours package
Type 'python' to enter the Python interpreter. You should see '>>>'
In Python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit Python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------
# Option 1: Use DB Browser for SQLite
You can enter data directly into the cities or tours table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2023-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from parkyoga import db
from .models import Suburb, Course
import datetime


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
    s1 = Suburb(name='Brisbane City', image='s_brisbanecity.jpg', \
        description='''Brisbane CBD is popular for chain fashion stores and luxe brands on busy Queen Street, plus the shady riverfront City Botanic Gardens. Brisbane City Hall offers historical photos in the Museum of Brisbane, and skyline views from its 1930s Clock Tower. The area is generally quiet at weekends, apart from the waterfront cocktail bars and seafood eateries around Eagle Street Pier, which draw an upmarket crowd.''')
    s2 = Suburb(name='East Brisbane', image='s_eastbrisbane.jpg', \
        description='''East Brisbane is an inner southern suburb of the City of Brisbane, Queensland, Australia. In the 2016 census, East Brisbane had a population of 5,934 people''')
    s3 = Suburb(name='Kangaroo Point', image='s_kangaroopoint.jpg', \
        description='''About Kangaroo Point is an inner southern suburb in the City of Brisbane, Queensland, Australia. In the 2016 census, Kangaroo Point had a population of 8,063 people. The suburb features two prominent attractions, the Story Bridge and Kangaroo Point Cliffs.''')
      
    try:
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()
    except:
        return 'There was an issue adding the suburbs in dbseed function'

    c1 = Course(suburb_id=s1.id, image='c_kidyoga.jpg', price=20.00,\
        date=datetime(2024, 6, 2),\
        name='children yoga in wickham park',\
        description= 'Lone Pine Koala Sanctuary is the world\'s first and largest koala sanctuary and is home to more than 130 koalas. Hand-feed their kangaroos and wild lorikeets, be entertained by a platypus or - best of all - get cuddly with a beautiful koala. Duration 0900-1400 (5hrs), begins at entrance to Koala Plaza') 
    c2 = Course(suburb_id=s1.id, image='c_mindfulyoga.jpg', price=15.00,\
        date=datetime(2024, 6, 3),\
        name='mindful yoga in botanic garden',\
        description= 'Get up close and personal with Australia\'s favourite wildlife and tick two items off your bucket list with a trip to Lone Pine Koala Sanctuary. Lone Pine is only 40 minutes from the CBD by bus and you\'ll be cuddling up to koalas and hand-feeding kangaroos in no time. Don\'t forget the selfie! Duration 0900-1300 (4hrs), begins at entrance to Kanga Plaza.')
    c3 = Course(suburb_id=s2.id, image='c_sunrise.jpg', price=15.50,\
        date=datetime(2024, 6, 4),\
        name='sunrise vin yoga in mowbray park',\
        description= 'You don\'t have to travel to the far north to see Australia\'s bustling reef and sea life. Take a short ferry ride from the Port of Brisbane and you\'ll find yourself at Moreton Island, a tropical sand island with crystal-clear coastal water, lakes and incredible snorkelling at the historic Tangalooma Wrecks. You\'ll want your GoPro to take some incredible underwater snaps. Duration 0900-1700 (8hrs), begins at entrance to Transit Centre.')
    c4 = Course(suburb_id=s2.id, image='c_sunset.jpg', price=15.00,\
        date=datetime(2024, 6, 5),\
        name='sunset hatha yoga in mowbray park',\
        description= 'From June to November, Whale Watching Tours inc. runs daily cruises for those who want to witness the incredible acrobatics of the southern humpback whale. More than 20,000 whales migrate through every winter. Tickets for the five-hour cruise through Moreton Bay are good value and include guaranteed whale sightings. Duration 1300-1800 (5hrs), begins at entrance to Port Street.')                
    c5 = Course(suburb_id=s2.id, image='c_yin.jpg', price=20.00,\
        date=datetime(2024, 6, 6),\
        name='yin yoga in williamnia park',\
        description= 'Forget the outback and take in the green scene. While most international visitors picture red dirt when they think of Australia, you\'re more likely to find yourself surrounded by lush greenery than outback desert. Take the opportunity to check out local fauna and flora at the national parks, as close as 20 minutes from the CBD. Did we mention our parks have drop-bears? Must bring sunblock. Duration 1000-1300 (3hrs), begins at entrance to Forrest Car Park.')
    c6 =  Course(suburb_id=s2.id, image='c_acro.webp', price=20.99,\
        date=datetime(2024, 6, 7),\
        name='acro yoga in gaba park',\
        description= 'The world\'s biggest sand island is just a few hours away. Heritage-listed Big Sandy Island has more than 100 freshwater lakes, pristine water and white-sand beaches. There\'s many ways to explore the island but the most fun is by four-wheel-drive. Join a tour such as the Dingos Resort tag-along four-wheel drive tour, where you can drive yourself and make friends along the way. Duration 0600-1600 (11hrs), begins at entrance to Ferry Road.')
    c7 = Course(suburb_id=s3.id, image='c_weekend.jpg', price=30.00,\
        date=datetime(2024, 6, 8),\
        name='weekend yoga in kangaroo park',\
        description= 'You can\'t come to Australia without enjoying the abundant inland lakes, falls and swimming holes. There\'s almost too many to choose from. Check out Visit our must-swim spots. Duration 0900-1200 (3hrs), begins at entrance to River Park.')
    c8 = Course(suburb_id=s3.id, image='c_partner.jpg', price=30.00,\
        date=datetime(2024, 6, 9),\
        name='partner yoga in kangaroo point park',\
        description= 'Jump on board a CityCat  or ride our private City Cab to explore the city by ferry. CityCats run between the city and various points of interest all the way around to killer bay. Duration 1000-1200 (2hrs), begins at entrance to CBD Ferry Stop.')

    try:
        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)
        db.session.add(c4)
        db.session.add(c5)
        db.session.add(c6)
        db.session.add(c7)
        db.session.add(c8)
        db.session.commit()
    except:
        return 'There was an issue adding a course in dbseed function'

    return 'DATA LOADED'