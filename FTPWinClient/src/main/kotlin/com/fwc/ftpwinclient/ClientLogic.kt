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

	fun downloadAll(clientPath: String, serverFiles: List<TreeItem<String>>) {
		for (serverFile in serverFiles) {
			if (serverFile.value == "..") {
				continue
			}
			download(clientPath, serverFile.value)
		}
	}

	private fun download(clientPath: String, serverFile: String) {
		val sourcePath = ftpClient.printWorkingDirectory() + "/" + serverFile
		val targetPath = File(clientPath, serverFile)

		if (ftpClient.mlistFile(sourcePath).isFile) {
			// Элемент - файл
			downloadFile(sourcePath, targetPath.path)
		} else {
			// Элемент - директория
			createClientDirectory(targetPath.path)
			ftpClient.changeWorkingDirectory(sourcePath)
			for (file in ftpClient.listFiles()) {
				download(targetPath.path, file.name)
			}
			openParentServerDirectory()
		}
	}

	private fun downloadFile(serverFilePath: String, clientFilePath: String) {
		val localFileOutputStream = FileOutputStream(clientFilePath)
		ftpClient.retrieveFile(serverFilePath, localFileOutputStream)
		localFileOutputStream.close()
	}

	fun uploadAll(clientPath: String, serverFiles: List<TreeItem<String>>) {
	}

	private fun upload(clientPath: String, serverFile: String) {
	}

	private fun uploadFile(serverFilePath: String, clientFilePath: String) {
		val localFileInputStream = FileInputStream(clientFilePath)
		ftpClient.storeFile(serverFilePath, localFileInputStream)
		localFileInputStream.close()
	}

//
//	fun uploadAll(clientDirectoryName: File): TreeItem<String>
//	{
//		val root = TreeItem(clientDirectoryName.name.split("/").last())
//		val subFiles = clientDirectoryName.listFiles()
//		if (subFiles != null) {
//			for (subFile in subFiles) {
//				if (subFile.isDirectory) {
//					root.children.add(getClientSystem(subFile))
//				} else {
//					root.children.add(TreeItem(subFile.name))
//				}
//			}
//		}
//		return root
//	}

	fun createServerDirectory(newServerDirectory: String) {
		ftpClient.makeDirectory(newServerDirectory)
	}

	fun createClientDirectory(newClientDirectory: String) {
		File(newClientDirectory).mkdirs()
	}

	fun removeServerFile(serverFilePath: String) {
		ftpClient.deleteFile(serverFilePath)
	}

	fun removeClientFile(clientFilePath: String) {
		File(clientFilePath).delete()
	}
}