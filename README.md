# LIT-Revu

Django web application for publishing review requests (tickets), writing
reviews in response, following other users, and browsing a personalized
feed.

## Description

LITRevu is a web application built with Django that allows users to
request and publish book or article reviews, interact with other users
through a following system, and access a personalized content feed.

------------------------------------------------------------------------

## Features

-   User registration, login, and logout
-   Create, update, and delete tickets
-   Create, update, and delete reviews
-   Create a ticket and a review in a single step
-   User following system
-   Personalized feed
-   User search and autocomplete

------------------------------------------------------------------------

## Technologies Used

-   Python
-   Django
-   SQLite
-   HTML / CSS / JavaScript
-   Git / GitHub

------------------------------------------------------------------------

## Project Structure

    src/
        accounts/   # users, authentication, and following system
        tickets/    # tickets [review requests]
        reviews/    # reviews and personalized feed
        templates/  # HTML templates
        static/     # CSS / JavaScript
        LIT_Revu/   # Django project settings
        manage.py   # application entry point
        db.sqlite3  # database
        README.md

------------------------------------------------------------------------

## Local Installation

### 1. Clone the Repository

    git clone https://github.com/mouquettom/lit-revu.git
    cd lit-revu

### 2. Create and Activate a Virtual Environment

#### macOS / Linux

    python3 -m venv .env
    source .env/bin/activate

#### Windows PowerShell

    py -m venv .env
    .env\Scripts\Activate.ps1

### 3. Install Dependencies

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

### 4. Create Migrations and Run the Server

    cd src/
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

------------------------------------------------------------------------

## Additional Information

The project uses a `media/` directory to store images uploaded for
tickets. If the directory does not already exist, it will be created
when the first image is uploaded while creating a ticket.

When a ticket containing an uploaded image is deleted, the associated
image is also removed.

### Useful Command

Create a superuser:

    python manage.py createsuperuser

------------------------------------------------------------------------

## Author

@tom_mouquet

Project developed as part of the OpenClassrooms **Développeur
d'application Python** training program.
