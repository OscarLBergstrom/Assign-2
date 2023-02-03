# Assignment 2

## How to add the project to GitHub

## How to install

Steps 1-X can be followed more thourghly through this guide.

1. Install and set up a venv.

2. Install flask.

3. Install ngrok. 

4. run flask on the file Flask_application.

```
run flask
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


