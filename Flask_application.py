from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine

app = Flask(__name__)

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

    def to_json(self):
        return {
            "commit": self.commit,
            "group": self.group,
            "build_date": self.build_date,
            "log_test": self.log_test,
            "log_build": self.log_build,
            "log_installation": self.log_installation
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
            repo_name = repo["name"]
            ref = data["ref"]
            # Provides the name of the branch
            branch = ref[len("refs/heads/"):len(ref)]

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


@app.route('/build', methods=["GET"])
def display_builds():
    """
    Displays all the prevoius builds and the links to them
    """
    response = "All builds:\n"

    builds = []
    for obj in GithubSchema.objects:
        builds.append(obj)
    builds = jsonify(builds)

    for build in builds:
        response += "Build " + build["_id"]["$oid"] + " can be found at " + ngrok_address+ "/commits/" + build["_id"]["$oid"] +"\n"
    return response


@app.route('/build/<id>')
def display_build(id):
    """
    Displays a build and the information about it.
    """
    response = ""
    build = None
    for obj in GithubSchema.objects:
        if obj["_id"]["$oid"] == id:
            build = obj
    build = jsonify(build)
    if build is not None:
        commit_id = build["commit"]
        response += "Commit " + commit_id + " was built on: " + build["build_date"] + "\n"
        response += "The results where: \n"
        response += "Build: "
        if build["log_build"]=="0":
            response += "Build successfull"
        else:
            response += "Build failed"
        response += "\nInstallation: "
        if build["log_installation"]=="0":
            response += "Installation successfull"
        else:
            response += "Installation failed"
        response += "\nTests: "
        if build["log_test"]=="0":
            response += "Tests successfull"
        else:
            response += "Tests failed"
    else:
        respose += "This build was not found"
    return response

if __name__ == "__main__":
    app.run(debug=True)


def build(branch, repo_name):
    pass


def test(data):
    pass
