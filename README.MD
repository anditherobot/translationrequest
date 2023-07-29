# Document Translation System - README

This document provides an overview and instructions for using the Document Translation System, a Django-based web application for managing document translation requests. The system allows users to submit translation requests, track their progress, and download translated files. Administrators can manage translation requests, update their status, and notify users when their requests are completed.
Getting Started
Prerequisites

Before running the application, ensure that you have the following installed:

    Python 3.x
    Django (latest version)

Installation

    Clone the repository to your local machine:

bash

git clone https://github.com/your-username/translation-system.git

    Navigate to the project directory:

sql

cd translation-system

    Create a virtual environment (optional but recommended):

bash

python -m venv env

    Activate the virtual environment:

bash

# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate

    Install the required packages:

pip install -r requirements.txt

Database Setup

    Create the initial database schema:

python manage.py migrate

    Create a superuser account for accessing the admin panel:

python manage.py createsuperuser

    Follow the prompts to set a username, email, and password for the superuser.

Running the Application

    Start the development server:

python manage.py runserver

    Access the application in your web browser at http://localhost:8000/.

    Log in using the superuser account to access the admin panel at http://localhost:8000/admin/.

Usage
Admin Panel

    In the admin panel, you can manage clients, translation requests, and client files.
    Clients: View and update client information, translation requests, and uploaded files.
    Translation Requests: Review and update the status of translation requests. Notify users when requests are completed.
    Client Files: View and manage uploaded files associated with translation requests.

    Crendentials: username: transadmin / password: transpassword

Client Dashboard

    Clients can access their dashboard after submitting their information.
    On the dashboard, clients can create new translation requests, track the progress of their requests, and view/download completed translations.
    Clients can also delete uploaded files and submit additional translation requests.

Creating a Translation Request

    Log in as a client or superuser and access the respective dashboard or admin panel.
    Create a new client if you are a superuser or select an existing client if you are a client.
    Click on "Create New Translation Request" to submit a new translation request.
    Provide the source and target languages, additional information, and upload the files to be translated.
    Submit the translation request, and it will be added to the system.

Tracking Progress and Viewing Translations

    Clients can track the progress of their translation requests on their dashboard.
    In the admin panel, the superuser can view the status of all translation requests.
    When a translation request is completed, the client can download the translated files from their dashboard.
    The superuser can also update the status of the translation request and notify the user when the translation is completed.

Customization

You can customize the application by adding more languages, status choices, or additional fields to the models to suit your specific requirements. Feel free to explore the Django documentation for more details on model customization, forms, and templates.
Troubleshooting

If you encounter any issues or have questions, please refer to the project documentation or open an issue on the GitHub repository.
Acknowledgments

Thank you for using the Document Translation System! We hope this application simplifies and enhances your document translation management process. If you have any feedback or suggestions, we would love to hear from you. Happy translating!
