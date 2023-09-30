package com.fac.ftpandclient

import android.os.Bundle
import com.google.android.material.bottomnavigation.BottomNavigationView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.fac.ftpandclient.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private lateinit var connectionModel: ConnectionModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

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
}