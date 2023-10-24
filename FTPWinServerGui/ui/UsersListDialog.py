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

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QTableView, QSpacerItem, QToolButton, QHeaderView, QLineEdit
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from src.GlobalStates import GlobalStates
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

		# Adding a search
		self.search_layout = QHBoxLayout()

		self.search_line = QLineEdit(self)
		self.search_line.setPlaceholderText("Enter the username who needs to be search")
		self.search_line.textChanged.connect(self.search_line_textChanged)
		self.search_layout.addWidget(self.search_line)

		self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.search_layout.addSpacerItem(self.spacer)

		self.main_layout.addLayout(self.search_layout)

		# Читаю всю базу данных
		user_list = GlobalStates.user_db.get_all_users()

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
			'Permission CHMOD',
			'Permission MFMT'
		])

		# Заполняю модель данными из списка пользователей
		for row, user in enumerate(user_list):
			self.process_table_row(row, user)

		# Создаю представление для отображения данных
		self.proxy_model = QSortFilterProxyModel()
		self.proxy_model.setSourceModel(self.user_model)  # Подставьте сюда свою модель данных

		self.user_list = QTableView(self)
		self.user_list.setModel(self.proxy_model)
		self.user_list.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
		GlobalStates.user_db.new.connect(self.user_db_new)
		GlobalStates.user_db.dirty.connect(self.user_db_dirty)
		GlobalStates.user_db.deleted.connect(self.user_db_deleted)
		self.main_layout.addWidget(self.user_list)

		# Adding a tool button
		self.tool_layout = QHBoxLayout()

		self.straight_sort_tool = QToolButton(self)
		self.straight_sort_tool.clicked.connect(self.straight_sort_tool_clicked)
		self.tool_layout.addWidget(self.straight_sort_tool)

		self.reverse_sort_tool = QToolButton(self)
		self.reverse_sort_tool.clicked.connect(self.reverse_sort_tool_clicked)
		self.tool_layout.addWidget(self.reverse_sort_tool)

		self.reset_sort_tool = QToolButton(self)
		self.reset_sort_tool.clicked.connect(self.reset_sort_tool_clicked)
		self.tool_layout.addWidget(self.reset_sort_tool)

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

	def search_line_textChanged(self):
		self.proxy_model.setFilterRegularExpression(self.search_line.text())

	def user_db_new(self, username):
		new_row = self.user_list.model().rowCount()
		updated_user = GlobalStates.user_db.get_user(username)

		self.process_table_row(new_row, updated_user)

		self.user_list.update()

	def user_db_dirty(self, username):

		selected_row = self.user_list.selectionModel().selectedIndexes()[0].row()
		updated_user = GlobalStates.user_db.get_user(username)

		self.process_table_row(selected_row, updated_user)

		self.user_list.update()

	def user_db_deleted(self, username):
		deleted_rows = self.user_list.selectionModel().selectedRows()

		# Переберите индексы в обратном порядке, чтобы не нарушить порядок при удалении строк
		for index in sorted(deleted_rows, reverse=True):
			row = index.row()
			# Удалите строку из модели
			self.user_model.removeRow(row)

		self.user_list.update()

	def straight_sort_tool_clicked(self):
		column = 0  # Номер столбца, по которому вы хотите сортировать
		order = Qt.SortOrder.AscendingOrder  # Используйте Qt.AscendingOrder или Qt.DescendingOrder
		self.user_list.model().sort(column, order)

	def reverse_sort_tool_clicked(self):
		column = 0  # Номер столбца, по которому вы хотите сортировать
		order = Qt.SortOrder.DescendingOrder  # Используйте Qt.AscendingOrder или Qt.DescendingOrder
		self.user_list.model().sort(column, order)

	def reset_sort_tool_clicked(self):
		self.user_list.model().sort(-1)  # Установить столбец сортировки на -1, чтобы вернуть исходный порядок

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
		usernames = []

		for index in selected_indexes:
			# Получаем индекс выделенной строки и столбца с именем пользователя (первый столбец)
			username_index = self.user_model.index(index.row(), 0)
			username = self.user_model.data(username_index)  # Получаем имя пользователя
			usernames.append(username)

		for username in usernames:
			GlobalStates.user_db.remove_user(username)

	def process_table_row(self, row, user):
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
