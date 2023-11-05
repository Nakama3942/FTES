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

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy, QPlainTextEdit, QLabel, QLineEdit
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QMouseEvent

class ConsoleFrame(QFrame):
	def __init__(self):
		super(ConsoleFrame, self).__init__()

		self.main_layout = QVBoxLayout()
		self.main_layout.setContentsMargins(4, 4, 4, 4)
		self.main_layout.setSpacing(2)

		self.console_output = QPlainTextEdit(self)
		self.console_output.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
		self.console_output.setObjectName("console_field_in_frame")
		self.console_output.setReadOnly(True)
		self.console_output.installEventFilter(self)
		self.main_layout.addWidget(self.console_output)

		self.console_input_layout = QHBoxLayout()
		self.main_layout.addLayout(self.console_input_layout)

		self.query_string = QLabel(self)
		self.query_string.setObjectName("console_query_in_frame")
		self.query_string.setFixedSize(110, 18)
		self.query_string.installEventFilter(self)
		self.console_input_layout.addWidget(self.query_string)

		self.console_input = QLineEdit(self)
		self.console_input.setObjectName("console_line_in_frame")
		self.console_input.setFixedHeight(18)
		# todo Реализовать консоль, в которую можно вводить команды
		self.console_input.installEventFilter(self)
		self.console_input_layout.addWidget(self.console_input)

		self.setLayout(self.main_layout)
		self.setObjectName("main_frame")
		self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

	def mousePressEvent(self, event: QMouseEvent):
		super().mousePressEvent(event)
		self.console_input.setFocus()
		self.console_input.setCursorPosition(len(self.console_input.text()))

	def eventFilter(self, obj, event):
		if event.type() == QEvent.Type.FocusIn:
			self.console_output.textCursor().clearSelection()
			self.console_input.setFocus()
			self.console_input.setCursorPosition(len(self.console_input.text()))
		return super().eventFilter(obj, event)
