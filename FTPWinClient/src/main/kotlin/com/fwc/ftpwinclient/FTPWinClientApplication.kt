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