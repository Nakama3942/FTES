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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QLineEdit, QCheckBox, QGroupBox, QPushButton, QLabel, QFrame

from src.GlobalStates import GlobalStates

class CreateUserFormDialog(QDialog):
	def __init__(self):
		super(CreateUserFormDialog, self).__init__()

		# Adding layouts
		self.frame_layout = QVBoxLayout()

		self.attention_line = QLabel(self)
		self.attention_line.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		self.attention_line.setText("Once the user is created, the name cannot be changed!")
		self.attention_line.setObjectName("attention_line")
		self.frame_layout.addWidget(self.attention_line)

		self.username = QLineEdit(self)
		self.username.setPlaceholderText("Enter the username")
		self.frame_layout.addWidget(self.username)

		self.password = QLineEdit(self)
		self.password.setPlaceholderText("Enter the password")
		self.password.setEchoMode(QLineEdit.EchoMode.Password)
		self.frame_layout.addWidget(self.password)

		self.home_dir = QLineEdit(self)
		self.home_dir.setPlaceholderText("Enter the home directory")
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
		self.permission_group.setTitle("Permission")
		self.permission_group.setLayout(self.permission_layout)
		self.frame_layout.addWidget(self.permission_group)

		self.add_layout = QHBoxLayout()

		self.add_butt = QPushButton("Add new user", self)
		self.add_butt.clicked.connect(self.add_butt_clicked)
		self.add_layout.addWidget(self.add_butt)

		self.apply_butt = QPushButton("Add and apply", self)
		self.apply_butt.clicked.connect(self.apply_butt_clicked)
		self.add_layout.addWidget(self.apply_butt)

		self.frame_layout.addLayout(self.add_layout)

		self.frame = QFrame()
		self.frame.setLayout(self.frame_layout)
		self.frame.setContentsMargins(0, 0, 0, 0)

		self.main_layout = QVBoxLayout()
		self.main_layout.addWidget(self.frame)

		# Dialog window customization
		self.setLayout(self.main_layout)
		self.setWindowTitle("Add new user")
		self.setMinimumSize(600, 480)

	def add_butt_clicked(self):
		GlobalStates.user_db.create_user(
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

	def apply_butt_clicked(self):
		self.add_butt_clicked()
		self.close()
