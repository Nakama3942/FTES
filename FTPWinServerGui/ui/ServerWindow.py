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

# todo Реализовать закрытие сервера при закрытии программы
# todo Реализовать проверки ввода
# todo По возможности, добавить свой Логгер вместо стандартного

from datetime import datetime
import pickle
import re

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLineEdit, QToolButton, QPushButton, QFileDialog, QTableView, QSpacerItem, QHeaderView, QLabel, QFrame
from PyQt6.QtCore import QRegularExpression, Qt, QSortFilterProxyModel, QSize
from PyQt6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QIcon, QPixmap, QTransform, QFontDatabase, QFont

from src.GlobalStates import GlobalStates
from src.Server import Server
from ui.Interceptor import Interceptor
from ui.CreateUserFormDialog import CreateUserFormDialog
from ui.UpdateUserFormDialog import UpdateUserFormDialog
from ui.AboutUserFormDialog import AboutUserFormDialog

class ServerWindow(QMainWindow):
	def __init__(self):
		super(ServerWindow, self).__init__()

		###################
		# Initialization
		###################
		# Initialization of program font
		QFontDatabase.addApplicationFont("./font/Montserrat-Medium.ttf")
		QFontDatabase.addApplicationFont("./font/JetBrainsMono-Light.ttf")
		# print(QFontDatabase.applicationFontFamilies(id)[0])

		# Initialization of Logger
		self.STDOUT = Interceptor()
		self.STDERR = Interceptor()
		self.STDOUT.writing.connect(self.intercept_writing)
		self.STDERR.writing.connect(self.intercept_writing)

		# Initialization of dialog windows
		self.create_user_form_dialog = CreateUserFormDialog()
		self.update_user_form_dialog = UpdateUserFormDialog()
		self.about_user_form_dialog = AboutUserFormDialog()

		# Initialization of Server
		self.serv = Server("", self.STDOUT, self.STDERR)
		self.serv.set_log()

		##############################
		#
		# Server layout
		#
		##############################
		self.server_layout = QVBoxLayout()

		self.console = QPlainTextEdit(self)
		self.console.setMinimumSize(750, 0)
		self.console.setReadOnly(True)
		self.server_layout.addWidget(self.console)

		self.serving_layout = QHBoxLayout()

		self.ip_address = QLineEdit(self)
		self.ip_address.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		self.ip_address.setPlaceholderText("Enter the IP")
		self.ip_address.setValidator(
			QRegularExpressionValidator(
				QRegularExpression(
					r"^192\.168\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
				)
			)
		)
		self.serving_layout.addWidget(self.ip_address)

		self.serving_butt = QPushButton("Start server", self)
		self.serving_butt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.serving_butt.setCheckable(True)
		self.serving_butt.clicked.connect(self.serving_butt_clicked)
		self.serving_layout.addWidget(self.serving_butt)

		self.server_layout.addLayout(self.serving_layout)

		##############################
		#
		# Users layout
		#
		##############################
		self.users_layout = QVBoxLayout()

		###################
		# Search line
		###################
		self.attention_line = QLabel(self)
		self.attention_line.setText("For changes to the user database to take effect,\nyou need to restart the server.")
		self.attention_line.setObjectName("attention_line")
		self.attention_line.setVisible(False)
		self.users_layout.addWidget(self.attention_line)

		self.search_layout = QHBoxLayout()

		self.search_line = QLineEdit(self)
		self.search_line.setPlaceholderText("Search username")
		self.search_line.textChanged.connect(self.search_line_textChanged)
		self.search_layout.addWidget(self.search_line)

		self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.search_layout.addSpacerItem(self.spacer)

		self.users_layout.addLayout(self.search_layout)

		###################
		# Creating a user table
		###################
		# Reading the entire database
		user_list = GlobalStates.user_db.get_all_users()

		# Creating a data model
		self.user_model = QStandardItemModel(len(user_list), 4)
		self.user_model.setHorizontalHeaderLabels([
			'Username',
			'RETR',
			'DELE',
			'STOR'
		])

		# Filling the model with data from the list of users
		for row, user in enumerate(user_list):
			self.process_table_row(row, user)

		# Adding the model to the filter shell
		self.proxy_model = QSortFilterProxyModel()
		self.proxy_model.setSourceModel(self.user_model)  # Подставьте сюда свою модель данных

		# Displaying the data shell in a table
		self.user_list = QTableView(self)
		self.user_list.setModel(self.proxy_model)
		self.user_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		GlobalStates.user_db.new.connect(self.user_db_new)
		GlobalStates.user_db.dirty.connect(self.user_db_dirty)
		GlobalStates.user_db.deleted.connect(self.user_db_deleted)
		self.users_layout.addWidget(self.user_list)

		###################
		# Adding a tool buttons
		###################
		self.tool_layout = QHBoxLayout()

		self.straight_sort_tool = QToolButton(self)
		self.straight_sort_tool.setIcon(QIcon(QPixmap("./icon/sort_24.svg")))
		self.straight_sort_tool.clicked.connect(self.straight_sort_tool_clicked)
		self.tool_layout.addWidget(self.straight_sort_tool)

		self.reverse_sort_tool = QToolButton(self)
		self.reverse_sort_tool.setIcon(QIcon(QPixmap("./icon/sort_24.svg").transformed(QTransform().scale(1, -1))))
		self.reverse_sort_tool.clicked.connect(self.reverse_sort_tool_clicked)
		self.tool_layout.addWidget(self.reverse_sort_tool)

		self.reset_sort_tool = QToolButton(self)
		self.reset_sort_tool.setIcon(QIcon(QPixmap("./icon/reset_sort_24.svg")))
		self.reset_sort_tool.clicked.connect(self.reset_sort_tool_clicked)
		self.tool_layout.addWidget(self.reset_sort_tool)

		self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.tool_layout.addSpacerItem(self.spacer)

		self.add_user_tool = QToolButton(self)
		self.add_user_tool.setIcon(QIcon(QPixmap("./icon/user_add_24.svg")))
		self.add_user_tool.clicked.connect(self.add_user_tool_clicked)
		self.tool_layout.addWidget(self.add_user_tool)

		self.update_user_tool = QToolButton(self)
		self.update_user_tool.setIcon(QIcon(QPixmap("./icon/user_update_24.svg")))
		self.update_user_tool.clicked.connect(self.update_user_tool_clicked)
		self.tool_layout.addWidget(self.update_user_tool)

		self.about_user_tool = QToolButton(self)
		self.about_user_tool.setIcon(QIcon(QPixmap("./icon/about_user_24.svg")))
		self.about_user_tool.clicked.connect(self.about_user_tool_clicked)
		self.tool_layout.addWidget(self.about_user_tool)

		self.remove_user_tool = QToolButton(self)
		self.remove_user_tool.setIcon(QIcon(QPixmap("./icon/user_remove_24.svg")))
		self.remove_user_tool.clicked.connect(self.remove_user_tool_clicked)
		self.tool_layout.addWidget(self.remove_user_tool)

		self.users_layout.addLayout(self.tool_layout)

		##############################
		#
		# Main window customization
		#
		##############################
		self.main_layout = QHBoxLayout()
		# self.main_layout.setContentsMargins(20, 6, 6, 6)
		self.main_layout.addLayout(self.server_layout)
		self.main_layout.addLayout(self.users_layout)

		self.central_widget = QWidget()
		self.central_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.central_widget)
		self.setWindowTitle("FTES WSG - File Transfer EcoSystem Windows Server Graphic")
		self.setMinimumSize(1280, 720)

	##############################
	#
	# Implementations
	#
	##############################
	###################
	# Implementations of Server functional
	###################
	def intercept_writing(self, text):
		"""Implementation of log writing"""
		self.console.appendPlainText(text.strip())

		text_re = re.search(r"\[.*\] .*-\[(.*?)\]", text)
		if text_re:
			username = text_re.group(1)
			if username:
				GlobalStates.user_db.silent_spy_update(username, {"user_logs": text})
				if re.search(r"logged in", text):
					GlobalStates.user_db.set_user_date(username, {"last_login_date": datetime.now().replace(microsecond=0)})
			else:
				# Если вторые квадратные скобки пусты, ищем имя пользователя после слова USER в одинарных кавычках
				text_re = re.search(r"USER '(.*?)'", text)
				if text_re:
					username = text_re.group(1)
					if username:
						GlobalStates.user_db.silent_spy_update(username, {"user_logs": text})

	def serving_butt_clicked(self) -> None:
		"""Implementation of connect/disconnect button"""
		if self.serving_butt.isChecked():
			self.serving_butt.setText("Stop server")
			self.attention_line.setVisible(True)

			if self.ip_address.text() != "":
				self.serv.set_ip(self.ip_address.text())

			self.serv.build()

			users = GlobalStates.user_db.get_all_users()
			for user in users:
				permissions_dict = {
					"e": user.permission_CWD,
					"l": user.permission_LIST,
					"r": user.permission_RETR,
					"a": user.permission_APPE,
					"d": user.permission_DELE,
					"f": user.permission_RNFR,
					"m": user.permission_MKD,
					"w": user.permission_STOR,
					"M": user.permission_CHMOD,
					"T": user.permission_MFMT
				}
				permission = ''.join(key for key, value in permissions_dict.items() if value)
				self.serv.add_user(user.username, user.password, user.home_dir, permission)

			self.serv.run()

		else:
			self.serving_butt.setText("Start server")
			self.attention_line.setVisible(False)
			self.serv.stop()
			self.serv.remove_all_users()

	###################
	# Implementations of Users functional
	###################
	def search_line_textChanged(self):
		"""Implementation of search in users table"""
		self.proxy_model.setFilterRegularExpression(self.search_line.text())

	def user_db_new(self, username):
		"""Implementation of adding a new user"""
		new_row = self.user_list.model().rowCount()
		updated_user = GlobalStates.user_db.get_user(username)

		self.process_table_row(new_row, updated_user)

		self.user_list.update()

	def user_db_dirty(self, username):
		"""Implementation of updating a user"""
		selected_row = self.user_list.selectionModel().selectedIndexes()[0].row()
		updated_user = GlobalStates.user_db.get_user(username)

		self.process_table_row(selected_row, updated_user)

		self.user_list.update()

	def user_db_deleted(self, username):
		"""Implementation of deleting an old user"""
		deleted_rows = self.user_list.selectionModel().selectedRows()

		# Переберите индексы в обратном порядке, чтобы не нарушить порядок при удалении строк
		for index in sorted(deleted_rows, reverse=True):
			row = index.row()
			# Удалите строку из модели
			self.user_model.removeRow(row)

		self.user_list.update()

	def straight_sort_tool_clicked(self):
		"""Implementation of sort a user table"""
		column = 0  # Номер столбца, по которому вы хотите сортировать
		order = Qt.SortOrder.AscendingOrder  # Используйте Qt.AscendingOrder или Qt.DescendingOrder
		self.user_list.model().sort(column, order)

	def reverse_sort_tool_clicked(self):
		"""Implementation of sort in reverse order a user table"""
		column = 0  # Номер столбца, по которому вы хотите сортировать
		order = Qt.SortOrder.DescendingOrder  # Используйте Qt.AscendingOrder или Qt.DescendingOrder
		self.user_list.model().sort(column, order)

	def reset_sort_tool_clicked(self):
		"""Implementation of reset a sorting"""
		self.user_list.model().sort(-1)  # Установить столбец сортировки на -1, чтобы вернуть исходный порядок

	def add_user_tool_clicked(self):
		"""Implementation of showing a dialog window for adding a new user"""
		self.create_user_form_dialog.show()

	def update_user_tool_clicked(self):
		"""Implementation of showing a dialog window for updating a user"""
		selected_indexes = self.user_list.selectionModel().selectedRows()
		if len(selected_indexes) == 0:
			return
		username_index = self.user_model.index(selected_indexes[0].row(), 0)
		username = self.user_model.data(username_index)
		self.update_user_form_dialog.set_username(username)
		self.update_user_form_dialog.show()

	def about_user_tool_clicked(self):
		"""Implementation of showing a dialog window for view data about user"""
		selected_indexes = self.user_list.selectionModel().selectedRows()
		if len(selected_indexes) == 0:
			return
		username_index = self.user_model.index(selected_indexes[0].row(), 0)
		username = self.user_model.data(username_index)
		self.about_user_form_dialog.set_username(username)
		self.about_user_form_dialog.show()

	def remove_user_tool_clicked(self):
		"""Implementation of showing a dialog window for deleting an old user"""
		selected_indexes = self.user_list.selectionModel().selectedRows()
		usernames = []

		for index in selected_indexes:
			# Получаем индекс выделенной строки и столбца с именем пользователя (первый столбец)
			username_index = self.user_model.index(index.row(), 0)
			username = self.user_model.data(username_index)  # Получаем имя пользователя
			usernames.append(username)

		for username in usernames:
			GlobalStates.user_db.remove_user(username)

	def process_table_row(self, row, user):
		"""Implementation of adding table item in user row"""
		for col, data in enumerate([
			user.username,
			user.permission_RETR,
			user.permission_DELE,
			user.permission_STOR
		]):
			item = QStandardItem(str(data))
			item.setEditable(False)
			if col != 0:
				item.setSelectable(False)
			self.user_model.setItem(row, col, item)
