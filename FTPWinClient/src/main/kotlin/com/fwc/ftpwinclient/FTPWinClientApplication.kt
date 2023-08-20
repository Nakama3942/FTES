package com.fwc.ftpwinclient

import javafx.application.Application
import javafx.fxml.FXMLLoader
import javafx.scene.Scene
import javafx.stage.Stage

class FTPWinClientApplication : Application() {
    override fun start(stage: Stage) {
        val fxmlLoader = FXMLLoader(FTPWinClientApplication::class.java.getResource("main-window.fxml"))
        val scene = Scene(fxmlLoader.load(), 600.0, 800.0)
        stage.title = "File Transfer EcoSystem Windows Client (FTES WC)"
        stage.scene = scene
        stage.minWidth = 600.0
        stage.minHeight = 800.0
        stage.show()
    }
}

fun main() {
    Application.launch(FTPWinClientApplication::class.java)
}