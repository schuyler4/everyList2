from flask import Blueprint, render_template, request, session, redirect, url_for, flash, session
from models import List, List_Item, Comment, db_session

routes = Blueprint('routes', __name__)
@routes.route("/")
def home():
	return render_template('home.html')


@routes.route("/addlist", methods=["GET", "POST"])
def add_list():
	if request.method == "POST":
		print("posting")
		title = request.form["title"]
		description = request.form["description"]
		items = request.form['items']
		new_list = List(title, description)
		new_item = List_Item(items)
		db_session.add(new_list)
		db_session.add(new_item)
		try:
			db_session.commit()
		except Exception as e:
			db_session.rollback()
			db_session.flush()
		return redirect(url_for('routes.add_list'))
	return render_template('add_list.html')


@routes.route("/listoflists", methods=["GET", "POST"])
def list_of_lists():
	all_lists = db_session(List).all()
	return render_template('list_of_lists.html', all_lists = all_lists)


@routes.route("/list/<title>/<id>", methods=["GET" ,"POST"])
def list(title, id):
	pass


@routes.route("/like", methods=["POST"])
def like():
	pass


@routes.route("/dislike", methods=["POST"])
def dislike():
	pass


@routes.route("/login", methods=["GET", "POST"])
def login():
	pass


@routes.route("/signup", methods=["GET", "POST"])
def sign_up():
	pass

