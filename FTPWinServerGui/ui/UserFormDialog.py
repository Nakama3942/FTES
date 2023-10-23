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

class UserFormDialog(QDialog):
	def __init__(self):
		super(UserFormDialog, self).__init__()

		# Adding layouts
		self.main_layout = QVBoxLayout()

		self.username = QLineEdit(self)
		self.username.setPlaceholderText("Enter the username")
		self.main_layout.addWidget(self.username)

		self.password = QLineEdit(self)
		self.password.setPlaceholderText("Enter the password")
		self.password.setEchoMode(QLineEdit.EchoMode.Password)
		self.main_layout.addWidget(self.password)

		self.home_dir = QLineEdit(self)
		self.home_dir.setPlaceholderText("Enter the home directory")
		self.main_layout.addWidget(self.home_dir)

		self.permission_layout = QVBoxLayout()
		self.permission_la = QCheckBox("la", self)
		self.permission_layout.addWidget(self.permission_la)
		self.permission_lala = QCheckBox("lala", self)
		self.permission_layout.addWidget(self.permission_lala)
		self.permission_lalala = QCheckBox("lalala", self)
		self.permission_layout.addWidget(self.permission_lalala)

		self.permission_group = QGroupBox(self)
		self.permission_group.setLayout(self.permission_layout)
		self.main_layout.addWidget(self.permission_group)

		self.add_butt = QPushButton("Add new user", self)
		self.add_butt.clicked.connect(self.add_butt_clicked)
		self.main_layout.addWidget(self.add_butt)

		# Dialog window customization
		self.setLayout(self.main_layout)
		self.setWindowTitle("Add new user")
		self.setMinimumSize(600, 480)

	def add_butt_clicked(self):
		print("Add new user")
