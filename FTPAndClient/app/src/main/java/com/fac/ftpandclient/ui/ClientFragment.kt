package com.fac.ftpandclient.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import com.fac.ftpandclient.databinding.FragmentClientBinding
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ImportantData

class ClientFragment : Fragment() {

    private var _binding: FragmentClientBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var serv: ClientLogic
    private lateinit var home: String

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentClientBinding.inflate(inflater, container, false)
        val root: View = binding.root
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Получите экземпляр ClientLogic, который вы создали ранее
        serv = ImportantData.server!!
        home = ImportantData.clientRoot!!

        // Получите ссылку на RecyclerView из вашего layout'а
        val fileListRecyclerView = binding.clientFileList
        val filePath = binding.clientPathField
        filePath.setText("/")

        // Загрузите файловую систему сервера из ClientLogic и установите ее в адаптер
        Thread {
            var clientFiles = serv.openClientDirectory(home + filePath.text.toString()) // Этот метод нужно реализовать в вашем ClientLogic
            var fileItems = clientFiles!!.map { FileItem("", it, "", false) }

            val layoutManager = LinearLayoutManager(context)

            // Создайте адаптер для RecyclerView, который будет отображать файлы
            var adapter = FileListAdapter(fileItems)

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
                        val newPath: String = filePath.text.toString() + fileItems[position].name
                        filePath.setText(newPath)
                        Thread {
                            clientFiles = serv.openClientDirectory(home + filePath.text.toString())
                            fileItems = clientFiles!!.map { FileItem("", it, "", false) }
                            adapter = FileListAdapter(fileItems)
                            activity?.runOnUiThread {
                                // Уведомите адаптер о изменениях
                                fileListRecyclerView.adapter = adapter
                            }
                        }.start()
                    }
                })
            }
        }.start() // TODO достать весь код из потока
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}