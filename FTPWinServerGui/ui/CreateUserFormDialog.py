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

from datetime import datetime
import re
import os

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit, QCheckBox, QGroupBox, QPushButton, QLabel, QFrame
from PyQt6.QtGui import QPixmap, QIcon

from src.GlobalStates import GlobalStates
from ui.frames.MessageLineFrame import MessageLineFrame

class CreateUserFormDialog(QDialog):
	def __init__(self):
		super(CreateUserFormDialog, self).__init__()

		# Adding layouts
		self.frame_layout = QVBoxLayout()
		self.frame_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
		self.spacer = QSpacerItem(540, 0)
		self.frame_layout.addSpacerItem(self.spacer)

		self.username = MessageLineFrame()
		self.username.line_frame_icon.setPixmap(QPixmap("./icon/user_badge_24.svg"))
		self.username.line_frame_field.setPlaceholderText("Enter the username")
		self.username.line_frame_field.textChanged.connect(self.username_frame_line_edit_textChanged)
		self.username.line_frame_tool.setVisible(False)
		self.username.line_frame_mark.setPixmap(QPixmap("./icon/circle_24.svg"))
		self.frame_layout.addWidget(self.username)

		self.password = MessageLineFrame()
		self.password.line_frame_icon.setPixmap(QPixmap("./icon/password_24.svg"))
		self.password.line_frame_field.setEchoMode(QLineEdit.EchoMode.Password)
		self.password.line_frame_field.setPlaceholderText("Enter the password")
		self.password.line_frame_field.textChanged.connect(self.password_frame_line_edit_textChanged)
		self.password.line_frame_tool.setIcon(QIcon(QPixmap("./icon/visibility_off_24.svg")))
		self.password.line_frame_tool.clicked.connect(self.password_line_frame_tool_clicked)
		self.password.line_frame_mark.setPixmap(QPixmap("./icon/circle_24.svg"))
		self.frame_layout.addWidget(self.password)

		self.home_dir = MessageLineFrame()
		self.home_dir.line_frame_icon.setPixmap(QPixmap("./icon/user_directory_24.svg"))
		self.home_dir.line_frame_field.setPlaceholderText("Enter the home directory")
		self.home_dir.line_frame_field.textChanged.connect(self.home_dir_frame_line_edit_textChanged)
		self.home_dir.line_frame_tool.setVisible(False)
		self.home_dir.line_frame_mark.setPixmap(QPixmap("./icon/circle_24.svg"))
		self.user_home_dir = QCheckBox("Create a personal user directory in the specified directory", self)
		self.home_dir.main_layout.addWidget(self.user_home_dir)
		self.frame_layout.addWidget(self.home_dir)

		self.permission_layout = QVBoxLayout()
		self.permission_e = QCheckBox("Change directory (CWD, CDUP commands)", self)
		self.permission_layout.addWidget(self.permission_e)
		self.permission_l = QCheckBox("List files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)", self)
		self.permission_layout.addWidget(self.permission_l)
		self.permission_r = QCheckBox("Retrieve file from the server (RETR command)", self)
		self.permission_layout.addWidget(self.permission_r)
		self.permission_a = QCheckBox("Append data to an existing file (APPE command)", self)
		self.permission_layout.addWidget(self.permission_a)
		self.permission_d = QCheckBox("Delete file or directory (DELE, RMD commands)", self)
		self.permission_layout.addWidget(self.permission_d)
		self.permission_f = QCheckBox("Rename file or directory (RNFR, RNTO commands)", self)
		self.permission_layout.addWidget(self.permission_f)
		self.permission_m = QCheckBox("Create directory (MKD command)", self)
		self.permission_layout.addWidget(self.permission_m)
		self.permission_w = QCheckBox("Store a file to the server (STOR, STOU commands)", self)
		self.permission_layout.addWidget(self.permission_w)
		self.permission_M = QCheckBox("Change file mode / permission (SITE CHMOD command)", self)
		self.permission_layout.addWidget(self.permission_M)
		self.permission_T = QCheckBox("Change file modification time (SITE MFMT command)", self)
		self.permission_layout.addWidget(self.permission_T)

		self.permission_group = QGroupBox(self)
		self.permission_group.setTitle("Permissions")
		self.permission_group.setLayout(self.permission_layout)
		self.frame_layout.addWidget(self.permission_group)

		self.add_butt = QPushButton("Add new user", self)
		self.add_butt.clicked.connect(self.add_butt_clicked)
		self.frame_layout.addWidget(self.add_butt)

		# Dialog window customization
		self.setLayout(self.frame_layout)
		self.setWindowTitle("Add new user")
		# self.setMinimumSize(600, 480)

	def username_frame_line_edit_textChanged(self, text):
		if text == "":
			self.username.line_frame_message.setVisible(False)
			self.username.line_frame_message.setText("")
			self.username.line_frame_mark.setPixmap(QPixmap("./icon/circle_24.svg"))
			self.username.logic_mark = False
		else:
			self.username.line_frame_message.setVisible(True)
			if len(text) > 14:
				self.username.line_frame_message.setVisible(True)
				self.username.line_frame_message.setText("The name must not exceed 14 letters!")
				self.username.line_frame_mark.setPixmap(QPixmap("./icon/circle_cancel_24.svg"))
				self.username.logic_mark = False
			elif re.match(r'^[a-zA-Z_]+$', text):
				if GlobalStates.user_db.check_username(text):
					self.username.line_frame_message.setText("Once the user is created, the name cannot be changed!")
					self.username.line_frame_mark.setPixmap(QPixmap("./icon/circle_check_24.svg"))
					self.username.logic_mark = True
				else:
					self.username.line_frame_message.setText("A user with this name already exists!")
					self.username.line_frame_mark.setPixmap(QPixmap("./icon/circle_cancel_24.svg"))
					self.username.logic_mark = False
			else:
				self.username.line_frame_message.setText("Wrong user name!")
				self.username.line_frame_mark.setPixmap(QPixmap("./icon/circle_cancel_24.svg"))
				self.username.logic_mark = False

	def password_line_frame_tool_clicked(self):
		if self.password.line_frame_tool.isChecked():
			self.password.line_frame_field.setEchoMode(QLineEdit.EchoMode.Normal)
			self.password.line_frame_tool.setIcon(QIcon(QPixmap("./icon/visibility_on_24.svg")))
		else:
			self.password.line_frame_field.setEchoMode(QLineEdit.EchoMode.Password)
			self.password.line_frame_tool.setIcon(QIcon(QPixmap("./icon/visibility_off_24.svg")))

	def password_frame_line_edit_textChanged(self, text):
		if text == "":
			self.password.line_frame_message.setVisible(False)
			self.password.line_frame_message.setText("")
			self.password.line_frame_mark.setPixmap(QPixmap("./icon/circle_24.svg"))
			self.password.logic_mark = False
		else:
			# Проверка пароля
			if len(text) < 4:
				self.password.line_frame_message.setVisible(True)
				self.password.line_frame_message.setText("The password is too short!")
				self.password.line_frame_mark.setPixmap(QPixmap("./icon/circle_cancel_24.svg"))
				self.password.logic_mark = False
			elif re.match(r'^[a-zA-Z0-9]+$', text):
				has_digit = any(char.isdigit() for char in text)
				has_alpha = any(char.isalpha() for char in text)
				if has_digit and has_alpha:
					self.password.line_frame_message.setVisible(False)
					self.password.line_frame_message.setText("")
					self.password.line_frame_mark.setPixmap(QPixmap("./icon/circle_check_24.svg"))
				else:
					self.password.line_frame_message.setVisible(True)
					self.password.line_frame_message.setText("The password is not secure!")
					self.password.line_frame_mark.setPixmap(QPixmap("./icon/circle_check_24.svg"))
				self.password.logic_mark = True
			else:
				self.password.line_frame_message.setVisible(True)
				self.password.line_frame_message.setText("Wrong password!")
				self.password.line_frame_mark.setPixmap(QPixmap("./icon/circle_cancel_24.svg"))
				self.password.logic_mark = False

	def home_dir_frame_line_edit_textChanged(self, text):
		if text == "":
			self.home_dir.line_frame_message.setVisible(False)
			self.home_dir.line_frame_message.setText("")
			self.home_dir.line_frame_mark.setPixmap(QPixmap("./icon/circle_24.svg"))
			self.home_dir.logic_mark = False
		else:
			if os.path.exists(text) and os.path.isdir(text):
				self.home_dir.line_frame_message.setVisible(False)
				self.home_dir.line_frame_message.setText("")
				self.home_dir.line_frame_mark.setPixmap(QPixmap("./icon/circle_check_24.svg"))
				self.home_dir.logic_mark = True
			else:
				self.home_dir.line_frame_message.setVisible(True)
				self.home_dir.line_frame_message.setText("Wrong directory!")
				self.home_dir.line_frame_mark.setPixmap(QPixmap("./icon/circle_cancel_24.svg"))
				self.home_dir.logic_mark = False

	def add_butt_clicked(self):
		if self.user_home_dir.isChecked():
			# Создайте путь для личной директории пользователя
			user_directory = os.path.join(self.home_dir.line_frame_field.text(), self.username.line_frame_field.text())
			# Проверьте, существует ли директория пользователя
			if not os.path.exists(user_directory):
				# Если не существует, создайте ее
				os.makedirs(user_directory)
		else:
			user_directory = self.home_dir.line_frame_field.text()

		if self.username.logic_mark and self.password.logic_mark and self.home_dir.logic_mark:
			GlobalStates.user_db.create_user(
				self.username.line_frame_field.text(),
				{
					"password": self.password.line_frame_field.text(),
					"home_dir": user_directory,
					"upload_count_successful": 0,
					"upload_size": 0,
					"upload_time": 0.0,
					"download_count_successful": 0,
					"download_size": 0,
					"download_time": 0.0,
					"permission_CWD": self.permission_e.isChecked(),
					"permission_LIST": self.permission_l.isChecked(),
					"permission_RETR": self.permission_r.isChecked(),
					"permission_APPE": self.permission_a.isChecked(),
					"permission_DELE": self.permission_d.isChecked(),
					"permission_RNFR": self.permission_f.isChecked(),
					"permission_MKD": self.permission_m.isChecked(),
					"permission_STOR": self.permission_w.isChecked(),
					"permission_CHMOD": self.permission_M.isChecked(),
					"permission_MFMT": self.permission_T.isChecked(),
					"user_logs": ""
				}
			)
			GlobalStates.user_db.set_user_status(self.username.line_frame_field.text(), False)
			GlobalStates.user_db.set_user_date(self.username.line_frame_field.text(), {"date_of_creation": datetime.now().replace(microsecond=0)})
			self.close()
