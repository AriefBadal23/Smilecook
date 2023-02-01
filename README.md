## Smilecook recipe platform

I have created an API for an application named _**Smilecook**_ to share recipes with everyone with your created account. And I created this while reading the book "Python API Development Fundamentals" to improve and better my understanding of REST API's and the way it works with the Flask framework.

The application is deployed on Azure app service 
(http://smilecook.azurewebsites.net/swagger)

**Available Smilecook API Endpoints**
You can find the available endpoints on the swagger endpoint ( /swagger)

The overall strucuture of the project:
![structure of the project](/documentation/project_structure.jpg)


**Migrations**
**Models**
In this folder you can find the models I have used for the Smilecook PostgreSQL database
Which are the recipe and user models.

**Resources**
Because we are using the Flask-RESTfull library which is just an extension of Flask
to setup the routing for the client request we use resourceful routing, which are the main building blocks of the library. Resources are built on top Flask’s pluggable view and are the main building blocks of Flask-RESTfull.


**Schemas**
This folder we use for the data validation by using the Marshmallow library.
With the created schemas it makes sure that for example a username is really a string type by the process of deserialization (which is the recreation of the object from a stream of bytes).

**Static**
In this folder we define our ‘static’ files such as images. This folder contains all the assets (default images), uploaded covers, avatars and recipe images.

**Template**
This folder contains an email HTML template that is being used when a user is signed up on the platform.

**Note:**
The emailadres should by added to the Mailgun portal thats why I provided some
test-accounts to use. After creating a new account a mail will be sent with a activation link which is already been done.

**Test-Accounts**
|Email              | Password | Username |
|-------------------|----------|----------|
|hitej85282@tingn.com| Secret123| Marco    |
|shadowmaster@outlook.com| Secret123| mary |


**Swagger documentation**
The swagger docs is available on the /swagger endpoint


**How to start the application**
* For the database I use PostgreSQL locally

If you want to start the application locally:
1. Open a new terminal in your desired code editor for example VScode.
2. Clone the project with: `git clone https://github.com/AriefBadal23/Smilecook.git`
3. Type the following`pip install -r requirements.txt`

4. Create a database with the name smilecook
5. Setup the credentials for the database, change or add in config.py in DevelopmentConfig() the line:  `SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://username:password@localhost:5432/smilecook"`

6. To migrate the database use `flask db migrate` followed by `flask db upgrade`
7. Check the database for the recipe and user tables if they exists.
8. Again in the terminal type: `py app.py` The application should start.
9. Try to login with one of the test-accounts above to create a new recipe. Do this with the /token endpoint.
10.  If everything went right the recipes should be displayed at the /recipes endpoint.