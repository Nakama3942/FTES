package com.fac.ftpandclient

import org.apache.commons.net.ftp.FTPClient
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream

class LoginException(message: String) : Exception(message)

class ClientLogic(
	private val username: String = "user",
	private val password: String = "12345",
	private val server: String = "192.168.0.102"
) {
//	private val server: String = "127.0.0.1"
//	private val server: String = "192.168.0.102"
	private val port: Int = 21
	private val ftpClient = FTPClient()

	fun connect() {
		ftpClient.connect(server, port)
		if (!ftpClient.login(username, password)) {
			disconnect()
			throw LoginException("USER '$username' failed login.")
		}
	}

	fun disconnect() {
		ftpClient.logout()
		ftpClient.disconnect()
	}

	private fun getServerSystem(): List<String> {
		val directoryContent = mutableListOf("..")
		val subFiles = ftpClient.listFiles(ftpClient.printWorkingDirectory())
		if (subFiles != null) {
			for (subFile in subFiles) {
				if (subFile.isDirectory) {
					directoryContent.add("${subFile.name}/")
				} else {
					directoryContent.add(subFile.name)
				}
			}
		}
		return directoryContent
	}

	fun openServerDirectory(serverDirectoryName: String): List<String>? {
		if (ftpClient.changeWorkingDirectory(serverDirectoryName)) {
			return getServerSystem()
		}
		return null
	}

	fun openParentServerDirectory(): List<String>? {
		if (ftpClient.changeToParentDirectory()) {
			return getServerSystem()
		}
		return null
	}

	fun updateServerDirectory(): List<String> {
		return getServerSystem()
	}

	private fun getClientSystem(clientDirectoryName: String): List<String>
	{
		val directory = File(clientDirectoryName)
		val directoryContent = mutableListOf("..")
		val subFiles = directory.listFiles()
		if (subFiles != null) {
			for (subFile in subFiles) {
				if (subFile.isDirectory) {
					directoryContent.add("${subFile.name}/")
				} else {
					directoryContent.add(subFile.name)
				}
			}
		}
		return directoryContent
	}

	fun openClientDirectory(clientDirectoryName: String): List<String>? {
		if (File(clientDirectoryName).isDirectory) {
			return getClientSystem(clientDirectoryName)
		}
		return null
	}

	fun openParentClientDirectory(clientDirectoryName: String): List<String>? {
		if (File(clientDirectoryName).isDirectory) {
			return getClientSystem(clientDirectoryName)
		}
		return null
	}

	fun updateClientDirectory(clientDirectoryName: String): List<String> {
		return getClientSystem(clientDirectoryName)
	}

	fun getServerFileSize(filePath: String): Long {
//		val fileInfo = ftpClient.mlistFile(filePath)
//		return fileInfo.size
		return ftpClient.mlistFile(filePath).size
	}

	fun getClientFileSize(filePath: String): Long {
		return File(filePath).length()
	}

	fun downloadAll(clientPath: String, serverFiles: List<String>, clear: Boolean) {
		for (serverFile in serverFiles) {
			if (serverFile == "..") {
				continue
			}
			download(clientPath, serverFile)
			if (clear) {
				removeServerPath(ftpClient.printWorkingDirectory() + "/" + serverFile)
			}
		}
	}

	private fun download(clientPath: String, serverFile: String) {
		val sourcePath = ftpClient.printWorkingDirectory() + "/" + serverFile
		val targetPath = File(clientPath, serverFile)

		if (ftpClient.mlistFile(sourcePath).isFile) {
			// This element a file
			val localFileOutputStream = FileOutputStream(targetPath.path)
			ftpClient.retrieveFile(sourcePath, localFileOutputStream)
			localFileOutputStream.close()
		} else {
			// This element a directory
			createClientDirectory(targetPath.path)
			ftpClient.changeWorkingDirectory(sourcePath)
			for (file in ftpClient.listFiles()) {
				download(targetPath.path, file.name)
			}
			openParentServerDirectory()
		}
	}

	fun uploadAll(clientPath: String, clientFiles: List<String>, clear: Boolean) {
		for (clientFile in clientFiles) {
			if (clientFile == "..") {
				continue
			}
			upload(clientPath, clientFile)
			if (clear) {
				removeClientPath(File(clientPath, clientFile).path)
			}
		}
	}

	private fun upload(clientPath: String, clientFile: String) {
		val sourcePath = File(clientPath, clientFile)
		val targetPath = ftpClient.printWorkingDirectory() + "/" + clientFile

		if (sourcePath.isFile) {
			// This element a file
			val localFileInputStream = FileInputStream(sourcePath.path)
			ftpClient.storeFile(targetPath, localFileInputStream)
			localFileInputStream.close()
		} else {
			// This element a directory
			createServerDirectory(targetPath)
			ftpClient.changeWorkingDirectory(targetPath)
			for (file in sourcePath.listFiles()!!) {
				upload(sourcePath.path, file.name)
			}
			openParentServerDirectory()
		}
	}

	fun createServerDirectory(newServerDirectory: String) {
		ftpClient.makeDirectory(newServerDirectory)
	}

	fun createClientDirectory(newClientDirectory: String) {
		File(newClientDirectory).mkdirs()
	}

	fun removeServerPath(serverFilePath: String) {
		if (ftpClient.mlistFile(serverFilePath).isDirectory) {
			// This element a directory
			ftpClient.changeWorkingDirectory(serverFilePath)
			for (file in ftpClient.listFiles()) {
				removeServerPath(file.name)
			}
			openParentServerDirectory()
			ftpClient.removeDirectory(serverFilePath)
		} else {
			// This element a file
			ftpClient.deleteFile(ftpClient.mlistFile(serverFilePath).name)
		}
	}

	fun removeClientPath(clientFilePath: String) {
		File(clientFilePath).deleteRecursively()
	}
}