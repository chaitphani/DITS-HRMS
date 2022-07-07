# DITS-HRMS

# SETUP of the Project(for windows)

-- clone this repo, jump into the repo directory and start 
    with below mentioned commands:

> python -m venv (env_name) -> creates virtualenv

> venv/Scripts/activate -> to activate the vitualenv

> pip install -r requirements.txt -> to install all the dependencies from requirements.txt

> python manage.py runserver -> to run the local server at http://localhost:8000/


-- WORKING WITH PORTAL:
before starting the local server try with below mentioned command:

> python manage.py createsuperuser

with the above create an admin user with the details.

after login with the above credentails, can able to create the staff users inside the portal.

more over, this portal is provided with reset password even.


-- PURPOSE OF THE PORTAL:
1. With this portal, one can add and follow with different project at a time.
2. Can include staff users with the relevant project and can work on the project.
3. Can add/update the task and issue within project.
4. Assigned user can provide comments within each task or issue(kind of chatting with others)
5. Included with notification service for any mentions and task assignments.
6. Staff can add their attendance and request leaves and only admin can check with attendance and leaves and he can approve/keep on hold/reject.


Thanks for using this portal.
