package com.fwc.ftpwinclient

import javafx.fxml.FXML
import javafx.scene.control.Button
import javafx.scene.control.PasswordField
import javafx.scene.control.TextField
import javafx.scene.control.TreeItem
import javafx.scene.control.TreeView
import java.io.File

class MainWindowController {
    @FXML
    private lateinit var loginField: TextField
    @FXML
    private lateinit var passField: PasswordField
    @FXML
    private lateinit var serverFileSystems: TreeView<String>
    @FXML
    private lateinit var clientFileSystems: TreeView<String>
    @FXML
    private lateinit var connectButt: Button
    @FXML
    private lateinit var disconnectButt: Button

    private lateinit var serv: ClientLogic

    @FXML
    private fun onConnectClicked()
    {
        serverFileSystems.root = createNode(File("."))
        clientFileSystems.root = createNode(File(".."))
        serv = ClientLogic()
        serv.run()
    }

    @FXML
    private fun onDisconnectClicked()
    {
        serverFileSystems.root = null
        clientFileSystems.root = null
    }

    private fun createNode(directory: File): TreeItem<String>
    {
        val root = TreeItem(directory.name)
        if (directory.isDirectory) {
            val files = directory.listFiles()
            if (files != null) {
                for (childFile in files) {
                    root.children.add(createNode(childFile))
                }
            }
        }
        return root
    }
}