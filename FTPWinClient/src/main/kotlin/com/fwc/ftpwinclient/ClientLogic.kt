package com.fwc.ftpwinclient

import javafx.scene.control.TreeItem
import org.apache.commons.net.ftp.FTPClient
import org.apache.commons.net.ftp.FTPFile
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream

class ClientLogic (
	private val server: String = "127.0.0.1",
	private val port: Int = 21,
	private val username: String = "user",
	private val password: String = "12345"
) {
	private val ftpClient = FTPClient()

	fun connect() {
		try {
			ftpClient.connect(server, port)
			ftpClient.login(username, password)
		} catch (e: Exception) {
			e.printStackTrace()
		}
	}

	fun disconnect() {
		try {
			ftpClient.logout()
			ftpClient.disconnect()
		} catch (e: Exception) {
			e.printStackTrace()
		}
	}

	fun getServerSystem(serverDirectoryName: String): TreeItem<String> {
		val root = TreeItem(serverDirectoryName.split("/").last())
		val subFiles = ftpClient.listFiles(serverDirectoryName)
		if (subFiles != null) {
			for (subFile in subFiles) {
				if (subFile.isDirectory) {
					root.children.add(getServerSystem("$serverDirectoryName/${subFile.name}"))
				} else {
					root.children.add(TreeItem(subFile.name))
				}
			}
		}
		return root
	}

	fun getClientSystem(clientDirectoryName: File): TreeItem<String>
	{
		val root = TreeItem(clientDirectoryName.name.split("/").last())
		val subFiles = clientDirectoryName.listFiles()
		if (subFiles != null) {
			for (subFile in subFiles) {
				if (subFile.isDirectory) {
					root.children.add(getClientSystem(subFile))
				} else {
					root.children.add(TreeItem(subFile.name))
				}
			}
		}
		return root
	}

//	fun getServerSystem(directory: String = "/"): Array<FTPFile>? {
//		try {
////			val root = FTPFile(directory)
//			val files = ftpClient.listFiles(directory)
////			for (file in files) {
////				if (file.isDirectory) {
////
////				}
////			}
//			return files
//		} catch (e: Exception) {
//			e.printStackTrace()
//		}
//		return null
//	}

	fun run() {


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