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

import logging
import threading

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

from src.GlobalStates import GlobalStates

class Server:
	def __init__(self, ip, stdout, stderr):
		self.__ip = ip
		self.__stdout = stdout
		self.__stderr = stderr

		self.__authorizer = DummyAuthorizer()
		self.__handler = FTPHandler
		self.__server = None

		self.__server_thread = None

	def set_log(self):
		# Налаштування логування
		logger = logging.getLogger()
		logger.setLevel(logging.INFO)

		formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

		# Створення обробника для виводу в консоль
		console_handler = logging.StreamHandler()
		console_handler.setFormatter(formatter)
		console_handler.encoding = 'utf-8'
		console_handler.setStream(self.__stdout)
		logger.addHandler(console_handler)

		# Створення обробника для запису до файлу
		file_handler = logging.FileHandler(f"{GlobalStates.program_dir}\pyftpd.log", encoding="utf-8")
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

	def set_ip(self, ip):
		self.__ip = ip

	def build(self):
		self.__handler.authorizer = self.__authorizer
		# self.__handler.banner = "pyftpdlib основанный на ftpd."

		self.__server = ThreadedFTPServer((self.__ip, 21), self.__handler)

		self.__server.max_cons = 256
		self.__server.max_cons_per_ip = 5

	def add_user(self, username, password, homedir, perm):
		self.__authorizer.add_user(username, password, homedir, perm)

	def remove_all_users(self):
		self.__authorizer.user_table.clear()

	def run(self):
		self.__server_thread = threading.Thread(target=self.__server.serve_forever)
		self.__server_thread.start()

	def stop(self):
		logging.shutdown()
		self.__server.close_all()
