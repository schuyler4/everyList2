from flask import Blueprint, render_template, request, session, redirect, url_for, flash, session
from models import List, List_Item, Comment, User, db_session
from sqlalchemy import *
from sqlalchemy.orm import *

routes = Blueprint('routes', __name__)
@routes.route("/")
def home():
	return render_template('home.html')


@routes.route("/addlist", methods=["GET", "POST"])
def add_list():
	if request.method == "POST":
		title = request.form["title"]
		description = request.form["about"]
		items = request.form['items']
		print items
		new_list = List(title, description, 0)
		new_items = List_Item(items)
		new_list.items.append(new_items)
		db_session.add(new_list)
		db_session.add(new_items)
		try:
			db_session.commit()
		except Exception as e:
			print(e)
			db_session.rollback()
			db_session.flush()
		return "sucksess"
	return render_template('add_list.html')


@routes.route("/listoflists", methods=["GET", "POST"])
def list_of_lists():
	all_lists = db_session.query(List).all()
	print(all_lists)
	return render_template('list_of_lists.html', all_lists = all_lists)


@routes.route("/list/<title>/<id>", methods=["GET" ,"POST"])
def list(title, id):
	list = db_session.query(List).filter(List.title == title, List.id == id).first()
	list_items = db_session.query(List).filter(List.title == title, List.id == id).options(lazyload('items')).all()
	print "panda"
	list.items.content
	print "panda"
	return render_template('list.html', list=list, items=list_items)

@routes.route("/like", methods=["POST"])
def like():
	pass


@routes.route("/dislike", methods=["POST"])
def dislike():
	pass


@routes.route("/signup", methods=["GET", "POST"])
def sign_up():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		existing_user = db_session.query(User).filter(User.username == username).first()
		if existing_user:
			flash("someone has alreay used that username try again")
			return redirect(url_for('routes.sign_up'))
		else:
			new_user = User(username, password)
			db_session.add(new_user)
			try:
				db_session.commit()
				session['logged_in'] = True
			except Exception as e:
				db_session.rollback()
				db_session.flush()
				print "error"
			return redirect(url_for('routes.home'))
	return render_template('signup.html')


@routes.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		user = db_session.query(User).filter(User.username == username, User.password == password).first()
		if user:
			return redirect(url_for('routes.home'))
			session["logged_in"] = True
		else:
			return redirect(url_for('routes.login'))
			flash("your username or password wash entered incorectly")
	return render_template('login.html')


@routes.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('routes.home'))


@routes.route("/deleteitems/<title>/<id>")
def delete_items(title, id):
	pass
