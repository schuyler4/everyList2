from flask import Flask, Blueprint
#from flask.ext.hashing import Hashing

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "Jfj9u90((fd((0__))fdas"


from route import routes
app.register_blueprint(routes)


if(__name__ == "__main__"):
	app.run()