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

import pickle

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLineEdit, QToolButton, QPushButton, QFileDialog
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from src.GlobalStates import GlobalStates
from src.Server import Server
from ui.Interceptor import Interceptor
from ui.UsersListDialog import UsersListDialog

class ServerWindow(QMainWindow):
	def __init__(self):
		super(ServerWindow, self).__init__()

		# initial
		self.STDOUT = Interceptor()
		self.STDERR = Interceptor()
		self.STDOUT.writing.connect(self.intercept_writing)
		self.STDERR.writing.connect(self.intercept_writing)

		# Initialization of dialog windows
		self.users_list_dialog = UsersListDialog()

		# Create a main layout
		self.main_layout = QVBoxLayout()

		self.console = QPlainTextEdit(self)
		self.console.setReadOnly(True)
		self.main_layout.addWidget(self.console)

		self.serving_layout = QHBoxLayout()

		self.ip_address = QLineEdit(self)
		self.ip_address.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		self.ip_address.setPlaceholderText("Enter the IP address")
		self.ip_address.setValidator(
			QRegularExpressionValidator(
				QRegularExpression(
					r"^192\.168\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
				)
			)
		)
		self.serving_layout.addWidget(self.ip_address)

		self.user_list_butt = QPushButton("Users list", self)
		self.user_list_butt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
		self.user_list_butt.clicked.connect(self.user_list_butt_clicked)
		self.serving_layout.addWidget(self.user_list_butt)

		self.main_layout.addLayout(self.serving_layout)

		self.serving_butt = QPushButton("Start server", self)
		self.serving_butt.setCheckable(True)
		self.serving_butt.clicked.connect(self.serving_butt_clicked)
		self.main_layout.addWidget(self.serving_butt)

		# Main window customization
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.central_widget)
		self.setWindowTitle("FTES WSG - File Transfer EcoSystem Windows Server Graphic")
		self.setMinimumSize(600, 480)

		#
		self.serv = None

	def user_list_butt_clicked(self):
		self.users_list_dialog.show()

	def serving_butt_clicked(self) -> None:
		if self.serving_butt.isChecked():
			self.serving_butt.setText("Stop server")

			args = {}
			if self.ip_address.text() != "":
				args = {"ip": self.ip_address.text(), "stdout": self.STDOUT, "stderr": self.STDERR}

			# Создаем объект Popen и перенаправляем вывод
			self.serv = Server(**args)

			users = GlobalStates.user_db.get_all_users()
			for user in users:
				permissions_dict = {
					"e": user.permission_CWD,
					"l": user.permission_LIST,
					"r": user.permission_RETR,
					"a": user.permission_APPE,
					"d": user.permission_DELE,
					"f": user.permission_RNFR,
					"m": user.permission_MKD,
					"w": user.permission_STOR,
					"M": user.permission_CHMOD,
					"T": user.permission_MFMT
				}
				permission = ''.join(key for key, value in permissions_dict.items() if value)
				self.serv.add_user(user.username, user.password, user.home_dir, permission)

			self.serv.run()

		else:
			self.serving_butt.setText("Start server")
			self.serv.stop()

	def intercept_writing(self, text):
		self.console.appendPlainText(text.strip())
