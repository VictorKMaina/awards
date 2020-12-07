# ![Awards Logo](static/images/logox2.png)
### By Victor K. Maina
## [See it on Heroku](https://dev-awards-ip.herokuapp.com/)
---

This project is an Awwwards clone built with Django. The app allows users to rate developer's websites based on design, usability, and content. Developers can also post new projects on the app.

A running version of this app already deployed on Heroku. [Click here](https://dev-awards-ip.herokuapp.com/) to use it.

## Installation

The following installations instruction are for Ubuntu.

### Setup

To run this application, you will need Python, Git and Postgresql on your system.

```sh
sudo apt install python3 git postgresql
```

Once that is done, clone this repository onto you computer and enter the new directory.

```sh
git clone https://github.com/VictorKMaina/awards
cd awards/
```

### Dependencies

The app requires some dependencies to run. To install them, first create a  virtual environment and activate it.

```sh
python3 -m venv env
source env/bin/activate
```

Then install the dependencies using pip.

```sh
pip install -r requirements.txt
```

### Database

Since the app also needs a database to run, we need to set up Postgres. Postgres will need you to create a username and password to access databases. You can follow the steps [here](https://www.postgresql.org/docs/8.0/sql-createuser.html) to get started.

Once you have a Postgres username, enter Postgres using `psql` on your terminal and create a new database.

```sh
psql
```
```postgres
CREATE DATABASE awards;
```

### Environment Variables

Now that you have a database create, you need to create some environment variables so that Django can use. In the project's root directory, create a `.env` file. Add the following to it, updating it with your own information.

```
SECRET_KEY='<Your Secret Key>'
DEBUG=True
DB_NAME='awards'
DB_USER='<Your Postgres Username>'
DB_PASSWORD='<Your Postgres Password>'
DB_HOST='127.0.0.1'
MODE='dev'
ALLOWED_HOSTS=['*']
DISABLE_COLLECTSTATIC=1
``` 

### Sendgrid

During the login process, the app sends a confirmation email to a new user. For this to work, it needs to be intergrated with Sendgrid. Here are the steps to generating an API key from Sendgrid's documentation.

>1. Sign up for a [SendGrid account](https://signup.sendgrid.com/)
>
>2. Create and store a SendGrid [API key](https://app.sendgrid.com/settings/api_keys) with full access "Mail Send" permissions.
>
>3. Verify your [Sender Identity](https://sendgrid.com/docs/for-developers/sending-email/sender-identity/)

On step 3, use the quick verification method to verify one email address. Remember this address.

Once you have generated your API key, add it to the environment variables, together with your verified email address.

```
SENDGRID_API_KEY='<Your Sendgrid API Key>'
SENDGRID_EMAIL_ADDRESS='<Your verified email address>'
```

### Cloudinary

The app utilizes Cloudinary to store the images that are uploaded. Go to the [Cloudinary documentation](https://cloudinary.com/documentation) to learn how to create an API key.

Once you have your Cloudinary name, API key, and API secret key, add them to the environment variables.

```
CLOUD_NAME='<Your Cloudinary username>'
CLOUDINARY_API_KEY='<Your API key>'
CLOUDINARY_API_SECRET='<Your API secret>'
```

### Migrations

Now that the `.env` file is ready to use, we need to upgrade our database to correspond with the app's models.

```sh
python manage.py migrate
```

## Usage

The app is now ready to run. 

```sh
python managy.py runserver
```

<!-- End of document -->
### External Links

1. [ER Diagram | Google Drive](https://drive.google.com/file/d/1Zy8Uy7HDKKdiol4ryDMCAEBP7PEjcXi0/view?usp=sharing)
2. [Wireframe | Figma](https://www.figma.com/file/Ge25KBxsd1V9fxfIC4fwLW/Awards?node-id=0%3A1)
3. [Awards | Deployed on Heroku](https://dev-awards-ip.herokuapp.com/)

### [LICENSE](/LICENSE)