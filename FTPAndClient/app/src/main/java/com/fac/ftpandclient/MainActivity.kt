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

package com.fac.ftpandclient

import android.os.Bundle
import androidx.activity.result.ActivityResultLauncher
import com.google.android.material.bottomnavigation.BottomNavigationView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.fac.ftpandclient.databinding.ActivityMainBinding

// TODO Complete permissions

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

//    private lateinit var pLauncher: ActivityResultLauncher<Array<String>>

    private lateinit var connectionModel: ConnectionModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
//        registerPermissionListener()
//        checkPermissions()

        val navView: BottomNavigationView = binding.navView

        // Accessing the ConnectionViewModel
        connectionModel = ViewModelProvider(this)[ConnectionModel::class.java]

        val navController = findNavController(R.id.nav_host_fragment_activity_main)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        val appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.navigation_login,
                R.id.navigation_client,
                R.id.navigation_server,
                R.id.navigation_server_with_saf
            )
        )

        // Subscribe to connection state changes
        connectionModel.isConnected().observe(this) { isConnected ->
            // Setting the click ability of tabs depending on isConnected
            navView.menu.findItem(R.id.navigation_client).isEnabled = isConnected
            navView.menu.findItem(R.id.navigation_client).isVisible = isConnected
            navView.menu.findItem(R.id.navigation_server).isEnabled = isConnected
            navView.menu.findItem(R.id.navigation_server).isVisible = isConnected
            navView.menu.findItem(R.id.navigation_server_with_saf).isEnabled = isConnected
            navView.menu.findItem(R.id.navigation_server_with_saf).isVisible = isConnected
        }

        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)
    }

//    private fun checkPermissions() {
//        when {
//            ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED -> {
//                Toast.makeText(this, "Permission READ_EXTERNAL_STORAGE granted", Toast.LENGTH_LONG).show()
//            }
//            else -> {
//                pLauncher.launch(arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE))
//            }
//        }
//        when {
//            ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED -> {
//                Toast.makeText(this, "Permission WRITE_EXTERNAL_STORAGE granted", Toast.LENGTH_LONG).show()
//            }
//            else -> {
//                pLauncher.launch(arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE))
//            }
//        }
//    }
//
//    private fun registerPermissionListener() {
//        pLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) {
//            if (it[Manifest.permission.READ_EXTERNAL_STORAGE] == true) {
//                Toast.makeText(this, "Permission allow", Toast.LENGTH_LONG).show()
//            }
//            else {
//                Toast.makeText(this, "Permission denied", Toast.LENGTH_LONG).show()
//            }
//        }
//    }
}