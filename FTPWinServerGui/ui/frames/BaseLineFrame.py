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

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtGui import QPixmap

class BaseLineFrame(QFrame):
	def __init__(self):
		super(BaseLineFrame, self).__init__()

		self.main_layout = QVBoxLayout()
		self.main_layout.setContentsMargins(4, 4, 4, 4)

		self.line_layout = QHBoxLayout()
		self.main_layout.addLayout(self.line_layout)

		self.line_frame_icon = QLabel(self)
		self.line_frame_icon.setObjectName("empty_background")
		# self.line_frame_icon.setPixmap(frame_icon)
		self.line_layout.addWidget(self.line_frame_icon)

		self.line_frame_field = QLineEdit(self)
		self.line_frame_field.setObjectName("frame_in_frame")
		# self.line_frame_field.setPlaceholderText(frame_placeholder)
		self.line_layout.addWidget(self.line_frame_field)

		self.setLayout(self.main_layout)
		self.setObjectName("frame_in_frame")
