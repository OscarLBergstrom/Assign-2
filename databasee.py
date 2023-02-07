from flask import Flask, make_response
from flask_mongoengine import MongoEngine


app = Flask(__name__)
db = MongoEngine()
db.init_app(app)

app.config["MONGODB_HOST"] = "mongodb+srv://user123:Sommar13@cluster0.r1nafxc.mongodb.net/?retryWrites=true&w=majority"


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


@app.route('/api/test', methods=['POST'])
def db_test():
    result = GithubSchema(commit="commit1", identifier="id1",
                          build_date="bd1", build_logs="bl1")
    result.save()
    return make_response("", 201)


if __name__ == "__main__":
    app.run()
