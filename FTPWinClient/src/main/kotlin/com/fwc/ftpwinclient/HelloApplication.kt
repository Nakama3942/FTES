package com.fwc.ftpwinclient

import javafx.application.Application
import javafx.fxml.FXMLLoader
import javafx.scene.Scene
import javafx.stage.Stage

class HelloApplication : Application() {
    override fun start(stage: Stage) {
        val fxmlLoader = FXMLLoader(HelloApplication::class.java.getResource("hello-view.fxml"))
        val scene = Scene(fxmlLoader.load(), 600.0, 800.0)
        stage.title = "Hello!"
        stage.scene = scene
        stage.minWidth = 600.0
        stage.minHeight = 800.0
        stage.show()
    }
}

fun main() {
    Application.launch(HelloApplication::class.java)
}