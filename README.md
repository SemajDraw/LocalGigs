# LocalGigs

James Ward - C12404762 - Final Year Project


# Set Up
To run the project the django__api application needs to be run with the following command, after navigating to the folder.
	### python manage.py runserver 127.0.0.0:8000

Then the recommender needs to be run by navigating to the folder and running
	### python manage.py runserver 127.0.0.0:8001

The get_artist_recommendations method in the ticketmaster.py file also needs to be modified to point to the correct IP address

When both applications are running, in another terminal navigate to the django__api folder and run the following command
	### python manage.py process_tasks


# django__api Back-End / Front-End 

# /app
Folder -  contains the app application

  ## /migrations
  This folder contains all database migration files

  ## /tests
  Folder - contains all test files for app application

    ### test_models.py
    File - contains tests for the models

    ### test_urls.py
    File - contains tests for the urls

    ### test_views.py
    File - contains tests for the views

  ### adapter.py
  File - creates the link between the users email and their Facebook account.

  ### admin.py
  File - contains code to register new models with Django admin so they appear in the admin console

  ### forms.py
  File - contains a number of Django forms that are used to pass data from the templates to the views.

  ### models.py
  File - contains the code to create the user profile model and the triggers to create is when a user creates a new account.

  ### views.py
  File - contains the bulk of the business logic for the app section of the app.

  ### urls.py
  File -  contains all urls for the front end



# /api

  ## /tests
  Folder - contains all test files for app application

    ### test_models.py
    File - contains tests for the models

    ### test_urls.py
    File - contains tests for the urls

    ### test_views.py
    File - contains tests for the views

  ### forms.py
  File - contains a number of Django forms that are used to pass data from the templates to the views.

  ### serializers.py
  File - contains methods that put data from API calls in to the correct format so it can be used to perform CRUD operations on the database or used for some other business logic purpose.

  ### spotify.py
  File - contains all business logic regarding the Spotify API

  ### spotify.py
  File - contains all business logic regarding the Ticketmaster API

  ### views.py
  File - contains the bulk of the business logic for the api section for the app.

  ### urls.py
  File -  contains all urls for the API functionality


# django_api

  ### settings.py
  File -  contains all the configurations for the app

  ### urls.py
  File -  contains all the base urls for the app


## GeoLite2
  Geolocation library

## media
  Folder - contains folders of all static images and icons for the application

## static
  Folder - contains folders of all CSS and JS files

## templates
  Folder - contains folders of all HTML templates

### crontab
  File - initializes cron job on linux machine

### Dockerfile
  This file contains all of the configurations for the Docker container.

### entry.sh
  File - script to run cron job on server

### requirements.txt
  This file is generated when the command pip freeze is run, it extracts all of the dependencies for the project and stores them on this file which is then used when creating the Docker image to install all of the dependencies on the container and in the app.

### start_app.sh
  File - entrypoint script to run server



# Recommender

## api/

  ### pre_processing.py
  File - handles the cleaning and preparation of the data recieved from the back-end

  ### recommendation.py
  File - performs the recommendations

  ### urls.py
  File - contains the urls for the recommender

  ### views.py
  File - contains business logic for the recommender

# django_api

  ### settings.py
  File -  contains all the configurations for the recommender

  ### urls.py
  File -  contains all the base urls for the recommender

### Dockerfile
  This file contains all of the configurations for the Docker container.

### requirements.txt
  This file is generated when the command pip freeze is run, it extracts all of the dependencies for the project and stores them on this file which is then used when creating the Docker image to install all of the dependencies on the container and in the app.



# Mobile

# /src

  ## /app
    
    ### app.component.ts
    File - initializes the application

    ### app.html
    File - contains the link to the root HTML page tabs.html

    ### app.module.ts
    File - modules and packages for the application are included here

    ### app.scss
    File - SCSS style file

    ### app.main.ts
    File - bootstraps the application

  ## /assets
    Folder - contains folders containing static images for the application
    
 ## /pages
    Folder - contains all application pages

    ### /login   
      ### login.html
      File - html for login screen

      ### login.module.ts
      File - loads login screen

      ### login.scss
      File - contains the style sheet for the login page.

      ### login.ts
      File - contains the funcitonality for the login page.

    ### /map
      ### map.html
      File - html for map screen

      ### map.scss
      File - contains the style sheet for the map page.

      ### map.ts
      File - contains the funcitonality for the map page.

    ### /profile 
      ### profile.html
      File - html for profile screen

      ### profile.scss
      File - contains the style sheet for the profile page.

      ### profile.ts
      File - contains the funcitonality for the profile page.

    ### /search
      ### search.html
      File - html for search screen

      ### search.scss
      File - contains the style sheet for the search page.

      ### search.ts
      File - contains the funcitonality for the search page.

    ### /signup 
      ### signup.html
      File - html for signup screen

      ### signup.scss
      File - contains the style sheet for the signup page.

      ### signup.ts
      File - contains the funcitonality for the signup page.

    ### /tabs
      ### tabs.html
      File - contains the layout for the navigation tabs

      ### search.ts
      File - contains the funcitonality for tab ordering and navigation.

  ## /providers

    ### /rest
      ### rest.ts
      File - handles all connectivity to the Back_End of the Web application

  ### index.html
  File - the base template all other pages are rendered in



# BasicRecommender

  ## Dataset
  Folder - contains a number of datasets used throughout testing and development

  ## Evaluation
  Folder - contains a number of early testing files used for evaluating algorithms

  ## Models
  Folder - contains different versions of the models serialized and stored at different epoch levels

  ## Preprocessing
  Folder - contains several data cleaning and preparation files

  ## Recommender 
  Folder - contains the initial recommender construction and tesing and plotting files
