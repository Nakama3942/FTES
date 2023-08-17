package com.fwc.ftpwinclient

import javafx.scene.control.TreeItem
import org.apache.commons.net.ftp.FTPClient
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream

class ClientLogic (
	private val username: String = "user",
	private val password: String = "12345"
) {
	private val server: String = "127.0.0.1"
	private val port: Int = 21
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
		val root = TreeItem(serverDirectoryName)
		root.children.add(TreeItem(".."))
		val subFiles = ftpClient.listFiles(ftpClient.printWorkingDirectory())
		if (subFiles != null) {
			for (subFile in subFiles) {
				if (subFile.isDirectory) {
					root.children.add(TreeItem("${subFile.name}/"))
				} else {
					root.children.add(TreeItem(subFile.name))
				}
			}
		}
		return root
	}

	fun openServerDirectory(serverDirectoryName: String): TreeItem<String>? {
		if (ftpClient.changeWorkingDirectory(serverDirectoryName)) {
			return getServerSystem(serverDirectoryName)
		}
		return null
	}

	fun openParentServerDirectory(): TreeItem<String>? {
		if (ftpClient.changeToParentDirectory()) {
			return getServerSystem(ftpClient.printWorkingDirectory().split("/").last())
		}
		return null
	}

	fun updateServerDirectory(): TreeItem<String> {
		return getServerSystem(ftpClient.printWorkingDirectory().split("/").last())
	}
	
	fun getClientSystem(clientDirectoryName: File): TreeItem<String>
	{
		val root = TreeItem(clientDirectoryName.name)
		root.children.add(TreeItem(".."))
		val subFiles = clientDirectoryName.listFiles()
		if (subFiles != null) {
			for (subFile in subFiles) {
				if (subFile.isDirectory) {
					root.children.add(TreeItem("${subFile.name}/"))
				} else {
					root.children.add(TreeItem(subFile.name))
				}
			}
		}
		return root
	}

	fun openClientDirectory(clientDirectoryName: File): TreeItem<String>? {
		if (clientDirectoryName.isDirectory) {
			return getClientSystem(clientDirectoryName)
		}
		return null
	}

	fun openParentClientDirectory(clientDirectoryName: File): TreeItem<String>? {
		if (clientDirectoryName.isDirectory) {
			return getClientSystem(clientDirectoryName)
		}
		return null
	}

	fun updateClientDirectory(clientDirectoryName: File): TreeItem<String> {
		return getClientSystem(clientDirectoryName)
	}

	fun downloadFile(serverFilePath: String, clientFilePath: String) {
		val localFileOutputStream = FileOutputStream(clientFilePath)
		ftpClient.retrieveFile(serverFilePath, localFileOutputStream)
		localFileOutputStream.close()
	}

	fun uploadFile(serverFilePath: String, clientFilePath: String) {
		val localFileInputStream = FileInputStream(clientFilePath)
		ftpClient.storeFile(serverFilePath, localFileInputStream)
		localFileInputStream.close()
	}

	fun removeServerFile(serverFilePath: String) {
		ftpClient.deleteFile(serverFilePath)
	}

	fun removeClientFile(clientFilePath: String) {
		File(clientFilePath).delete()
	}

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