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
from PyQt6.QtGui import QPainter, QColor

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLineEdit, QToolButton, QPushButton, QFileDialog, QTableView, QSpacerItem, QHeaderView, QLabel, QFrame
from PyQt6.QtCore import QRegularExpression, Qt, QSortFilterProxyModel, QSize
from PyQt6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QIcon, QPixmap, QTransform, QFontDatabase, QFont

from src.GlobalStates import GlobalStates
from ui.frames.BaseLineFrame import BaseLineFrame
from ui.frames.PushLineFrame import PushLineFrame
from ui.frames.MarkedLineFrame import MarkedLineFrame

class AboutUserFormDialog(QDialog):
	def __init__(self):
		super(AboutUserFormDialog, self).__init__()

		GlobalStates.user_db.dirty.connect(self.user_db_updated)
		GlobalStates.user_db.deleted.connect(self.user_db_deleted)

		# Adding layouts
		self.frame_layout = QVBoxLayout()
		self.frame_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
		# self.spacer = QSpacerItem(540, 0)
		# self.frame_layout.addSpacerItem(self.spacer)

		self.username = MarkedLineFrame()
		self.username.setObjectName("main_frame_read_only")
		self.username.line_frame_icon.setPixmap(QPixmap("./icon/user_badge_24.svg"))
		self.username.line_frame_field.setReadOnly(True)
		self.username.line_frame_field.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		self.username.line_frame_tool.setVisible(False)
		self.frame_layout.addWidget(self.username)

		self.data_grid_layout = QGridLayout()
		self.frame_layout.addLayout(self.data_grid_layout)

		self.password_line = QLabel("Password:", self)
		self.password_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.password_line, 0, 0)
		self.password = PushLineFrame()
		self.password.line_frame_icon.setPixmap(QPixmap("./icon/password_24.svg"))
		self.password.line_frame_field.setReadOnly(True)
		self.password.line_frame_field.setEchoMode(QLineEdit.EchoMode.Password)
		self.password.line_frame_tool.setIcon(QIcon(QPixmap("./icon/visibility_off_24.svg")))
		self.password.line_frame_tool.clicked.connect(self.password_line_frame_tool_clicked)
		self.password.setObjectName("main_frame_read_only")
		self.data_grid_layout.addWidget(self.password, 0, 1)

		self.home_dir_line = QLabel("User home directory:", self)
		self.home_dir_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.home_dir_line, 1, 0)
		self.home_dir = BaseLineFrame()
		self.home_dir.line_frame_icon.setPixmap(QPixmap("./icon/user_directory_24.svg"))
		self.home_dir.line_frame_field.setReadOnly(True)
		self.home_dir.setObjectName("main_frame_read_only")
		self.data_grid_layout.addWidget(self.home_dir, 1, 1)

		self.date_of_creation_line = QLabel("Date of the creation of user:", self)
		self.date_of_creation_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.date_of_creation_line, 2, 0)
		self.date_of_creation = BaseLineFrame()
		self.date_of_creation.line_frame_icon.setPixmap(QPixmap("./icon/calendar_today_24.svg"))
		self.date_of_creation.line_frame_field.setReadOnly(True)
		self.date_of_creation.setObjectName("main_frame_read_only")
		self.data_grid_layout.addWidget(self.date_of_creation, 2, 1)

		self.date_of_change_line = QLabel("Date of the change user properties:", self)
		self.date_of_change_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.date_of_change_line, 3, 0)
		self.date_of_change = BaseLineFrame()
		self.date_of_change.line_frame_icon.setPixmap(QPixmap("./icon/calendar_today_24.svg"))
		self.date_of_change.line_frame_field.setReadOnly(True)
		self.date_of_change.setObjectName("main_frame_read_only")
		self.data_grid_layout.addWidget(self.date_of_change, 3, 1)

		self.last_login_date_line = QLabel("Date of the user last login:", self)
		self.last_login_date_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.last_login_date_line, 4, 0)
		self.last_login_date = BaseLineFrame()
		self.last_login_date.line_frame_icon.setPixmap(QPixmap("./icon/calendar_event_24.svg"))
		self.last_login_date.line_frame_field.setReadOnly(True)
		self.last_login_date.setObjectName("main_frame_read_only")
		self.data_grid_layout.addWidget(self.last_login_date, 4, 1)

		self.login_time_line = QLabel("Last login time:", self)
		self.login_time_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.login_time_line, 5, 0)
		self.login_time = BaseLineFrame()
		self.login_time.line_frame_icon.setPixmap(QPixmap("./icon/time_24.svg"))
		self.login_time.line_frame_field.setReadOnly(True)
		self.login_time.setObjectName("main_frame_read_only")
		self.data_grid_layout.addWidget(self.login_time, 5, 1)

		self.upload_statistics_line = QLabel("Statistics on uploaded data:", self)
		self.upload_statistics_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.upload_statistics_line, 6, 0)
		self.upload_statistics = QPlainTextEdit(self)
		self.upload_statistics.setMaximumHeight(90)
		self.upload_statistics.setReadOnly(True)
		self.data_grid_layout.addWidget(self.upload_statistics, 6, 1)

		self.download_statistics_line = QLabel("Statistics on downloaded data:", self)
		self.download_statistics_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.download_statistics_line, 7, 0)
		self.download_statistics = QPlainTextEdit(self)
		self.download_statistics.setMaximumHeight(90)
		self.download_statistics.setReadOnly(True)
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
		self.user_permission_list.setFixedSize(600, 70)
		self.user_permission_list.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
		self.user_permission_list.setModel(self.user_permission_model)
		self.user_permission_list.verticalHeader().setVisible(False)
		self.user_permission_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

		self.permission_line = QLabel("Permissions:", self)
		self.permission_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.permission_line, 8, 0)
		self.data_grid_layout.addWidget(self.user_permission_list, 8, 1)

		self.user_logs_line = QLabel("User logs:", self)
		self.user_logs_line.setObjectName("empty_background")
		self.data_grid_layout.addWidget(self.user_logs_line, 9, 0)
		self.user_logs = QPlainTextEdit(self)
		self.user_logs.setReadOnly(True)
		self.user_logs.setObjectName("console_font")
		self.data_grid_layout.addWidget(self.user_logs, 9, 1)

		# Dialog window customization
		self.setLayout(self.frame_layout)
		self.setWindowTitle("Inspect user data")
		# self.setMinimumSize(920, 480)

	def user_db_updated(self, user_obj):
		self.set_username(user_obj)

	def user_db_deleted(self, username):
		if username == self.username.line_frame_field.text():
			self.close()

	def password_line_frame_tool_clicked(self):
		if self.password.line_frame_tool.isChecked():
			self.password.line_frame_field.setEchoMode(QLineEdit.EchoMode.Normal)
			self.password.line_frame_tool.setIcon(QIcon(QPixmap("./icon/visibility_on_24.svg")))
		else:
			self.password.line_frame_field.setEchoMode(QLineEdit.EchoMode.Password)
			self.password.line_frame_tool.setIcon(QIcon(QPixmap("./icon/visibility_off_24.svg")))

	def set_username(self, user_obj):
		self.username.line_frame_field.setText(user_obj.username)
		self.password.line_frame_field.setText(user_obj.password)
		self.home_dir.line_frame_field.setText(user_obj.home_dir)

		if user_obj.online:
			self.username.line_frame_mark.setPixmap(QPixmap("./icon/online_24.svg"))
		else:
			self.username.line_frame_mark.setPixmap(QPixmap("./icon/offline_24.svg"))

		self.date_of_creation.line_frame_field.setText(str(user_obj.date_of_creation))
		self.date_of_change.line_frame_field.setText(str(user_obj.date_of_change))
		self.last_login_date.line_frame_field.setText(str(user_obj.last_login_date))
		self.login_time.line_frame_field.setText(str(user_obj.login_time))

		self.upload_statistics.setPlainText(f"Number of successfully uploaded: {user_obj.upload_count_successful} files\nTotal upload traffic: {naturalsize(user_obj.upload_size, binary=True, format='%.3f')}\nTotal uploading time: {precisedelta(user_obj.upload_time, format='%.3f')}")
		self.download_statistics.setPlainText(f"Number of successfully downloaded: {user_obj.download_count_successful} files\nTotal download traffic: {naturalsize(user_obj.download_size, binary=True, format='%.3f')}\nTotal downloading time: {precisedelta(user_obj.download_time, format='%.3f')}")

		for col, data in enumerate([
			user_obj.permission_CWD,
			user_obj.permission_LIST,
			user_obj.permission_RETR,
			user_obj.permission_APPE,
			user_obj.permission_DELE,
			user_obj.permission_RNFR,
			user_obj.permission_MKD,
			user_obj.permission_STOR,
			user_obj.permission_CHMOD,
			user_obj.permission_MFMT
		]):
			if data:
				item = QStandardItem(QIcon("./icon/check_24.svg"), "")
			else:
				item = QStandardItem(QIcon("./icon/cancel_24.svg"), "")
			item.setEditable(False)
			item.setSelectable(False)
			self.user_permission_model.setItem(0, col, item)

		self.user_logs.setPlainText(str(user_obj.user_logs).strip())
