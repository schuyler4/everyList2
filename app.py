from flask import Flask, Blueprint
#from flask.ext.hashing import Hashing
from flask_alembic import Alembic
from flask_mail import Mail


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "Jfj9u90((fd((0__))fdas"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['WHOOSE_BASE'] = 'sqlite:///data.db'


mail = Mail(app)


from routes.route import routes
app.register_blueprint(routes)
from routes.admin_routes import admin_routes
app.register_blueprint(admin_routes)


if(__name__ == "__main__"):
	app.run()