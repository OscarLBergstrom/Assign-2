from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
from mail import notify_build_test
from build_test import initialization
import requests
from datetime import date

app = Flask(__name__)
ngrok_address = "https://84f3-2001-6b0-1-1041-a45e-8a86-8385-da98.eu.ngrok.io"
app.config["MONGODB_HOST"] = "mongodb+srv://user123:Sommar13@cluster0.r1nafxc.mongodb.net/?retryWrites=true&w=majority"

db = MongoEngine()
db.init_app(app)


class GithubSchema(db.Document):
    commit = db.StringField()
    group = db.StringField()
    build_date = db.StringField()
    log_test = db.StringField()
    log_build = db.StringField()
    log_installation = db.StringField()
    test_logs = db.StringField()

    def to_json(self):
        return {
            "commit": self.commit,
            "group": self.group,
            "build_date": self.build_date,
            "log_test": self.log_test,
            "log_build": self.log_build,
            "log_installation": self.log_installation,
            "test_logs" : self.test_logs
        }


@app.route('/')
def my_flask_application():
    return 'Welcome to the worlds best CI!! :D assadsa'


@app.route('/api/test', methods=['POST', 'GET'])
def db_test():
    if request.method == 'POST':
        try:
            result = GithubSchema(commit=request.get_json(force=True)["commit"], group=request.get_json(force=True)["group"], build_date=request.get_json(force=True)[
                                  "build_date"], log_test=request.get_json(force=True)["log_test"], log_build=request.get_json(force=True)["log_build"], log_installation=request.get_json(force=True)["log_installation"])
            result.save()
            return make_response("", 201)
        except Exception as e:
            make_response(e, 500)

    elif request.method == 'GET':
        result = []
        for obj in GithubSchema.objects:
            result.append(obj)
        return make_response(jsonify(result), 200)


@app.route('/payload', methods=["POST"])
def recieve_post():
    if request.method == 'POST':
        data = request.json
        try:
            repo = data["repository"]
            repo_name = repo["full_name"]
            ref = data["ref"]
            dir = repo["name"]
            # Provides the name of the branch
            branch = ref[len("refs/heads/"):len(ref)]
            config_file = "config.yml"

            for commit in data["commits"]:
                commit_id = commit["id"]
                user_email = commit["author"]["email"]
                results = initialization(repo_name, branch, dir, config_file)
                # save in the database
                try:
                    result = GithubSchema(commit=str(commit_id), group=repo_name, build_date=str(date.today(
                    )), log_test=str(results[0]), log_build=str(results[2]), log_installation=str(results[1]), test_logs=results[3])
                    result.save()
                    print("results2 ", results)
                except Exception as e:
                    print(e)
                # notify user of the result of the testing, compilation and installation
                notify_build_test(user_email, results, commit_id)
        except:

            response = make_response("Fail")
            response.status_code = 400
            return response

        response = make_response("Success")
        response.status_code = 200
        return response


@app.route('/build', methods=["GET"])
def display_builds():
    """
    Displays all the prevoius builds and the links to them
    """
    response = "All builds:\n"

    builds = []
    for obj in GithubSchema.objects:
        builds.append(obj)

    for build in builds:
        build_id = str(build.id)

        response += "Build " + build_id + " can be found at " + \
            ngrok_address + "/build/" + build_id + "<br>"
    return response


@app.route('/build/<id>')
def display_build(id):
    """
    Displays a build and the information about it.
    """
    response = ""
    build = None
    for obj in GithubSchema.objects:
        if str(obj.id) == id:
            build = obj
    if build is not None:
        commit_id = build.commit
        response += "Commit " + commit_id + " was built on: " + build.build_date + "\n"
        response += "The results where: <br>"
        response += "Build: "
        if build.log_build == "0":
            response += "Build successfull"
        else:
            response += "Build failed"
        response += "<br>Installation: "
        if build.log_installation == "0":
            response += "Installation successfull"
        else:
            response += "Installation failed"
        response += "<br>Tests: "
        if build.log_test == "0":
            response += "Tests successfull"
        else:
            response += "Tests failed"
            response +="<br>-------<br>Test logs:<br>"+ build.test_logs +"<br>-------<br>"

    else:
        response += "This build was not found"
    return response


if __name__ == "__main__":
    app.run(debug=True)
