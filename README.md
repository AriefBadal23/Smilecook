## Smilecook recipe platform

I have created an API for an application named _**Smilecook**_ to share recipes with everyone with your created account. And I created this while reading the book "Python API Development Fundamentals" to improve and better my understanding of REST API's and the way it works with the Flask framework.

To test the backend of the application you can use Postman
For the database. I'm running PostgreSql locally. 


**Available Smilecook API Endpoints**
|Endpoint              |HTTP method |   |
|-------------------|----------|----------|
|/recipes|GET | Get all the recipes   |
|/recipes|POST |Create a recipe  |

The overall strucuture of the project:
![structure of the project](/Chapter_2/smilecook/documentation/project_structure.jpg)


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
test-accounts to use.

**Test-Accounts**
|Email              | Password | Username |
|-------------------|----------|----------|
|hitej85282@tingn.com| Secret123| Marco    |
|shadowmaster@outlook.com| Secret123| mary |


**Swagger documentation**
The swagger docs is available on the /swagger endpoint

**Deployment**
Currently deployed on Azure Web services:
[Smilecook](http://smilecook.azurewebsites.net)