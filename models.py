from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()
engine = create_engine('sqlite:///data.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()
metadata = MetaData()

class List(Base):
	id = Column('list_id', Integer, primary_key=True)
	title = Column(String(50))
	description = Column(String(500))
	items = relationship("List_Item", backref="List")
	comments = relationship("Comment", backref="List")
	popularity = Column(Integer)
	__tablename__ = "List"

	def __init__(self, title, description, popularity):
		self.title = title
		self.description = description
		self.popularity = 0


class List_Item(Base):
	list_id = Column(Integer, ForeignKey(List.id), primary_key=True)
	content = Column(String(50))
	list = relationship("List", cascade="all, delete-orphan", backref="List_Item", single_parent=True)
	__tablename__ = "List_Item"

	def __init__(self, content):
		self.content = content


class Comment(Base):
	list_id = Column(Integer, ForeignKey(List.id), primary_key=True)
	name = Column(String(50))
	content = Column(String(300))
	list = relationship("List", cascade="all,delete", backref="Comment")
	__tablename__ = "Comment"

	def __init__(self, name, content):
		self.name = name
		self.content = content


class User(Base):
	id = Column(Integer, primary_key=True)
	username = Column(String(50))
	password = Column(String(50))
	__tablename__ = "User"

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)


class Idea(Base):
	id = Column(Integer, primary_key=True)
	title = Column(String(50))
	content = Column(String)
	__tablename__ = "Idea"

	def __init__(self, title, content):
		self.title = title
		self.content = content

Base.metadata.create_all(engine)