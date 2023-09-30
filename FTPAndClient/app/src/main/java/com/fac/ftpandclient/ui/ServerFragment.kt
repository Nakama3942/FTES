package com.fac.ftpandclient.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ServerLink
import com.fac.ftpandclient.databinding.FragmentServerBinding

class ServerFragment : Fragment() {

    private var _binding: FragmentServerBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var serv: ClientLogic

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentServerBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Получите экземпляр ClientLogic, который вы создали ранее
        serv = ServerLink.server!!

        // Получите ссылку на RecyclerView из вашего layout'а
        val fileListRecyclerView = binding.serverFileList

        // Загрузите файловую систему сервера из ClientLogic и установите ее в адаптер
        Thread {
            val serverFiles = serv.openServerDirectory("/") // Этот метод нужно реализовать в вашем ClientLogic
            val fileItems = serverFiles!!.map { FileItem("", it, "", false) }

            val layoutManager = LinearLayoutManager(context)

            // Создайте адаптер для RecyclerView, который будет отображать файлы
            val adapter = FileListAdapter(fileItems)

            // Установите адаптер для RecyclerView
            activity?.runOnUiThread {
                fileListRecyclerView.adapter = adapter
                fileListRecyclerView.layoutManager = layoutManager

                adapter.setOnItemClickListener(object : FileListAdapter.OnItemClickListener {
                    override fun onItemClick(position: Int) {
                        // Обработка клика на элементе в списке
//                        val clickedItem = fileItems[position]
                        val myToast = Toast.makeText(
                            activity,
                            fileItems[position].name,
                            Toast.LENGTH_LONG
                        )
                        myToast.show()
                        // Ваш код обработки клика
                    }
                })
            }
        }.start()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}