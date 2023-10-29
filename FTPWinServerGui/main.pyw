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
import os

from PyQt6.QtWidgets import QApplication

from src.GlobalStates import GlobalStates
from ui.ServerWindow import ServerWindow
from ui.UserDb import UserDb

if __name__ == '__main__':
	GlobalStates.program_dir = os.path.expandvars("%APPDATA%\FTPWinServerGui")

	# Теперь вы можете создать директорию в AppData\Roaming для вашего приложения
	if not os.path.exists(GlobalStates.program_dir):
		os.makedirs(GlobalStates.program_dir)

	GlobalStates.user_db = UserDb(GlobalStates.program_dir)

	app = QApplication(sys.argv)
	with open("./ui/light.qss", "r") as style:
		app.setStyleSheet(style.read())
	ui = ServerWindow()
	ui.show()
	sys.exit(app.exec())
