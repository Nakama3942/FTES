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

from PyQt6.QtWidgets import QApplication

from src.GlobalStates import GlobalStates
from ui.ServerWindow import ServerWindow

def on_about_to_quit():
	GlobalStates.user_db.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.aboutToQuit.connect(on_about_to_quit)
	with open("./ui/light.qss", "r") as style:
		app.setStyleSheet(style.read())
	ui = ServerWindow()
	ui.show()
	sys.exit(app.exec())
