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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QCheckBox, QGroupBox, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLineEdit, QToolButton, QPushButton, QFileDialog, QTableView, QSpacerItem, QHeaderView, QLabel, QFrame
from PyQt6.QtCore import QRegularExpression, Qt, QSortFilterProxyModel, QSize
from PyQt6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QIcon, QPixmap, QTransform, QFontDatabase, QFont

from src.GlobalStates import GlobalStates

class AboutUserFormDialog(QDialog):
	def __init__(self):
		super(AboutUserFormDialog, self).__init__()

		# Adding layouts
		self.frame_layout = QVBoxLayout()

		self.username = QLineEdit(self)
		self.username.setReadOnly(True)
		self.username.setObjectName("not_editable_line")
		self.username.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		self.frame_layout.addWidget(self.username)

		self.password = QLineEdit(self)
		self.password.setReadOnly(True)
		self.password.setObjectName("not_editable_line")
		# self.password.setEchoMode(QLineEdit.EchoMode.Password)
		self.frame_layout.addWidget(self.password)

		self.home_dir = QLineEdit(self)
		self.home_dir.setReadOnly(True)
		self.home_dir.setObjectName("not_editable_line")
		self.frame_layout.addWidget(self.home_dir)

		self.date_of_creation = QLineEdit(self)
		self.date_of_creation.setReadOnly(True)
		self.date_of_creation.setObjectName("not_editable_line")
		self.frame_layout.addWidget(self.date_of_creation)

		self.date_of_change = QLineEdit(self)
		self.date_of_change.setReadOnly(True)
		self.date_of_change.setObjectName("not_editable_line")
		self.frame_layout.addWidget(self.date_of_change)

		self.last_login_date = QLineEdit(self)
		self.last_login_date.setReadOnly(True)
		self.last_login_date.setObjectName("not_editable_line")
		self.frame_layout.addWidget(self.last_login_date)

		# Creating a data model
		self.user_permission_model = QStandardItemModel(1, 10)
		self.user_permission_model.setHorizontalHeaderLabels([
			'CWD',
			'LIST',
			'RETR',
			'APPE',
			'DELE',
			'RNFR',
			'MKD',
			'STOR',
			'CHMOD',
			'MFMT'
		])

		# Displaying the data shell in a table
		self.user_permission_list = QTableView(self)
		self.user_permission_list.setMinimumSize(570, 70)
		self.user_permission_list.setMaximumSize(570, 70)
		self.user_permission_list.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
		self.user_permission_list.setModel(self.user_permission_model)
		self.user_permission_list.verticalHeader().setVisible(False)
		self.user_permission_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		self.frame_layout.addWidget(self.user_permission_list)

		self.user_logs = QPlainTextEdit(self)
		# self.user_logs.setMinimumSize(750, 0)
		self.user_logs.setReadOnly(True)
		self.frame_layout.addWidget(self.user_logs)

		# Dialog window customization
		self.setLayout(self.frame_layout)
		self.setWindowTitle("Add new user")
		self.setMinimumSize(720, 480)

	def set_username(self, username):
		self.username.setText(username)
		user = GlobalStates.user_db.get_user(username)
		self.password.setText(f"Password: {user.password}")
		self.home_dir.setText(f"User home directory: '{user.home_dir}'")

		self.date_of_creation.setText(f"Date of the creation of user: {user.date_of_creation}")
		self.date_of_change.setText(f"Date of the change user properties: {user.date_of_change}")
		self.last_login_date.setText(f"Date of the user last login: {user.last_login_date}")

		for col, data in enumerate([
			user.permission_CWD,
			user.permission_LIST,
			user.permission_RETR,
			user.permission_APPE,
			user.permission_DELE,
			user.permission_RNFR,
			user.permission_MKD,
			user.permission_STOR,
			user.permission_CHMOD,
			user.permission_MFMT
		]):
			if data:
				item = QStandardItem(QIcon("./icon/check_24.svg"), "")
			else:
				item = QStandardItem(QIcon("./icon/false_24.svg"), "")
			item.setEditable(False)
			item.setSelectable(False)
			self.user_permission_model.setItem(0, col, item)

		self.user_logs.appendPlainText(user.user_logs)
