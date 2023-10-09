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

package com.fac.ftpandclient.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.Spinner
import android.widget.Toast
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat
import androidx.core.content.ContextCompat
import androidx.core.view.isVisible
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.ConnectionModel
import com.fac.ftpandclient.R
import com.fac.ftpandclient.databinding.FragmentLoginBinding
import com.fac.ftpandclient.ImportantData

class LoginFragment : Fragment() {

    private var _binding: FragmentLoginBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var serv: ClientLogic
    private lateinit var connectionModel: ConnectionModel

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentLoginBinding.inflate(inflater, container, false)
        val root: View = binding.root

        // Accessing the ConnectionViewModel
        connectionModel = ViewModelProvider(requireActivity())[ConnectionModel::class.java]

        // Links to interface buttons
        val languageBox = root.findViewById<Spinner>(R.id.languageBox)
        val themeSwitch = root.findViewById<SwitchCompat>(R.id.themeSwitch)
        val rootDir = root.findViewById<Spinner>(R.id.rootDirBox)
        val serverIp = root.findViewById<EditText>(R.id.serverIpField)
        val login = root.findViewById<EditText>(R.id.loginField)
        val password = root.findViewById<EditText>(R.id.passwordField)
        val connecting = root.findViewById<Button>(R.id.connectButt)

        // Creating and installing an adapter for selecting a language
        val languages = arrayOf("En", "Ua")
        val languageAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, languages)
        languageBox.adapter = languageAdapter

        // Устанавливаем обработчик выбора элемента
//        languageBox.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
//            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
//                val selectedItem = languages[position]
//                ImportantData.appLocale = selectedItem
//
//                // Сохраните выбранный язык и примените его к приложению
//                val locale = Locale(ImportantData.appLocale)
//                Locale.setDefault(locale)
//
//                val resources = context?.resources
//                val configuration = Configuration(resources?.configuration)
//                configuration.setLocale(locale)
//
//                context?.createConfigurationContext(configuration)
//
//                requireActivity().recreate()
//            }
//
//            override fun onNothingSelected(parent: AdapterView<*>?) {
//                // Вызывается, если ничего не выбрано
//                val myToast = Toast.makeText(
//                    activity,
//                    "Nothing selected",
//                    Toast.LENGTH_LONG
//                )
//                myToast.show()
//            }
//        }

        themeSwitch.setOnCheckedChangeListener { _, isChecked ->
            // Changing the App Theme
            if (isChecked) {
                // Dark theme selected
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
            } else {
                // Light theme selected
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
            }
        }

        // Creating a list of available roots
        val storageDirectories = ContextCompat.getExternalFilesDirs(requireContext(), null)
        val rootDirs = mutableListOf<String>()
        for (dir in storageDirectories) {
            rootDirs.add(dir.absolutePath.substring(0, dir.absolutePath.indexOf("/Android/data")))
        }

        // Creating and installing an adapter for selecting a root
        val storageAdapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, rootDirs)
        rootDir.adapter = storageAdapter
//        rootDir.isVisible = ImportantData.rootOfHomeDirectoryIsVisible

        // Installing a root selection handler
        rootDir.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                // Save selected item
                val selectedItem = rootDirs[position]
                ImportantData.clientRoot = selectedItem
            }
            override fun onNothingSelected(parent: AdapterView<*>?) {
                // Nothing selected
                val myToast = Toast.makeText(
                    activity,
                    "Nothing selected",
                    Toast.LENGTH_LONG
                )
                myToast.show()
            }
        }

        // Setting the correct text for the connection button depending on the connection state
        if (!connectionModel.isConnected().value!!) {
            connecting.text = getString(R.string.connect)
        }
        else {
            connecting.text = getString(R.string.disconnect)
        }

        connecting.setOnClickListener {
            // Connecting/disconnecting a connection
            Thread {
                // If there is no connection - connecting it, else - disconnecting it
                if (!connectionModel.isConnected().value!!) {
                    try {
                        ImportantData.server = ClientLogic(login.text.toString(), password.text.toString(), serverIp.text.toString())
//                        ImportantData.server = ClientLogic()
                        serv = ImportantData.server!!
                        serv.connect()
                        activity?.runOnUiThread {
                            connecting.text = getString(R.string.disconnect)
                            connectionModel.setConnected(true)
                            ImportantData.clientPath = "/"
                            ImportantData.serverRoot = "/"
                            ImportantData.serverPath = ""
                            ImportantData.rootOfHomeDirectoryIsVisible = false
                            rootDir.isVisible = false
                        }
                    } catch (e: Exception) {
                        activity?.runOnUiThread {
                            val myToast = Toast.makeText(
                                activity,
                                e.message.toString(),
                                Toast.LENGTH_LONG
                            )
                            myToast.show()
                        }
                    }
                }
                else {
                    serv.disconnect()
                    activity?.runOnUiThread {
                        connecting.text = getString(R.string.connect)
                        connectionModel.setConnected(false)
                        connectionModel.setClientUpdateIsNeeded(true)
                        connectionModel.setServerUpdateIsNeeded(true)
                        ImportantData.clientPath = ""
                        ImportantData.serverPath = ""
                        ImportantData.rootOfHomeDirectoryIsVisible = true
                        rootDir.isVisible = true
                    }
                }
            }.start()
        }

        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}