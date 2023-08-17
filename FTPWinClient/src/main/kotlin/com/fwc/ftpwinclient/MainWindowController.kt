package com.fwc.ftpwinclient

import javafx.fxml.FXML
import javafx.scene.control.*
import javafx.stage.StageStyle
import java.io.File

class MainWindowController {
    @FXML
    private lateinit var loginField: TextField
    @FXML
    private lateinit var passField: PasswordField
    @FXML
    private lateinit var serverDirectory: TextField
    @FXML
    private lateinit var clientDirectory: TextField
    @FXML
    private lateinit var serverFileSystems: TreeView<String>
    @FXML
    private lateinit var clientFileSystems: TreeView<String>
    @FXML
    private lateinit var connectButt: Button
    @FXML
    private lateinit var disconnectButt: Button
    @FXML
    private lateinit var downloadButt: Button
    @FXML
    private lateinit var uploadButt: Button
    @FXML
    private lateinit var createServerDirButt: Button
    @FXML
    private lateinit var createClientDirButt: Button
    @FXML
    private lateinit var removeServerDirButt: Button
    @FXML
    private lateinit var removeClientDirButt: Button
    @FXML
    private lateinit var dublicateToggle: ToggleButton

    private lateinit var serv: ClientLogic

    @FXML
    private fun onConnectClicked()
    {
//        serv = ClientLogic(loginField.text, passField.text)
        serv = ClientLogic("user", "12345")
        serv.connect()
        serverDirectory.text = "/"
        serverFileSystems.root = serv.getServerSystem("/")
        val selectionModel1 = serverFileSystems.selectionModel
        selectionModel1.selectionMode = SelectionMode.MULTIPLE
        clientDirectory.text = "N://"
        clientFileSystems.root = serv.getClientSystem(File("N://"))
        val selectionModel2 = clientFileSystems.selectionModel
        selectionModel2.selectionMode = SelectionMode.MULTIPLE

        serverFileSystems.setOnMouseClicked { event ->
            if (event.clickCount == 2) { // Двойной клик
                val selectedItem = serverFileSystems.selectionModel.selectedItem
                if (selectedItem != null) {
                    if (selectedItem.value == "..") {
                        serverDirectory.text = serverDirectory.text.split("/").subList(0, serverDirectory.text.split("/").size - 2).joinToString("/") + "/"
                        serverFileSystems.root = serv.openParentServerDirectory()
                    } else {
                        val newRoot = serv.openServerDirectory(selectedItem.value)
                        if (newRoot != null) {
                            serverFileSystems.root = newRoot
                            serverDirectory.text += selectedItem.value
                        }
                    }
                }
            }
        }
        clientFileSystems.setOnMouseClicked { event ->
            if (event.clickCount == 2) { // Двойной клик
                val selectedItem = clientFileSystems.selectionModel.selectedItem
                if (selectedItem != null) {
                    if (selectedItem.value == "..") {
                        clientDirectory.text = "N://" + clientDirectory.text.split("/").subList(2, clientDirectory.text.split("/").size - 2).joinToString("/")
                        if (clientDirectory.text.last().toString() != "/") {
                            clientDirectory.text += "/"
                        }
                        clientFileSystems.root = serv.openParentClientDirectory(File(clientDirectory.text))
                    } else {
                        val dir = File(clientDirectory.text + selectedItem.value)
                        if (dir.isDirectory) {
                            clientDirectory.text += selectedItem.value
                            clientFileSystems.root = serv.openClientDirectory(dir)
                        }
                    }
                }
            }
        }
    }

    @FXML
    private fun onDisconnectClicked()
    {
        serv.disconnect()
        serverDirectory.text = ""
        serverFileSystems.root = null
        clientDirectory.text = ""
        clientFileSystems.root = null
    }

    @FXML
    private fun onDownloadClicked()
    {
        val selectedItems = serverFileSystems.selectionModel.selectedItems
        serv.downloadAll(clientDirectory.text, selectedItems, !dublicateToggle.isSelected)
        updateSystems()
    }

    @FXML
    private fun onUploadClicked()
    {
        val selectedItems = clientFileSystems.selectionModel.selectedItems
        serv.uploadAll(clientDirectory.text, selectedItems, !dublicateToggle.isSelected)
        updateSystems()
    }

    @FXML
    private fun onCreateServerDirClicked()
    {
        val dialog = TextInputDialog()
        dialog.title = "Creating a new directory"
        dialog.headerText = "Enter the name of new directory"
        dialog.contentText = "Name of directory: "

        val dialogResult = dialog.showAndWait()
        dialogResult.ifPresent { directoryName ->
            if (directoryName.isNotBlank()) {
                serv.createServerDirectory(directoryName)
            } else {
                val alert = Alert(Alert.AlertType.ERROR)
                alert.title = "Error"
                alert.headerText = "The directory name cannot be empty"
                alert.contentText = "Enter the name of new directory"
                alert.buttonTypes.setAll(ButtonType.OK)
                alert.showAndWait()
                onCreateServerDirClicked()
            }
        }
        updateSystems()
    }

    @FXML
    private fun onCreateClientDirClicked()
    {
        val dialog = TextInputDialog()
        dialog.title = "Creating a new directory"
        dialog.headerText = "Enter the name of new directory"
        dialog.contentText = "Name of directory: "

        val dialogResult = dialog.showAndWait()
        dialogResult.ifPresent { directoryName ->
            if (directoryName.isNotBlank()) {
                serv.createClientDirectory(clientDirectory.text + directoryName)
            } else {
                val alert = Alert(Alert.AlertType.ERROR)
                alert.title = "Error"
                alert.headerText = "The directory name cannot be empty"
                alert.contentText = "Enter the name of new directory"
                alert.buttonTypes.setAll(ButtonType.OK)
                alert.showAndWait()
                onCreateClientDirClicked()
            }
        }
        updateSystems()
    }

    @FXML
    private fun onRemoveServerDirClicked()
    {
        val selectedItems = serverFileSystems.selectionModel.selectedItems
        for (selectedItem in selectedItems) {
            serv.removeServerPath(serverDirectory.text + selectedItem.value)
        }
        updateSystems()
    }

    @FXML
    private fun onRemoveClientDirClicked()
    {
        val selectedItems = clientFileSystems.selectionModel.selectedItems
        for (selectedItem in selectedItems) {
            serv.removeClientPath(clientDirectory.text + selectedItem.value)
        }
        updateSystems()
    }

    private fun updateSystems() {
        serverFileSystems.root = serv.updateServerDirectory()
        clientFileSystems.root = serv.updateClientDirectory(File(clientDirectory.text))
    }
}