# FastApi Auth
This POC is an E-commerce apis. This POC includes the following:
  1) user login<br>
  2) user logout<br>
  3) user profile<br>
  4) user ResendOTP<br>
  5) user AddCart<br>
  6) user Addorder<br>
  6) user FindProduct<br>
      

This POC uses tokens for the authentications . <br>
User must login before using profile .
  
# Prerequisites
You will need the following programmes properly installed on your computer.<br>
Python 3.7+

# Installation and Running

clone the repository
```
git clone https://github.com/ongraphpythondev/E-commerce_REST.git
cd E-commerce_REST
```
create a vertual environment
```
python3 -m venv .venv
.venv/bin/activate.bat
```
install required packages
```
pip install -r requirements.txt
```
running
```
python manage.py runserver
```
# Functionalities Included:
  1) user login<br>
  2) user logout<br>
  3) user profile<br>
  4) user ResendOTP<br>
  5) user AddCart<br>
  6) user Addorder<br>
  6) user FindProduct<br>

# Testing:
Profile : http://localhost:8000/account/profile <br>
Login : http://localhost:8000/account/login  <br>
Logout : http://localhost:8000/account/logout  <br>
Resend_otp : http://localhost:8000/account/resend_otp  <br>
Cart : http://localhost:8000/shopping/cart <br>
Order : http://localhost:8000/shopping/order  <br>
Findproduct : http://localhost:8000/shopping/findproduct <br>

# Note 
* Before run add cridentail of twillo in views