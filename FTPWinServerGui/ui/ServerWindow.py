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

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLineEdit, QToolButton, QPushButton, QFileDialog
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from ui.Interceptor import Interceptor
from ui.UsersListDialog import UsersListDialog
from src.Server import Server

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

		self.ip_address = QLineEdit(self)
		self.ip_address.setPlaceholderText("Enter the IP address")
		self.ip_address.setValidator(
			QRegularExpressionValidator(
				QRegularExpression(
					r"^192\.168\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
				)
			)
		)
		self.main_layout.addWidget(self.ip_address)

		self.user_list_butt = QPushButton("Users list", self)
		self.user_list_butt.clicked.connect(self.user_list_butt_clicked)
		self.main_layout.addWidget(self.user_list_butt)

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
		if self.serving.isChecked():
			self.serving.setText("Stop server")

			args = {"perm": "elradfmwMT", "stdout": self.STDOUT, "stderr": self.STDERR}
			if self.ip_address.text() == "":
				args['ip'] = "192.168.0.102"
			else:
				args['ip'] = self.ip_address.text()
			if self.username.text() == "":
				args['username'] = "user"
			else:
				args['username'] = self.username.text()
			if self.password.text() == "":
				args['password'] = "12345"
			else:
				args['password'] = self.password.text()
			if self.home_dir.text() == "":
				args['homedir'] = "."
			else:
				args['homedir'] = self.home_dir.text()
			if self.log_levels.text() == "":
				args['log_levels'] = "info"
			else:
				args['log_levels'] = self.log_levels.text()

			# Создаем объект Popen и перенаправляем вывод
			self.serv = Server(**args)

		else:
			self.serving.setText("Start server")
			self.serv.exit()

	def intercept_writing(self, text):
		self.console.appendPlainText(text.strip())
