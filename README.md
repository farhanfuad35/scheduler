## Scheduler

Scheduler is a constraint satisfying scheduling web app implemented using Backtracking Algorithm. Given,
  - Courses to be taken by each faculty
  - Free/available time of each faculty
  - Credits of the courses
This app can generate a single valid weekly routine providing that there exists one. For demo inputs, visit the site and check the sample inputs there.

### Installation
If you want to run the server locally:
  - Make sure you have _python_, _pip_ & _pipenv_ installed on your system.
  - Clone the repo to your project folder.
  - Create a python virtual environment in the project directory <br>
        ```pipenv shell```
  - Install required packages <br>
`pipenv install`
  - Make migrations and migrate <br>
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
  - Run server <br>
  ```python manage.py runserver```

### Technical Details
- **Language:** Python 3.8.5
- **Backend Framework:** Django 3.1.5
- **Frontend:** Bootstrap 4 (Template collected from the web)
