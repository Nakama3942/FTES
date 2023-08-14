import os
# import logging
import keyboard
import threading
import argparse

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer

__server = None

class Server:
	def __init__(self, username, password, homedir, perm):
		self.__username = username
		self.__password = password
		self.__homedir = homedir
		self.__perm = perm

		self.__authorizer = DummyAuthorizer()
		self.__handler = FTPHandler
		self.__server = None

		self.__starter = None
		self.__stopper = None

		self.__start()

	def __start(self):
		self.__build()
		self.run()
		self.stop()

	def __build(self):
		self.__authorizer.add_user(
			self.__username,
			self.__password,
			self.__homedir,
			perm=self.__perm
		)
		self.__authorizer.add_anonymous(os.getcwd())

		self.__handler.authorizer = self.__authorizer

		# logging.basicConfig(filename='pyftpd.log', level=logging.DEBUG)
		# self.__handler.log_prefix = 'XXX [%(username)s]@%(remote_ip)s'

		self.__handler.banner = "pyftpdlib основанный на ftpd."

		self.__server = ThreadedFTPServer(('127.0.0.1', 21), self.__handler)

		self.__server.max_cons = 256
		self.__server.max_cons_per_ip = 5

	def run(self):
		self.__starter = threading.Thread(target=self.__server.serve_forever)
		self.__starter.start()

	def stop(self):
		keyboard.wait("esc")
		self.__server.close_all()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='FTP Server')
	parser.add_argument('-u', '--username', default='user', required=True, help='Username')
	parser.add_argument('-p', '--password', default='12345', required=False, help='Password')
	parser.add_argument('-d', '--homedir', default='.', required=False, help='Home directory')

	args = parser.parse_args()

	serv = Server(args.username, args.password, args.homedir, 'elradfmwMT')

# if __name__ == '__main__':
# # экземпляр фиктивного средства авторизации
# # для управления "виртуальными" пользователями
# authorizer = DummyAuthorizer()

# # добавляем нового пользователя, имеющего полные права доступа `r/w`
# # и анонимного пользователя, для которого FS доступна только для чтения
# authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
# authorizer.add_anonymous(os.getcwd())

# # экземпляр класса обработчика FTP
# handler = FTPHandler
# handler.authorizer = authorizer

# # запись логов в файл '/var/log/pyftpd.log'
# logging.basicConfig(filename='pyftpd.log', level=logging.DEBUG)
# handler.log_prefix = 'XXX [%(username)s]@%(remote_ip)s'

# # настраиваемый баннер (строка, возвращаемая при подключении клиента)
# handler.banner = "pyftpdlib основанный на ftpd."

# masquerade-адрес и диапазон портов, которые будут использоваться
# для пассивных подключений. Строки ниже нужно раскомментировать
# если вы находитесь за NAT (masquerade_address укажите свой).
# handler.masquerade_address = '151.25.42.11'
# handler.passive_ports = range(60000, 65535)

# # экземпляр класса FTP-сервера, который слушает `0.0.0.0:2121`
# address = ('127.0.0.1', 21)
# server = FTPServer(address, handler)

# # лимиты на соединения
# server.max_cons = 256
# server.max_cons_per_ip = 5

# server.serve_forever()
