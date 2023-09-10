package com.fac.ftpandclient.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.R
import com.fac.ftpandclient.databinding.FragmentLoginBinding

class LoginFragment : Fragment() {

    private var _binding: FragmentLoginBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var serv: ClientLogic

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
//        val dashboardViewModel = ViewModelProvider(this).get(LoginViewModel::class.java)

        _binding = FragmentLoginBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val connecting = root.findViewById<Button>(R.id.connectButt)
        val login = root.findViewById<EditText>(R.id.loginField)
        val password = root.findViewById<EditText>(R.id.passwordField)

        connecting.setOnClickListener {
            Thread {
                if (connecting.text == getString(R.string.connect)) {
                    try {
                        serv = ClientLogic(login.text.toString(), password.text.toString())
                        serv.connect()
                        activity?.runOnUiThread {
                            connecting.text = getString(R.string.disconnect)
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