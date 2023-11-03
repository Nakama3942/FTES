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

from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap

from ui.frames.MarkedLineFrame import MarkedLineFrame

class MessageLineFrame(MarkedLineFrame):
	def __init__(self):
		super(MessageLineFrame, self).__init__()

		self.line_frame_message = QLabel(self)
		self.line_frame_message.setVisible(False)
		# self.line_frame_message.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		self.line_frame_message.setObjectName("attention_line")
		self.main_layout.addWidget(self.line_frame_message)

		# self.logic_mark = False
		#
		# self.main_layout = QVBoxLayout()
		# self.main_layout.setContentsMargins(4, 4, 4, 4)
		#
		# self.search_layout = QHBoxLayout()
		# self.icon_label = QLabel(self)
		# self.icon_label.setObjectName("frame_in_frame")
		# self.icon_label.setPixmap(QPixmap(frame_icon))
		# self.search_layout.addWidget(self.icon_label)
		# self.frame_line_edit = QLineEdit(self)
		# self.frame_line_edit.setObjectName("frame_in_frame")
		# self.frame_line_edit.setPlaceholderText(frame_placeholder)
		# self.search_layout.addWidget(self.frame_line_edit)
		# self.icon_label = QLabel(self)
		# self.icon_label.setObjectName("frame_in_frame")
		# self.search_layout.addWidget(self.icon_label)
		# self.main_layout.addLayout(self.search_layout)
		#
		# self.attention_line = QLabel(self)
		# self.attention_line.setVisible(False)
		# self.attention_line.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
		# self.attention_line.setObjectName("attention_line")
		# self.main_layout.addWidget(self.attention_line)
		#
		# self.setLayout(self.main_layout)

	# def setAttention(self, attention: str, pixmap: str):
	# 	if attention == "":
	# 		self.icon_label.setPixmap(QPixmap(pixmap))
	# 		self.attention_line.setText("")
	# 		self.attention_line.hide()
	# 	else:
	# 		self.icon_label.setPixmap(QPixmap(pixmap))
	# 		self.attention_line.setText(attention)
	# 		self.attention_line.show()
