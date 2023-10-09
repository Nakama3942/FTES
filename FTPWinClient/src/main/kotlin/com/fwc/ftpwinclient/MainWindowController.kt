// Copyright © 2023 Kalynovsky Valentin. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and

package com.fwc.ftpwinclient

import javafx.fxml.FXML
import javafx.scene.control.*
import javafx.scene.layout.VBox
import java.io.File

class MainWindowController {
    @FXML
    private lateinit var connectGroup: VBox
    @FXML
    private lateinit var serverGroup: VBox
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
        try {
            serv = ClientLogic(loginField.text, passField.text)
            serv.connect()
            connectGroup.isDisable = true
            serverGroup.isDisable = false
        } catch (e: Exception) {
            val error = e.toString().split(": ")
            val alert = Alert(Alert.AlertType.ERROR)
            alert.title = "Error"
            alert.headerText = error.subList(1, error.size).joinToString(": ")
            alert.contentText = error[0]
            alert.buttonTypes.setAll(ButtonType.OK)
            alert.showAndWait()
            return
        }

        serverDirectory.text = "/"
        serverFileSystems.root = createTreeItems(serverDirectory.text, serv.openServerDirectory(serverDirectory.text)!!)
        val serverSelectionModel = serverFileSystems.selectionModel
        serverSelectionModel.selectionMode = SelectionMode.MULTIPLE

        clientDirectory.text = "N://"
        clientFileSystems.root = createTreeItems(clientDirectory.text, serv.openClientDirectory(clientDirectory.text)!!)
        val clientSelectionModel = clientFileSystems.selectionModel
        clientSelectionModel.selectionMode = SelectionMode.MULTIPLE

        serverFileSystems.setOnMouseClicked { event ->
            if (event.clickCount == 2) {
                val selectedItem = serverFileSystems.selectionModel.selectedItem
                if (selectedItem != null) {
                    if (selectedItem.value == "..") {
                        serverDirectory.text = serverDirectory.text.split("/").subList(0, serverDirectory.text.split("/").size - 2).joinToString("/") + "/"
                        serverFileSystems.root = createTreeItems(serverDirectory.text, serv.openParentServerDirectory()!!)
                    } else {
                        try {
                            serverFileSystems.root = createTreeItems(serverDirectory.text, serv.openServerDirectory(selectedItem.value)!!)
                            serverDirectory.text += selectedItem.value
                        } catch (e: Exception) {
                            // If a file was selected, not a directory, an empty list will be returned, and an error
                            // will occur during conversion. Analogue of the client "if (dir.isDirectory)"
                        }
                    }
                }
            }
        }
        clientFileSystems.setOnMouseClicked { event ->
            if (event.clickCount == 2) {
                val selectedItem = clientFileSystems.selectionModel.selectedItem
                if (selectedItem != null) {
                    if (selectedItem.value == "..") {
                        clientDirectory.text = "N://" + clientDirectory.text.split("/").subList(2, clientDirectory.text.split("/").size - 2).joinToString("/")
                        if (clientDirectory.text.last().toString() != "/") {
                            clientDirectory.text += "/"
                        }
                        clientFileSystems.root = createTreeItems(clientDirectory.text, serv.openParentClientDirectory(clientDirectory.text)!!)
                    } else {
                        val dir = File(clientDirectory.text + selectedItem.value)
                        if (dir.isDirectory) {
                            clientFileSystems.root = createTreeItems(clientDirectory.text, serv.openClientDirectory(dir.path)!!)
                            clientDirectory.text += selectedItem.value
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
        connectGroup.isDisable = false
        serverGroup.isDisable = true

        serverDirectory.text = ""
        serverFileSystems.root = null
        clientDirectory.text = ""
        clientFileSystems.root = null
    }

    @FXML
    private fun onDownloadClicked()
    {
        val selectedItems = serverFileSystems.selectionModel.selectedItems
        serv.downloadAll(clientDirectory.text, createList(selectedItems), !dublicateToggle.isSelected)
        updateSystems()
    }

    @FXML
    private fun onUploadClicked()
    {
        val selectedItems = clientFileSystems.selectionModel.selectedItems
        serv.uploadAll(clientDirectory.text, createList(selectedItems), !dublicateToggle.isSelected)
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
        serverFileSystems.root = createTreeItems(serverDirectory.text, serv.updateServerDirectory())
        clientFileSystems.root = createTreeItems(clientDirectory.text, serv.updateClientDirectory(clientDirectory.text))
    }

    private fun createTreeItems(rootName: String, list: List<String>): TreeItem<String> {
        val root = TreeItem(rootName)
        for (content in list) {
            root.children.add(TreeItem(content))
        }
        return root
    }

    private fun createList(list: List<TreeItem<String>>): List<String> {
        return list.map { it.value }
    }
}