from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
from mail import notify_build_test
from build_test import initialization

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


@app.route('/')
def my_flask_application():
    return 'Welcome to the worlds best CI!! :D'


@app.route('/payload', methods=["POST"])
def recieve_post():
    if request.method == 'POST':
        data = request.json
        try:
            repo = data["repository"]
            repo_name = repo["full_name"]
            # print(repo_name)
            ref = data["ref"]
            dir = repo["name"]
            # print(dir)
            # Provides the name of the branch
            branch = ref[len("refs/heads/"):len(ref)]
            config_file = "config.yml"

            for commit in data["commits"]:
                commit_id = commit["id"]
                #commit_url = commit["url"]
                user_email = commit["author"]["email"]
                # print(user_email)
                result = initialization(repo_name, branch, dir, config_file)
                # print(result)
                notify_build_test(user_email, result, commit_id)
        except:

            response = make_response("Fail")
            response.status_code = 400
            return response

        response = make_response("Success")
        response.status_code = 200
        return response


if __name__ == "__main__":
    app.run()


def build(branch, repo_name):
    pass


def test(data):
    pass
