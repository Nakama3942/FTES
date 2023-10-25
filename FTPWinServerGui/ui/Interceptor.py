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

from PyQt6.QtCore import QObject, pyqtSignal

class Interceptor(QObject):
	writing = pyqtSignal(str)

	def __init__(self):
	# def __init__(self, io_stream):
		super().__init__()

		# self.io_stream = io_stream

	def write(self, text):
		# self.io_stream.write(text)
		self.writing.emit(text)

	def flush(self):
		pass
		# self.io_stream.flush()
