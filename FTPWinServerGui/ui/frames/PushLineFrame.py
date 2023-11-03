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

from PyQt6.QtWidgets import QToolButton
from PyQt6.QtGui import QPixmap, QIcon

from ui.frames.BaseLineFrame import BaseLineFrame

class PushLineFrame(BaseLineFrame):
	def __init__(self):
		super(PushLineFrame, self).__init__()

		self.line_frame_tool = QToolButton(self)
		self.line_frame_tool.setFixedSize(25, 25)
		self.line_frame_tool.setCheckable(True)
		self.line_frame_tool.setObjectName("frame_in_frame")
		self.line_layout.addWidget(self.line_frame_tool)
