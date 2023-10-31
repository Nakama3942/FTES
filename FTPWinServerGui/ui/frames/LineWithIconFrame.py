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

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtGui import QPixmap

class LineWithIconFrame(QFrame):
	def __init__(self, frame_icon, frame_placeholder):
		super(LineWithIconFrame, self).__init__()

		self.search_layout = QHBoxLayout()
		self.search_layout.setContentsMargins(4, 4, 4, 4)

		self.icon_label = QLabel(self)
		self.icon_label.setObjectName("frame_in_frame")
		self.icon_label.setPixmap(QPixmap(frame_icon))
		self.search_layout.addWidget(self.icon_label)

		self.frame_line_edit = QLineEdit(self)
		self.frame_line_edit.setObjectName("frame_in_frame")
		self.frame_line_edit.setPlaceholderText(frame_placeholder)
		self.search_layout.addWidget(self.frame_line_edit)

		self.setLayout(self.search_layout)
