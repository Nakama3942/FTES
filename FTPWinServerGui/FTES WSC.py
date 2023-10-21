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

import os
import logging
import keyboard
import threading
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

class Server:
	def __init__(self, ip, username, password, homedir, perm, log_levels):
		self.__ip = ip
		self.__username = username
		self.__password = password
		self.__homedir = homedir
		self.__perm = perm
		self.__log_levels = log_levels

		self.__authorizer = DummyAuthorizer()
		self.__handler = FTPHandler
		self.__server = None

		self.__starter = None
		self.__stopper = None

		self.__start()

	def __start(self):
		self.__build()
		self.__log()
		self.__run()
		self.__expectant()

	def __build(self):
		self.add_user(
			self.__username,
			self.__password,
			self.__homedir,
			self.__perm
		)

		self.__handler.authorizer = self.__authorizer

		self.__handler.banner = "pyftpdlib основанный на ftpd."

		self.__server = ThreadedFTPServer((self.__ip, 21), self.__handler)

		self.__server.max_cons = 256
		self.__server.max_cons_per_ip = 5

	def __log(self):
		# Настройка логгирования
		logger = logging.getLogger()
		match self.__log_levels:
			case "info":
				logger.setLevel(logging.INFO)
			case "debug":
				logger.setLevel(logging.DEBUG)
			case "warning":
				logger.setLevel(logging.WARNING)
			case "error":
				logger.setLevel(logging.ERROR)
			case "critical":
				logger.setLevel(logging.CRITICAL)
			case "fatal":
				logger.setLevel(logging.FATAL)
			case "notset":
				logger.setLevel(logging.NOTSET)

		formatter = logging.Formatter('[%(levelname)s %(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

		# Создание обработчика для вывода в консоль
		console_handler = logging.StreamHandler()
		console_handler.setFormatter(formatter)
		console_handler.encoding = 'utf-8'
		logger.addHandler(console_handler)

		# Создание обработчика для записи в файл
		file_handler = logging.FileHandler('pyftpd.log', encoding="utf-8")
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

	def __run(self):
		self.__starter = threading.Thread(target=self.__server.serve_forever)
		self.__starter.start()

	def __expectant(self):
		while True:
			event = keyboard.read_event()
			if event.event_type == keyboard.KEY_DOWN:
				match event.name:
					case "esc":
						logging.shutdown()
						self.__server.close_all()
						break
					case "a":
						self.add_user(
							input("Enter the user name: "),
							input("Enter the user password: "),
							input("Enter the user home directory: "),
							input("Enter the user permissions: "),
						)

	def add_user(self, username, password, homedir, perm):
		self.__authorizer.add_user(username, password, homedir, perm)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='FTP Server')
	parser.add_argument('-a', '--address', default='192.168.0.102', required=False, help='IP address')
	parser.add_argument('-u', '--username', default='user', required=False, help='Username')
	parser.add_argument('-p', '--password', default='12345', required=False, help='Password')
	parser.add_argument('-d', '--homedir', default='.', required=False, help='Home directory')
	parser.add_argument('-l', '--log', default='info', required=False, help='Logger levels')

	args = parser.parse_args()

	serv = Server(args.address, args.username, args.password, args.homedir, 'elradfmwMT', args.log)
