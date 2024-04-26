Commerce project - Auction application  
The commerce directory contains the main project-level configurations, such as settings, URL configurations, and ASGI/WSGI configurations  
Default SQL used by Django: Default SQLite database file

Auction App
The auctions app contains the main functionality of the e-commerce auction application.  
It includes templates, models, forms, views, and URL configurations specific to the auction features.  
This is a web application for an auction platform where users can create listings, place bids, and interact with auction listings.  

Features

User registration and authentication  
Create and manage auction listings  
Place bids on auction listings  
Update current bid for a listing  
Search for listings  
Identify the highest bidder for a listing  
Add listings to a watchlist  
Leave comments on auction listings  

Technologies Used  

Django web framework (Models, Views, Templates)  
Python programming language  
Django Templating language, HTML, CSS (powered by bootstrap) for the frontend  
Django's built-in testing framework  

Project Structure  

auctions/: Auctions Django app directory  

models.py: Contains the database models  
views.py: Contains the view functions  
urls.py: Defines the URL patterns for the app  
forms.py: Contains the form classes  
tests.py: Contains the test cases for the app  
templates/: Directory for HTML templates  
static/: Directory for static files (CSS, JavaScript, images)  

Commerce/:  
manage.py: Django management script  

Setup and Installation  

Clone the repository:  
git clone https://github.sydney.edu.au/INFO1111-2024/Self-Learning-Project-Django-Shermaine-Ng  

Navigate to the location of the cloned repository:  
cd location  

Command to make migrations if needed:  
python3 manage.py makemigrations  

Command to apply database migrations if needed:  
python3 manage.py migrate  

Run the development surver:  
python3 manage.py runserver  

Access application in web browser at:  
http://localhost:8000 mine was http://127.0.0.1:8000/  

To access the admin page of the auctions application visit:  
http://localhost:8000 mine was http://127.0.0.1:8000/admin/  

To create a super user account to access admin page:  
1. python3 manage.py createsuperuser  
2. enter the fields as prompted by the terminal  
3. access the admin page of the auctions application visit: http://localhost:8000 mine was http://127.0.0.1:8000/admin/  


Command to run tests in auctions/tests.py:  
python3 manage.py test  



