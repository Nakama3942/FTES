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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QTableView, QAbstractItemView, QSpacerItem, QToolButton, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from src.UserDb import UserDb
from ui.CreateUserFormDialog import CreateUserFormDialog
from ui.UpdateUserFormDialog import UpdateUserFormDialog

class UsersListDialog(QDialog):
	def __init__(self):
		super(UsersListDialog, self).__init__()

		# Initialization of dialog windows
		self.create_user_form_dialog = CreateUserFormDialog()
		self.update_user_form_dialog = UpdateUserFormDialog()

		# Adding layouts
		self.main_layout = QVBoxLayout()

		# Читаю всю базу данных
		user_db = UserDb()
		user_list = user_db.get_all_users()
		user_db.close()

		# Создаю модель данных
		self.user_model = QStandardItemModel(len(user_list), 13)
		self.user_model.setHorizontalHeaderLabels([
			'Username',
			'Password',
			'Home Dir',
			'Permission CWD',
			'Permission LIST',
			'Permission RETR',
			'Permission APPE',
			'Permission DELE',
			'Permission RNFR',
			'Permission MKD',
			'Permission STOR',
			'Permission SITE CHMOD',
			'Permission SITE MFMT'
		])

		# Заполняю модель данными из списка пользователей
		for row, user in enumerate(user_list):
			for col, data in enumerate([
				user.username,
				user.password,
				user.home_dir,
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
				item = QStandardItem(str(data))
				item.setEditable(False)
				if col != 0:
					item.setSelectable(False)
				self.user_model.setItem(row, col, item)

		# Создаю представление для отображения данных
		self.user_list = QTableView(self)
		self.user_list.setModel(self.user_model)
		self.user_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		self.main_layout.addWidget(self.user_list)

		# Adding a tool button
		self.tool_layout = QHBoxLayout()

		self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.tool_layout.addSpacerItem(self.spacer)

		self.add_user = QToolButton(self)
		self.add_user.clicked.connect(self.add_user_clicked)
		self.tool_layout.addWidget(self.add_user)

		self.update_user = QToolButton(self)
		self.update_user.clicked.connect(self.update_user_clicked)
		self.tool_layout.addWidget(self.update_user)

		self.remove_user = QToolButton(self)
		self.remove_user.clicked.connect(self.remove_user_clicked)
		self.tool_layout.addWidget(self.remove_user)

		self.main_layout.addLayout(self.tool_layout)

		# Dialog window customization
		self.setLayout(self.main_layout)
		self.setWindowTitle("Server users")
		self.setMinimumSize(600, 480)

	def add_user_clicked(self):
		self.create_user_form_dialog.show()

	def update_user_clicked(self):
		selected_indexes = self.user_list.selectionModel().selectedRows()
		if len(selected_indexes) == 0:
			return
		username_index = self.user_model.index(selected_indexes[0].row(), 0)
		username = self.user_model.data(username_index)
		self.update_user_form_dialog.set_username(username)
		self.update_user_form_dialog.show()

	def remove_user_clicked(self):
		selected_indexes = self.user_list.selectionModel().selectedRows()
		for index in selected_indexes:
			# Получаем индекс выделенной строки и столбца с именем пользователя (первый столбец)
			username_index = self.user_model.index(index.row(), 0)
			username = self.user_model.data(username_index)  # Получаем имя пользователя
			# Теперь у вас есть имя пользователя, и вы можете выполнить удаление или другие операции с ним.
			# Например, вызов метода remove_user(username) из вашей модели данных.
			user_db = UserDb()
			user_db.remove_user(username)
			user_db.close()
