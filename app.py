from flask import Flask, Blueprint


app = Flask(__name__)
app.config['DEBUG'] = True


from route import routes
app.register_blueprint(routes)


if(__name__ == "__main__"):
	app.run()