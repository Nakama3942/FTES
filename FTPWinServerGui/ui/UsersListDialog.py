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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QListView, QSpacerItem, QToolButton

from ui.UserFormDialog import UserFormDialog

class UsersListDialog(QDialog):
	def __init__(self):
		super(UsersListDialog, self).__init__()

		# Initialization of dialog windows
		self.user_form_dialog = UserFormDialog()

		# Adding layouts
		self.main_layout = QVBoxLayout()

		self.user_list = QListView(self)
		self.main_layout.addWidget(self.user_list)

		# Adding a tool button
		self.tool_layout = QHBoxLayout()

		self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.tool_layout.addSpacerItem(self.spacer)

		self.add_user = QToolButton(self)
		self.add_user.clicked.connect(self.add_user_clicked)
		self.tool_layout.addWidget(self.add_user)

		self.remove_user = QToolButton(self)
		self.remove_user.clicked.connect(self.remove_user_clicked)
		self.tool_layout.addWidget(self.remove_user)

		self.main_layout.addLayout(self.tool_layout)

		# Dialog window customization
		self.setLayout(self.main_layout)
		self.setWindowTitle("Server users")
		self.setMinimumSize(600, 480)

	def add_user_clicked(self):
		self.user_form_dialog.show()

	def remove_user_clicked(self):
		pass
