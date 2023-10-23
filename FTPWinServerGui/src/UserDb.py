# Copyright © 2023 Kalynovsky Valentin. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	home_dir = Column(String)
	permission_CWD = Column(Boolean)  # change directory (CWD, CDUP commands)
	permission_LIST = Column(Boolean)  # list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
	permission_RETR = Column(Boolean)  # retrieve file from the server (RETR command)
	permission_APPE = Column(Boolean)  # append data to an existing file (APPE command)
	permission_DELE = Column(Boolean)  # delete file or directory (DELE, RMD commands)
	permission_RNFR = Column(Boolean)  # rename file or directory (RNFR, RNTO commands)
	permission_MKD = Column(Boolean)  # create directory (MKD command)
	permission_STOR = Column(Boolean)  # store a file to the server (STOR, STOU commands)
	permission_CHMOD = Column(Boolean)  # change file mode / permission (SITE CHMOD command)
	permission_MFMT = Column(Boolean)  # change file modification time (SITE MFMT command)

class UserDb:
	def __init__(self):
		self.engine = create_engine("sqlite:///users_database.db")
		Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

	def create_user(self, username, password, home_dir, permissions):
		new_user = User(username=username, password=password, home_dir=home_dir, **permissions)
		self.session.add(new_user)
		self.session.commit()

	def get_user(self, username):
		return self.session.query(User).filter_by(username=username).first()

	def get_all_users(self):
		return self.session.query(User).all()

	def remove_user(self, username):
		user = self.session.query(User).filter_by(username=username).first()
		if user:
			self.session.delete(user)
			self.session.commit()

	def close(self):
		self.session.close()
