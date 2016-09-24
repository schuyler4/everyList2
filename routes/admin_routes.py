from flask import Blueprint, render_template, request, session, redirect, url_for, flash, session
from models.models import List, List_Item, Comment, User, Idea,db_session
from sqlalchemy import *
from sqlalchemy.orm import *
from flask.views import View, MethodView


admin_routes = Blueprint('admin_routed',__name__)


@admin_routes.route('/admin_signup')
def admin_signup():
	pass

@admin_routes.route('/admin_login')
def admin_login():
	pass


@admin_routes.route('/admin')
def admin():
	pass



