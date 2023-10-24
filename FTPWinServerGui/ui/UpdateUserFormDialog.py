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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QCheckBox, QGroupBox, QPushButton

from src.GlobalStates import GlobalStates

class UpdateUserFormDialog(QDialog):
	def __init__(self):
		super(UpdateUserFormDialog, self).__init__()

		# Adding layouts
		self.main_layout = QVBoxLayout()

		self.username = QLineEdit(self)
		self.username.setText("")
		self.username.setReadOnly(True)
		self.main_layout.addWidget(self.username)

		self.password = QLineEdit(self)
		self.password.setPlaceholderText("Enter the password")
		self.password.setEchoMode(QLineEdit.EchoMode.Password)
		self.main_layout.addWidget(self.password)

		self.home_dir = QLineEdit(self)
		self.home_dir.setPlaceholderText("Enter the home directory")
		self.main_layout.addWidget(self.home_dir)

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
		self.permission_group.setLayout(self.permission_layout)
		self.main_layout.addWidget(self.permission_group)

		self.update_butt = QPushButton("Update a selected user", self)
		self.update_butt.clicked.connect(self.update_butt_clicked)
		self.main_layout.addWidget(self.update_butt)

		# Dialog window customization
		self.setLayout(self.main_layout)
		self.setWindowTitle("Add new user")
		self.setMinimumSize(600, 480)

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

	def set_username(self, username):
		self.username.setText(username)
		user = GlobalStates.user_db.get_user(username)
		self.password.setText(user.password)
		self.home_dir.setText(user.home_dir)
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
