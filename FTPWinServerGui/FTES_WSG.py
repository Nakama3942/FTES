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

import sys
import pickle

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem, QLineEdit, QToolButton, QPushButton, QFileDialog
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from FTES_WSC import Server

class ServerWindow(QMainWindow):
	def __init__(self):
		super(ServerWindow, self).__init__()

		# Adding layouts
		self.main_layout = QVBoxLayout()
		self.tool_layout = QHBoxLayout()

		# Adding a tool button
		self.spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

		self.save_preset = QToolButton(self)
		self.save_preset.clicked.connect(self.save_preset_clicked)

		self.load_preset = QToolButton(self)
		self.load_preset.clicked.connect(self.load_preset_clicked)

		self.tool_layout.addSpacerItem(self.spacer)
		self.tool_layout.addWidget(self.save_preset)
		self.tool_layout.addWidget(self.load_preset)

		# Adding a Server arguments
		self.ip_address = QLineEdit(self)
		self.ip_address.setPlaceholderText("Enter the IP address")
		self.ip_address.setValidator(
			QRegularExpressionValidator(
				QRegularExpression(
					r"^192\.168\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
				)
			)
		)

		self.username = QLineEdit(self)
		self.username.setPlaceholderText("Enter the username")

		self.password = QLineEdit(self)
		self.password.setPlaceholderText("Enter the password")
		self.password.setEchoMode(QLineEdit.EchoMode.Password)

		self.home_dir = QLineEdit(self)
		self.home_dir.setPlaceholderText("Enter the home directory")

		self.log_levels = QLineEdit(self)
		self.log_levels.setPlaceholderText("Enter the logging levels")

		self.serving = QPushButton("Start server", self)
		self.serving.setCheckable(True)
		self.serving.clicked.connect(self.serving_clicked)

		# Create window layout
		self.main_layout.addLayout(self.tool_layout)
		self.main_layout.addWidget(self.ip_address)
		self.main_layout.addWidget(self.username)
		self.main_layout.addWidget(self.password)
		self.main_layout.addWidget(self.home_dir)
		self.main_layout.addWidget(self.log_levels)
		self.main_layout.addWidget(self.serving)
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.main_layout)

		# Main window customization
		self.setCentralWidget(self.central_widget)
		self.setWindowTitle("FTES WSG - File Transfer EcoSystem Windows Server Graphic")
		self.setMinimumSize(320, 240)

		#
		self.serv = None

	def save_preset_clicked(self) -> None:
		file_name, _ = QFileDialog.getSaveFileName(
			self, "Save server preset", "", "Server preset (*.preset)"
		)

		if file_name:
			with open(f"{file_name}.preset", "wb") as file:
				pickle.dump((self.ip_address.text(), self.username.text(), self.password.text(), self.home_dir.text(), self.log_levels.text()), file)

	def load_preset_clicked(self) -> None:
		file_name, _ = QFileDialog.getOpenFileName(
			self, "Load server preset", "", "Server preset (*.preset)"
		)

		if file_name:
			with open(file_name, "rb") as file:
				server_preset = pickle.load(file)
				self.ip_address.setText(server_preset[0])
				self.username.setText(server_preset[1])
				self.password.setText(server_preset[2])
				self.home_dir.setText(server_preset[3])
				self.log_levels.setText(server_preset[4])

	def serving_clicked(self) -> None:
		if self.serving.isChecked():
			self.serving.setText("Stop server")

			args = {"perm": "elradfmwMT"}
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

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ui = ServerWindow()
	ui.show()
	sys.exit(app.exec())
