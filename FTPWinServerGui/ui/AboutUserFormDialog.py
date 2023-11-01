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

from humanize import naturalsize, precisedelta

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QSpacerItem, QLineEdit, QCheckBox, QGroupBox, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLineEdit, QToolButton, QPushButton, QFileDialog, QTableView, QSpacerItem, QHeaderView, QLabel, QFrame
from PyQt6.QtCore import QRegularExpression, Qt, QSortFilterProxyModel, QSize
from PyQt6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QIcon, QPixmap, QTransform, QFontDatabase, QFont

from src.GlobalStates import GlobalStates

# todo Заменить все поля на собственные фреймы
# todo Добавить статус online/offline

class AboutUserFormDialog(QDialog):
	def __init__(self):
		super(AboutUserFormDialog, self).__init__()

		# Adding layouts
		self.frame_layout = QVBoxLayout()
		self.frame_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
		# self.spacer = QSpacerItem(540, 0)
		# self.frame_layout.addSpacerItem(self.spacer)

		self.username = QLineEdit(self)
		self.username.setReadOnly(True)
		self.username.setObjectName("not_editable_line")
		self.username.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		self.frame_layout.addWidget(self.username)

		self.data_grid_layout = QGridLayout()
		self.frame_layout.addLayout(self.data_grid_layout)

		self.password_line = QLabel("Password:", self)
		self.password_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.password_line, 0, 0)
		self.password = QLineEdit(self)
		self.password.setReadOnly(True)
		self.password.setObjectName("not_editable_line")
		# self.password.setEchoMode(QLineEdit.EchoMode.Password)
		self.data_grid_layout.addWidget(self.password, 0, 1)

		self.home_dir_line = QLabel("User home directory:", self)
		self.home_dir_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.home_dir_line, 1, 0)
		self.home_dir = QLineEdit(self)
		self.home_dir.setReadOnly(True)
		self.home_dir.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.home_dir, 1, 1)

		self.date_of_creation_line = QLabel("Date of the creation of user:", self)
		self.date_of_creation_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.date_of_creation_line, 2, 0)
		self.date_of_creation = QLineEdit(self)
		self.date_of_creation.setReadOnly(True)
		self.date_of_creation.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.date_of_creation, 2, 1)

		self.date_of_change_line = QLabel("Date of the change user properties:", self)
		self.date_of_change_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.date_of_change_line, 3, 0)
		self.date_of_change = QLineEdit(self)
		self.date_of_change.setReadOnly(True)
		self.date_of_change.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.date_of_change, 3, 1)

		self.last_login_date_line = QLabel("Date of the user last login:", self)
		self.last_login_date_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.last_login_date_line, 4, 0)
		self.last_login_date = QLineEdit(self)
		self.last_login_date.setReadOnly(True)
		self.last_login_date.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.last_login_date, 4, 1)

		self.login_time_line = QLabel("Last login time:", self)
		self.login_time_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.login_time_line, 5, 0)
		self.login_time = QLineEdit(self)
		self.login_time.setReadOnly(True)
		self.login_time.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.login_time, 5, 1)

		self.upload_statistics_line = QLabel("Statistics on uploaded data:", self)
		self.upload_statistics_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.upload_statistics_line, 6, 0)
		self.upload_statistics = QPlainTextEdit(self)
		self.upload_statistics.setMaximumHeight(90)
		self.upload_statistics.setReadOnly(True)
		self.upload_statistics.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.upload_statistics, 6, 1)

		self.download_statistics_line = QLabel("Statistics on downloaded data:", self)
		self.download_statistics_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.download_statistics_line, 7, 0)
		self.download_statistics = QPlainTextEdit(self)
		self.download_statistics.setMaximumHeight(90)
		self.download_statistics.setReadOnly(True)
		self.download_statistics.setObjectName("not_editable_line")
		self.data_grid_layout.addWidget(self.download_statistics, 7, 1)

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

		self.permission_line = QLabel("Permissions:", self)
		self.permission_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.permission_line, 8, 0)
		self.data_grid_layout.addWidget(self.user_permission_list, 8, 1)

		self.user_logs_line = QLabel("User logs:", self)
		self.user_logs_line.setObjectName("frame_in_frame")
		self.data_grid_layout.addWidget(self.user_logs_line, 9, 0)
		self.user_logs = QPlainTextEdit(self)
		self.user_logs.setReadOnly(True)
		self.data_grid_layout.addWidget(self.user_logs, 9, 1)

		# Dialog window customization
		self.setLayout(self.frame_layout)
		self.setWindowTitle("Inspect user data")
		# self.setMinimumSize(920, 480)

	def set_username(self, username):
		user = GlobalStates.user_db.get_user(username)
		self.username.setText(user.username)
		self.password.setText(user.password)
		self.home_dir.setText(user.home_dir)

		self.date_of_creation.setText(str(user.date_of_creation))
		self.date_of_change.setText(str(user.date_of_change))
		self.last_login_date.setText(str(user.last_login_date))
		self.login_time.setText(str(user.login_time))

		self.upload_statistics.setPlainText(f"Number of successfully uploaded: {user.upload_count_successful} files\nTotal upload traffic: {naturalsize(user.upload_size, binary=True, format='%.3f')}\nTotal uploading time: {precisedelta(user.upload_time, format='%.3f')}")
		self.download_statistics.setPlainText(f"Number of successfully downloaded: {user.download_count_successful} files\nTotal download traffic: {naturalsize(user.download_size, binary=True, format='%.3f')}\nTotal downloading time: {precisedelta(user.download_time, format='%.3f')}")

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

		self.user_logs.setPlainText(str(user.user_logs).strip())
