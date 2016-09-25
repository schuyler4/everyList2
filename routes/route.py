from flask import Blueprint, render_template, request, session, redirect, url_for, flash, session
from models.models import List, List_Item, Comment, User, Idea,db_session
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_mail import Message


routes = Blueprint('routes', __name__)
@routes.route("/")
def home():
	lists = db_session.query(List).limit(10).all()
	return render_template('home.html', lists=lists)


@routes.route("/idea", methods=["POST"])
def idea():
	title = request.form["title"]
	content = request.form["content"]
	new_idea = Idea(title, content)
	if new_idea.title and new_idea.content:
		db_session.add(new_idea)
		try: 
			db_session.commit()
			return redirect(url_for('routes.home'))
		except Exception as e:
			print(e)
			db_session.rollback()
			db_session.flush()
			flash("something whent wrong")
			return redirect(url_for('routes.home'))
	else:
		flash("are you sure you filled in all the fields")
		return redirect(url_for('routes.home'))


@routes.route("/addlist", methods=["GET", "POST"])
def add_list():
	if request.method == "POST":

		title = request.form["title"]
		description = request.form["about"]
		new_list = List(title, description)

		list_items = request.form.getlist('items')

		for item in list_items:
			print(item)
			new_items = List_Item(item)
			db_session.add(new_items)
			new_list.items.append(new_items)
		print("panda")

		db_session.add(new_list)

		items_created = False
		list_created = False

		if new_list.title and new_list.description:
			list_created = True
		else:
			flash("your list must have a title and a desciption")
		if new_items.content:
			list_items = True
		else:
			flash("your list must have some items")
			
		if list_created and items_created:
			try:
				db_session.commit()
				print("pandas are awsome")
			except Exception as e:
				print(e)
				db_session.rollback()
				db_session.flush()

		created_list = db_session.query(List).filter(List.title == title).first()
		redirect_id = created_list.id
		redirect_title = created_list.title
		return redirect(url_for('routes.list', title=redirect_title, id=redirect_id))
	return render_template('add_list.html')


@routes.route("/listoflists", methods=["GET", "POST"])
def list_of_lists():

	searched = False
	search = None

	if request.method == "POST":
		search = request.form['search']
		all_lists = db_session.query(List).filter(List.title == search).all()
		print(all_lists)
		return render_template('list_of_lists.html', all_lists = all_lists)

	all_lists = db_session.query(List).all()
	return render_template('list_of_lists.html', all_lists = all_lists)


@routes.route("/list/<title>/<id>", methods=["GET" ,"POST"])
def list(title, id):
	list = db_session.query(List).filter(List.title == title, List.id == id).first()
	list_items = db_session.query(List_Item).filter(List_Item.list_id == list.id).all()
	return render_template('list.html', list=list, items=list_items)


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
				print ("error")
			return redirect(url_for('routes.home'))
		msg = Message("Hello Email World",
						sender="marek.s.newton@gmail.com",
						recipients=["marek.s.newton@gmail.com"])
		mail.send(msg)

	return render_template('signup.html')


@routes.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		user = db_session.query(User).filter(User.username == username, User.password == password).first()
		if user:
			session['logged_in'] = True
			return redirect(url_for('routes.home'))
		else:
			return redirect(url_for('routes.login'))
			flash("your username or password wash entered incorectly")
	return render_template('login.html')


@routes.route("/logout")
def logout():
	session['logged_in'] = False
	return redirect(url_for('routes.home'))


@routes.route("/deleteitems/<title>/<id>", methods=['GET', 'POST'])
def delete_items(title, id):
	list = db_session.query(List).filter(List.title == title, List.id == id).first()
	if request.method == "POST":
		item = request.form['item']
		delete_item = db_session.query(List_Item).filter(List_Item.content == item, List_Item.list_id == list.id).first()
		if delete_item:
			db_session.delete(delete_item)
			try:
				db_session.commit()
			except Exception as e:
				db_session.rollback()
				db_session.flush()
				print("error")
				flash("an error ocured delting this item")
				return redirect(url_for('routes.delete_items', title=list.title, id=list.id))
		else:
			flash("this is not an item on this list")
			return redirect(url_for('routes.delete_items', title=list.title, id=list.id))
		return redirect(url_for('routes.list', title=list.title, id=list.id))
	if session.get('logged_in') == False:
		return redirect(url_for('routes.login'))
	if not list:
		return redirect(url_for('routes.list_of_lists'))
	items = db_session.query(List_Item).filter(List_Item.list_id == id).all()
	list = db_session.query(List).filter(List.id == id).first()
	return render_template('editlist.html', items = items, list=list)