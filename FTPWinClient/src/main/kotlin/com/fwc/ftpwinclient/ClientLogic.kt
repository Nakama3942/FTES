package com.fwc.ftpwinclient

import org.apache.commons.net.ftp.FTPClient
import java.io.FileInputStream
import java.io.FileOutputStream

class ClientLogic (
	private val server: String = "127.0.0.1",
	private val port: Int = 21,
	private val username: String = "user",
	private val password: String = "12345"
) {
	fun run() {
		val ftpClient = FTPClient()

		try {
			ftpClient.connect(server, port)
			ftpClient.login(username, password)

			// Вы можете изменить директорию, используя ftpClient.changeWorkingDirectory("путь_к_директории")

//			// Пример загрузки файла на сервер
//			val fileInputStream = FileInputStream("path/to/local/file.txt")
//			ftpClient.storeFile("remote/file.txt", fileInputStream)
//			fileInputStream.close()
//
//			// Пример скачивания файла с сервера
//			val localFileOutputStream = FileOutputStream("path/to/local/downloaded_file.txt")
//			ftpClient.retrieveFile("remote/downloaded_file.txt", localFileOutputStream)
//			localFileOutputStream.close()

			ftpClient.logout()
		} catch (e: Exception) {
			e.printStackTrace()
		} finally {
			if (ftpClient.isConnected) {
				try {
					ftpClient.disconnect()
				} catch (e: Exception) {
					e.printStackTrace()
				}
			}
		}
	}
}