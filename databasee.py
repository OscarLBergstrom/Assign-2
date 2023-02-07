from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
import pdb


app = Flask(__name__)


app.config["MONGODB_HOST"] = "mongodb+srv://user123:Sommar13@cluster0.r1nafxc.mongodb.net/?retryWrites=true&w=majority"

db = MongoEngine()
db.init_app(app)


class GithubSchema(db.Document):
    commit = db.StringField()
    identifier = db.StringField()
    build_date = db.StringField()
    build_logs = db.StringField()

    def to_json(self):
        return {
            "commit": self.commit,
            "identifier": self.identifier,
            "build_date": self.build_date,
            "build_log": self.build_logs
        }


@app.route('/api/test', methods=['POST', 'GET'])
def db_test():
    if request.method == 'POST':
        try:
            result = GithubSchema(commit="commit1", identifier="id1",
                                  build_date="bd1", build_logs="bl1")
            result.save()
            return make_response("", 201)
        except:
            return make_response("Could not upload to database", 500)

    elif request.method == 'GET':
        result = []
        for obj in GithubSchema.objects:
            result.append(obj)
        return make_response(jsonify(result), 200)


if __name__ == "__main__":
    app.run()
