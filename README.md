# Carguessr-PersonalWebsite

Link at carguessr.pythonanywhere.com            Guesstheprice doesn't work (yet)

My personal website is named Carguessr, which houses one fully functional (and one partially functional) minigame centered around scraping data off of the first table of a Wikipedia page and using it to guess the car model corresponding to that data. For instance, some common data points might include the designer of the car, the years of production, or any related/sister cars from a related company. Finally, the last piece of information included is an image of that exact car, scraped from a google images search. Due to the wide variety of Wikipedia car lists, with somewhat arbitrary groupings, it was challenging to find a list of car models without having to contend with another nested list within this list containing links to tangentially related topics. As such, I had to randomly choose from a list of seven Wikipedia car listings (such as List of sports cars), and then choose a car from there, while also avoiding hyperlinks that link to the manufacturer and not the model.

Finding_listings.py-primary script for finding auction listings
Flask_Game.py--contains all of the Flask endpoints and database queries necessary to run the website.
index.html--Carguessr page
pyt_back--primary script for finding Carguessr data

Frameworks/skills used

The website backend was created using the Python micro-framework Flask, which imports another script–the car data gathering script–upon runtime, and passes a JSON dictionary to Javascript using the Jinja2 templating engine. Using this, client-side Javascript code retrieves the JSON object, before parsing it to use in the game. The Flask file also contains all of the endpoints which the website references upon user request, such as the endpoint to log information to the database, or the endpoint to replay the game and gather more car data. The database was created using SQLAlchemy, with bcrypt encryption for passwords, which converts each password to binary when the user passes it into the account creation page. On the client-side, Javascript fetch and async functions communicate with the website backend, and CSS animations are used to modify what a user sees, depending on whether or not they are logged in. They also make the game more visually appealing.

