# Assignment 2

A simple CI written in python 3.8.10

## Steps for TA to grade

Steps 1-2 can be followed more thourghly through this [guide](https://phoenixnap.com/kb/install-flask).

1. Install and set up a venv.

2. Install flask.

3. Clone the repo.

4. Make a change on main or assessment, commit & push that change.

5. Check your email connected to your Github account.

6. If you get error 503 it is likely from the server being down, please try again later or ping us on canvas.


## How to install

Steps 1-2 can be followed more thourghly through this [guide](https://phoenixnap.com/kb/install-flask).

1. Install and set up a venv.

2. Install flask.

3. Install ngrok. 

4. run flask on the file Flask_application.

```
flask run
```

5. Take the localhost link given and run it through ngrok with 

```
ngrok http <localhost link>
```

6. Take the ngrok link and add it under Settings -> Webhooks on Github. 
```
<ngroklink>/payload
```

## How to run tests on server

1. Install and set up the server

2. Install and set up a venv.

3. Install flask.

4. Install pytest with

```
pip install -U pytest
```

5. Run the tests with
```
python3 -m pytest
```

# File structure

The server is in the file called server.py. The build and testing part of the CI is in the file build_test.py. The tests are in the folder tests. Test_CI.py tests the entire CI including Server reponses, Building and Testing, and Notifications.

# Statement of contribution

Jacob Trossing has worked on [Issue #5](https://github.com/OscarLBergstrom/Assign-2/issues/5) & [Issue #6](https://github.com/OscarLBergstrom/Assign-2/issues/6).

Filip Wetterdal has worked on [Issue #5](https://github.com/OscarLBergstrom/Assign-2/issues/5) & [Issue #15](https://github.com/OscarLBergstrom/Assign-2/issues/15).

Oscar Bergström has worked on [Issue #3](https://github.com/OscarLBergstrom/Assign-2/issues/3), [Issue #5](https://github.com/OscarLBergstrom/Assign-2/issues/5), [Issue #9](https://github.com/OscarLBergstrom/Assign-2/issues/9) & [Issue #19](https://github.com/OscarLBergstrom/Assign-2/issues/19).

Felipe Oliver has worked on [Issue #1](https://github.com/OscarLBergstrom/Assign-2/issues/1), [Issue #2](https://github.com/OscarLBergstrom/Assign-2/issues/2), [Issue #8](https://github.com/OscarLBergstrom/Assign-2/issues/8), [Issue #12](https://github.com/OscarLBergstrom/Assign-2/issues/12), [Issue #13](https://github.com/OscarLBergstrom/Assign-2/issues/13), [Issue #14](https://github.com/OscarLBergstrom/Assign-2/issues/14) & [Issue #15](https://github.com/OscarLBergstrom/Assign-2/issues/15).

Gustaf Johansson has worked on [Issue #1](https://github.com/OscarLBergstrom/Assign-2/issues/1), [Issue #2](https://github.com/OscarLBergstrom/Assign-2/issues/2), [Issue #8](https://github.com/OscarLBergstrom/Assign-2/issues/8), [Issue #12](https://github.com/OscarLBergstrom/Assign-2/issues/12), [Issue #13](https://github.com/OscarLBergstrom/Assign-2/issues/13), [Issue #14](https://github.com/OscarLBergstrom/Assign-2/issues/14), [Issue #15](https://github.com/OscarLBergstrom/Assign-2/issues/15) & [Issue #18](https://github.com/OscarLBergstrom/Assign-2/issues/18).

# Notifications

The notifications are sent through email when the code is pushed to a Github repo with the CI added to it. In the version control the user can see different versions through an url to a website.

# SEMAT
The current state that the team is in is Collaborating.

The team is working as one cohesive unit. Since the last assignment the team has gotten comfortable working with each other. The team help eachother with issues and asks for assistance  

The communication within the team is open and honest. The slack is a open channel for communication that relates to work or other. The team discussess issues that they have encountered during development. 

The team is focused on achieving the team missions. The team works togheter towards a clear goal of finishing the assignments. 

The team members know and trust each other. Throughout the past weeks the team members have gotten to know each other and trust each others strenghts. 

# What the team has done for P+
For P+ the team has made sure to link all commits to an issue. We have also implemented version control for the CI.
