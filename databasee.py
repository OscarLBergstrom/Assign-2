from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
import pdb


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


if __name__ == "__main__":
    app.run()
