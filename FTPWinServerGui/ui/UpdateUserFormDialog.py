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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QSpacerItem, QLineEdit, QCheckBox, QGroupBox, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt

from src.GlobalStates import GlobalStates
from ui.frames.ApprovingLineFrame import ApprovingLineFrame

class UpdateUserFormDialog(QDialog):
	def __init__(self):
		super(UpdateUserFormDialog, self).__init__()

		# Adding layouts
		self.frame_layout = QVBoxLayout()
		self.frame_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)
		self.spacer = QSpacerItem(540, 0)
		self.frame_layout.addSpacerItem(self.spacer)

		self.username = QLineEdit(self)
		self.username.setReadOnly(True)
		self.username.setObjectName("not_editable_line")
		self.username.setAlignment(Qt.AlignmentFlag.AlignHCenter)
		self.frame_layout.addWidget(self.username)

		self.password = ApprovingLineFrame("./icon/password_24.svg", "Enter the password")
		self.password.frame_line_edit.setEchoMode(QLineEdit.EchoMode.Password)
		self.password.frame_line_edit.textChanged.connect(self.password_frame_line_edit_textChanged)
		self.frame_layout.addWidget(self.password)

		self.home_dir = ApprovingLineFrame("./icon/user_directory_24.svg", "Enter the home directory")
		self.home_dir.frame_line_edit.textChanged.connect(self.home_dir_frame_line_edit_textChanged)
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

		self.update_butt = QPushButton("Update a selected user", self)
		self.update_butt.clicked.connect(self.update_butt_clicked)
		self.frame_layout.addWidget(self.update_butt)

		# Dialog window customization
		self.setLayout(self.frame_layout)
		self.setWindowTitle("Update user properties")
		# self.setMinimumSize(600, 480)

	def password_frame_line_edit_textChanged(self, text):
		if text == "":
			self.password.setAttention("", "")
			self.password.logic_mark = False
		else:
			# Проверка пароля
			if len(text) < 8:
				self.password.setAttention("The password is too short!", "./icon/false_24.svg")
				self.password.logic_mark = False
			elif re.match(r'^[a-zA-Z0-9]+$', text):
				has_digit = any(char.isdigit() for char in text)
				has_alpha = any(char.isalpha() for char in text)
				if has_digit and has_alpha:
					self.password.setAttention("", "./icon/check_24.svg")
				else:
					self.password.setAttention("The password is not secure!", "./icon/check_24.svg")
				self.password.logic_mark = True
			else:
				self.password.setAttention("Wrong password!", "./icon/false_24.svg")
				self.password.logic_mark = False

	def home_dir_frame_line_edit_textChanged(self, text):
		if text == "":
			self.home_dir.setAttention("", "")
			self.home_dir.logic_mark = False
		else:
			if os.path.exists(text) and os.path.isdir(text):
				self.home_dir.setAttention("", "./icon/check_24.svg")
				self.home_dir.logic_mark = True
			else:
				self.home_dir.setAttention("Wrong directory!", "./icon/false_24.svg")
				self.home_dir.logic_mark = False

	def update_butt_clicked(self):
		GlobalStates.user_db.update_user(
			self.username.text(),
			{
				"password": self.password.text(),
				"home_dir": self.home_dir.text(),
				"permission_CWD": self.permission_e.isChecked(),
				"permission_LIST": self.permission_l.isChecked(),
				"permission_RETR": self.permission_r.isChecked(),
				"permission_APPE": self.permission_a.isChecked(),
				"permission_DELE": self.permission_d.isChecked(),
				"permission_RNFR": self.permission_f.isChecked(),
				"permission_MKD": self.permission_m.isChecked(),
				"permission_STOR": self.permission_w.isChecked(),
				"permission_CHMOD": self.permission_M.isChecked(),
				"permission_MFMT": self.permission_T.isChecked()
			}
		)
		GlobalStates.user_db.set_user_date(self.username.text(), {"date_of_change": datetime.now().replace(microsecond=0)})
		self.close()

	def set_username(self, username):
		user = GlobalStates.user_db.get_user(username)
		self.username.setText(user.username)
		self.password.frame_line_edit.setText(user.password)
		self.home_dir.frame_line_edit.setText(user.home_dir)
		self.permission_e.setChecked(user.permission_CWD)
		self.permission_l.setChecked(user.permission_LIST)
		self.permission_r.setChecked(user.permission_RETR)
		self.permission_a.setChecked(user.permission_APPE)
		self.permission_d.setChecked(user.permission_DELE)
		self.permission_f.setChecked(user.permission_RNFR)
		self.permission_m.setChecked(user.permission_MKD)
		self.permission_w.setChecked(user.permission_STOR)
		self.permission_M.setChecked(user.permission_CHMOD)
		self.permission_T.setChecked(user.permission_MFMT)
