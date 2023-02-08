from flask import Flask, make_response
from flask import request

app = Flask(__name__)

@app.route('/')
def my_flask_application():
    return 'Welcome to the worlds best CI!! :D'


@app.route('/payload', methods = ["POST"] )
def recieve_post():
    if request.method == 'POST':
        data = request.json
        try:
            repo = data["repository"]
            repo_name = repo["name"]
            ref = data["ref"]
            branch = ref[len("refs/heads/"):len(ref)] # Provides the name of the branch

            for commit in data["commits"]:
                commit_url = commit["url"]
                build(branch, repo_name)
                test(commit_url)
        except:
            response = make_response("Fail")
            response.status_code = 400
            return response

        response = make_response("Success")
        response.status_code = 200
        return response

def build(branch, repo_name):
    pass
def test(data):
    pass  