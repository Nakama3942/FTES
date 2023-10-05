package com.fac.ftpandclient.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatDelegate
import androidx.appcompat.widget.SwitchCompat
import androidx.core.content.ContextCompat
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
//        val dashboardViewModel = ViewModelProvider(this).get(LoginViewModel::class.java)

        _binding = FragmentLoginBinding.inflate(inflater, container, false)
        val root: View = binding.root

        // Получите доступ к ConnectionViewModel
        connectionModel = ViewModelProvider(requireActivity()).get(ConnectionModel::class.java)

        val themeSwitch = root.findViewById<SwitchCompat>(R.id.themeSwitch)
//        val rootDir = root.findViewById<Spinner>(R.id.rootDirBox)
//        val rootDir = root.findViewById<TextView>(R.id.rootDirTextView)
//        val rootDir = root.findViewById<ToggleButton>(R.id.rootDirToggleButton)
        val rootDirStr = root.findViewById<TextView>(R.id.rootDirTextView)
        val serverIp = root.findViewById<EditText>(R.id.serverIpField)
        val login = root.findViewById<EditText>(R.id.loginField)
        val password = root.findViewById<EditText>(R.id.passwordField)
        val connecting = root.findViewById<Button>(R.id.connectButt)

        themeSwitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                // Выбрана тёмная тема
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
            } else {
                // Выбрана светлая тема
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
            }
        }

        var sdCard = ContextCompat.getExternalFilesDirs(requireContext(), null)[1].absolutePath
        sdCard = sdCard.substring(0, sdCard.indexOf("/Android/data"))
        rootDirStr.text = "CD card root directory is: " + sdCard
        ImportantData.clientRoot = sdCard
//        val storageDirectories = ContextCompat.getExternalFilesDirs(requireContext(), null)
//        val rootDirs = mutableListOf<String>()
//        for (dir in storageDirectories) {
//            rootDirs.add(dir.absolutePath.substring(0, dir.absolutePath.indexOf("/Android/data")))
//        }
//
//        // Создание адаптера для Spinner
//        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, rootDirs)
//
//        // Устанавливаем адаптер для Spinner
//        rootDir.adapter = adapter
//        rootDir.isVisible = ImportantData.rootOfHomeDirectoryIsVisible
//
//        // Устанавливаем обработчик выбора элемента
//        rootDir.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
//            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
//                val selectedItem = rootDirs[position]
//                ImportantData.clientRoot = selectedItem
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

        if (!connectionModel.isConnected().value!!) {
            connecting.text = getString(R.string.connect)
        }
        else {
            connecting.text = getString(R.string.disconnect)
        }

        connecting.setOnClickListener {
            Thread {
                if (!connectionModel.isConnected().value!!) {
                    try {
//                        ImportantData.server = ClientLogic(login.text.toString(), password.text.toString(), serverIp.text.toString())
                        ImportantData.server = ClientLogic()
                        serv = ImportantData.server!!
                        serv.connect()
                        activity?.runOnUiThread {
                            connecting.text = getString(R.string.disconnect)
                            connectionModel.setConnected(true)
                            ImportantData.clientPath = "/"
                            ImportantData.serverRoot = "/"
                            ImportantData.serverPath = ""
                            ImportantData.rootOfHomeDirectoryIsVisible = false
//                            rootDir.isVisible = false
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
//                        rootDir.isVisible = true
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