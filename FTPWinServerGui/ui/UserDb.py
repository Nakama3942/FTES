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

from sqlalchemy import create_engine, update, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from PyQt6.QtCore import QObject, pyqtSignal

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String)
	password = Column(String)
	home_dir = Column(String)
	date_of_creation = Column(DateTime)
	date_of_change = Column(DateTime)
	last_login_date = Column(DateTime)
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
	user_logs = Column(String)

class UserDb(QObject):
	new = pyqtSignal(str)
	dirty = pyqtSignal(str)
	deleted = pyqtSignal(str)

	def __init__(self):
		super(UserDb, self).__init__()

		self.engine = create_engine("sqlite:///users_database.db")
		Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

	def get_user(self, username):
		return self.session.query(User).filter_by(username=username).first()

	def get_all_users(self):
		return self.session.query(User).all()

	def create_user(self, username, user_data):
		new_user = User(username=username, **user_data)
		self.session.add(new_user)
		self.new.emit(username)
		self.session.commit()

	def update_user(self, username, new_data):
		user = self.get_user(username)
		if user:
			# Обновляем поля пользователя
			for key, value in new_data.items():
				setattr(user, key, value)

			# Фиксируем изменения в базе данных
			self.dirty.emit(username)
			self.session.commit()

	def silent_spy_update(self, username, new_data):
		user = self.get_user(username)
		if user:
			for key, value in new_data.items():
				# Создаем объект запроса для обновления поля
				update_query = update(User).where(User.username == username)
				# Обновляем поле, добавляя новое значение
				update_query = update_query.values({key: User.__dict__[key] + value})
				# Выполняем запрос
				self.session.execute(update_query)

			self.session.commit()

	def set_user_date(self, username, new_data):
		user = self.get_user(username)
		if user:
			# Обновляем поля пользователя
			for key, value in new_data.items():
				setattr(user, key, value)

			# Фиксируем изменения в базе данных
			self.session.commit()

	def remove_user(self, username):
		user = self.session.query(User).filter_by(username=username).first()
		if user:
			self.session.delete(user)
			self.deleted.emit(username)
			self.session.commit()

	def close(self):
		self.session.close()
