# sample-django

This project is created in Python 2.7 and Django 1.11.24 while keeping in mind that it will perform certain operations regarding CustomUser Model and their respective ActivityPeriod Models.

# Problem Statement:
Design and implement a Django application with User and ActivityPeriod models, write
a custom management command to populate the database with some dummy data, and design
an API to serve that data in the json format.

JSON Response:
   ```json
      {
      "ok": true,
      "members": [
        {
          "tz": "Africa/Addis_Ababa",
          "activity_periods": [
        
      ],
      "id": "56398ade-8fac-11ea-9836-b42e99a38ee8",
      "real_name": "rK6I8liqpABK"
    },
    {
      "tz": "Africa/Kinshasa",
      "activity_periods": [
        {
          "start_time": "May 06 2020 08:45 PM",
          "end_time": "May 06 2020 09:23 PM"
        },
        {
          "start_time": "May 06 2020 08:45 PM",
          "end_time": "May 06 2020 09:45 PM"
        }
      ],
      "id": "56db491e-8fac-11ea-bbe7-b42e99a38ee8",
      "real_name": "z1eyL9pEgqSc"
    }
    ]
  }
```


## CustomUser Model:
- **id** (This field will be the primary key for this Model and will store the data in the form of UUID)
- **real_name** (This field value will be a character field with limit 255)
- **tz** (This field value will store TimeZone related value and it will be a character field with limit 32)

## ActivityPeriods Model:
- **user** (This field will be the foreign key for this Model and will be used as reference from CustomUser Model)
- **start_time** (This field value will be a character field with limit 255)
- **end_time** (This field value will be a character field with limit 255)

## ActivityPeriodsManager Manager:
- create_activity_period(user, start_time, end_time)

    This method will fetch the user by providing user_uuid in the form of *str* and stores the information of ActivityPeriod Model in Database.
    
## Available commands:
 This section will list down all the commands which are available in this project.

- create_users

    input
    - total
    
    This command will accept *int* type in *total* which indicates the number of random CustomUsers will be created.
    
    Sample:  
  ```
  python manage.py create_users 10
  ```
  
- create_activity_period_for_custom_user
    
    input
    - user_uuid
    
    This command will be useful to create ActivityPeriod for a particular user by providing user_uuid in the form of *str*.
  
  Sample:  
  ```
  python manage.py create_activity_period_for_custom_user 5566d18f-8fac-11ea-b8f6-b42e99a38ee8
  ```
    
- create_activity_period_for_random_users
    
    input
    - total
    
    This command will accept *int* type in *total* which indicates the number of activity period will be created for random CustomUsers.
    
    Sample:  
  ```
  python manage.py create_activity_period_for_random_users 10
  ```
  
## Available URL requests:

This section will list down all the URL requests which are available in this project.

- /core/health-check
    
    This will provide the health status of the project.
    
    Sample Response:
    ```json
    {
    "Status": true
    }
    
- /core/fetch-data
    
    This will provide all the information regarding all CustomUsers and it's all ActivityPeriods available in the project.
    
    Sample Response:
    ```json
  {
  "ok": true,
  "members": [
    {
      "tz": "Africa/Addis_Ababa",
      "activity_periods": [
        
      ],
      "id": "56398ade-8fac-11ea-9836-b42e99a38ee8",
      "real_name": "rK6I8liqpABK"
    },
    {
      "tz": "Africa/Kinshasa",
      "activity_periods": [
        {
          "start_time": "May 06 2020 08:45 PM",
          "end_time": "May 06 2020 09:23 PM"
        },
        {
          "start_time": "May 06 2020 08:45 PM",
          "end_time": "May 06 2020 09:45 PM"
        }
      ],
      "id": "56db491e-8fac-11ea-bbe7-b42e99a38ee8",
      "real_name": "z1eyL9pEgqSc"
    }
    ]
  }

 ## Hosting
 
 This project can be hosted using many tricks, one of them is shown below.
 
- Hosting on Ubuntu using Gunicorn 19.10.0 without static content
    
    ```
  # To install the latest updates of ubuntu
  $ sudo apt-get update -y
  
  # Installing git for ubuntu
  $ sudo apt-get install -y git
  
  # Installing pip for ubuntu
  $ sudo apt-get install -y python-pip
  
  # Installing the virtualenv using pip
  $ sudo pip install virtualenv
  
  # Creating the virtualenv 
  $ virtualenv /opt/envs/sample-django
  
  # Activating the virtualenv 
  $ source /opt/envs/sample-django/bin/activate
  
  # Clonning the Git repository
  $ git clone https://github.com/tathagatk22/sample-django.git
  
  # Change the directory to BASE_DIR
  $ cd sample-django
  
  # Install all the dependent libraries such as django etc
  $ pip install -r requirements.txt
  
  # This will perform migrations from all the INSTALLED_APPS.
  $ python manage.py migrate 
  
  # This will be used to check the project in development mode.
  $ python manage.py runserver 
  
  # django_sample_project/wsgi.py : by using wsgi(Web Server Gateway Interface) 
  # Gunicorn server has wsgi implemented and 
  # so has our framework(Django), 
  # it means that we can run our app with that server.
  # And the entry point of communication for these two is the variable 
  # application, 
  # which is located in django_sample_project/wsgi.py in our case.
  # --bind : we are binding this project to a specific port 80, 
  # but can be changed as per requirement.
  # --workers : We are providing 3 for the number of workers to serve requests,
  # which we will require probably in real life as our requests increase
  # --daemon : run it in a daemon mode
  
  $ gunicorn --daemon --bind 0.0.0.0:80 --workers 3 django_sample_project.wsgi
  ```
 - Hosting on Docker Containerized platform using uWSGI web server with custom management command to populate the database with some dummy data
    ```
    # Building an Docker image with the tag which includes commit-id 
    # which will be used to maintaining multiple version for docker images.
    $ docker build -t sample-django:$(git rev-parse --short HEAD) -f Dockerfile .

    # Running an Docker image
    $ docker run -itd -p 80:8000 -e DB_Name=$(DB_Name) -e DB_User=$(DB_User) -e DB_Password=$(DB_Password) -e DB_Host=$(DB_Host) -e DB_Port=$(DB_Port) sample-django:$(Tag_Name)

    # Below commands will not create a new container with the application in running state,
    # it will execute and run the commands
    # which will overwrite the existing CMD present in Dockerfile
    # and performs just like a normal command line utility.

    # Populate the database with custom users using Docker command
    $ docker run --rm -e DB_Name=$(DB_Name) -e DB_User=$(DB_User) -e DB_Password=$(DB_Password) -e DB_Host=$(DB_Host) -e DB_Port=$(DB_Port) sample-django:$(Tag_Name) /venv/bin/python manage.py create_users 10

    # Populate the database with custom users using Docker command
    $ docker run --rm -e DB_Name=$(DB_Name) -e DB_User=$(DB_User) -e DB_Password=$(DB_Password) -e DB_Host=$(DB_Host) -e DB_Port=$(DB_Port) sample-django:$(Tag_Name) /venv/bin/python manage.py create_activity_period_for_random_users 10
    ```
 