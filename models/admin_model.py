from sqlalchemy import *
from models import Base

class Admin_Password(Base):
	id = Column('admin_password_id',Integer, primary_key=True)
	password = Column(String(50))
	__tablename__ = "Admin_Password"

	def __init__(self, password):
		self.password = password

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)


class Admin_Acount(Base):
	id = Column('admin_acount_id', Integer, primary_key=True)
	username = Column(String(50))
	password = Column(String(50))
	rank = Column(Integer)

	def __init__(self, username, password, rank):
		self.username = username
		self.password = password
		self.rank = 1

	def set_password(self, password):
		self.pw_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

