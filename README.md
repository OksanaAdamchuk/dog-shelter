# Dog Shelter

The Dog Shelter is a web application built using Python Django that helps the administration of the dog shelter search for permanent or temporary adopters for dogs. After the login process, users of the web application can choose as many dogs as they want to take care of temporarily, and one dog can be chosen by many users.

## Check it out!

[Dog Shelter project deployed to Render](https://dog-shelter-1m73.onrender.com)

## Getting started

Python3 must be already installed. 

```shell
git clone https://github.com/OksanaAdamchuk/dog-shelter.git
cd dog-shelter
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver  # starts Django Server
```

Now you can open the application in your web browser: http://localhost:8000/

To receive access to all pages you can use test user credentials:

username: TestUser

password: 987@Password

## Features

* Dog Database: Keep records of all dogs in the shelter, including their names, ages, breeds, and vaccination records.
* User Roles: Admins and vusers have different levels of access to the system.
* Authentication and Authorization: Secure login and permissions ensure data privacy.
* Search and Filtering: Easily find dogs based on specific criteria like name or breed.
* Vaccination Tracking: Keep track of vaccination status for each dog.
* Caretakers Tracking: You can see how many people wants to take care of some dog temporarily. 
