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
