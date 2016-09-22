from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import func


Base = declarative_base()
engine = create_engine('sqlite:///data.db', echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()


class List(Base):
	id = Column('list_id', Integer, primary_key=True)
	title = Column(String(50))
	description = Column(String(500))
	items = relationship("List_Item", backref="List")
	comments = relationship("Comments", backref="List")
	__tablename__ = "List"

	def __init__(self, title, description):
		self.title = title
		self.description = description


class List_Item(Base):
	list_id = Column(Integer, ForeignKey(List.id), primary_key=True)
	content = Column(String(50))
	list = relationship("List", cascade="all,delete", backref="List_Item")
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

print ("created all")
Base.metadata.create_all(engine)