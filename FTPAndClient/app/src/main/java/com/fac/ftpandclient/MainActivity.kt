package com.fac.ftpandclient

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import com.google.android.material.bottomnavigation.BottomNavigationView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.fac.ftpandclient.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private lateinit var pLauncher: ActivityResultLauncher<Array<String>>

    private lateinit var connectionModel: ConnectionModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        registerPermissionListener()
        checkPermissions()

        val navView: BottomNavigationView = binding.navView

        // Получите доступ к ConnectionViewModel
        connectionModel = ViewModelProvider(this).get(ConnectionModel::class.java)

        val navController = findNavController(R.id.nav_host_fragment_activity_main)
        // Passing each menu ID as a set of Ids because each
        // menu should be considered as top level destinations.
        val appBarConfiguration = AppBarConfiguration(
            setOf(
                R.id.navigation_login, R.id.navigation_client, R.id.navigation_server
            )
        )

        // Подпишитесь на изменения состояния подключения
        connectionModel.isConnected().observe(this, Observer { isConnected ->
            // Здесь можно настроить кликабельность вкладок в зависимости от isConnected
            navView.menu.findItem(R.id.navigation_client).isEnabled = isConnected
            navView.menu.findItem(R.id.navigation_client).isVisible = isConnected
            navView.menu.findItem(R.id.navigation_server).isEnabled = isConnected
            navView.menu.findItem(R.id.navigation_server).isVisible = isConnected
        })

        setupActionBarWithNavController(navController, appBarConfiguration)
        navView.setupWithNavController(navController)
    }

    private fun checkPermissions() {
        when {
            ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED -> {
                Toast.makeText(this, "Permission READ_EXTERNAL_STORAGE granted", Toast.LENGTH_LONG).show()
            }
            else -> {
                pLauncher.launch(arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE))
            }
        }
        when {
            ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED -> {
                Toast.makeText(this, "Permission WRITE_EXTERNAL_STORAGE granted", Toast.LENGTH_LONG).show()
            }
            else -> {
                pLauncher.launch(arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE))
            }
        }
    }

    private fun registerPermissionListener() {
        pLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) {
            if (it[Manifest.permission.READ_EXTERNAL_STORAGE] == true) {
                Toast.makeText(this, "Permission allow", Toast.LENGTH_LONG).show()
            }
            else {
                Toast.makeText(this, "Permission denied", Toast.LENGTH_LONG).show()
            }
        }
    }
}