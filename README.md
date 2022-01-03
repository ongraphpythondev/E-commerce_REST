Ecommerce Project
This POC we create Ecommerce Rest_APIs . This POC includes the following:

User authentication with message
Buy products 
Cart and order

This POC uses apis provided by Twilio free account.

Prerequisites
You will need the following programmes properly installed on your computer.
Python 3.7+

Installation and Running
clone the repository

git clone https://github.com/Ritesh1200/ongraph_project1.git
cd ongraph_project1
create a vertual environment

python3 -m venv .venv
.venv\Scripts\activate.bat
install required packages

pip install -r requirements.txt
running

python manage.py runserver
Note
Before running the the django project:

Functionalities Included:
User authentication with mobile messaging
User See all the products
User search products by name
User add to cart the products
User order them 

Testing:
login/authentication : http://127.0.0.1:8000/shopping/login --- must login once before testing any other apis
cart : http://127.0.0.1:8000/shopping/cart
Add to cart : http://127.0.0.1:8000/shopping/addcart/id
order : http://127.0.0.1:8000/zoom/shopping/order
add to order : http://127.0.0.1:8000/zoom/shopping/addorder/id
products : http://127.0.0.1:8000/zoom/shopping/product
