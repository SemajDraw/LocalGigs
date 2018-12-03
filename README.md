# LocalGigs

James Ward - C12404762 - Final Year Project

# Django API

## /app

### adapter.py

This file creates the link between the users email and their Facebook account.

### forms.py

This file contains a number of Django forms that are used to pass data from the templates to the views.

### models.py

This file contains the code to create the user profile model and the triggers to create is when a user creates a new account.

### views.py

This file contains the bulk of the business logic for the app section of the app.

## /api

### forms.py

This file contains a number of Django forms that are used to pass data from the templates to the views.

### views.py

This file contains the bulk of the business logic for the api section for the app.

### serializers.py

This file contains methods that put data from API calls in to the correct format so it can be used to perform CRUD operations on the database or used for some other business logic purpose.

### Dockerfile

This file contains all of the configurations for the Docker container.

### requirements.txt

This file is generated when the command pip freeze is run, it extracts all of the dependencies for the project and stores them on this file which is then used when creating the Docker image to install all of the dependencies on the container and in the app.

# Ionic app

## /src

### login.ts

This file contains the funcitonality for the login page.

### signup.ts

This file contains the funcitonality for the signup page.

### home.ts

This file contains the funcitonality for the home page.

### contact.ts

This file contains the funcitonality for the contact page.

### abput.ts

This file contains the funcitonality for the about page.

## / providers

### rest.ts

This file provides all of the functionality for any REST services required by the app.