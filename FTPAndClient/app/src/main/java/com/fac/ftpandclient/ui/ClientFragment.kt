package com.fac.ftpandclient.ui

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.fac.ftpandclient.databinding.FragmentClientBinding
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.ConnectionModel
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ImportantData

class ClientFragment : Fragment() {

    private var _binding: FragmentClientBinding? = null

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
        _binding = FragmentClientBinding.inflate(inflater, container, false)
        val root: View = binding.root

        // Получите экземпляр ClientLogic, который вы создали ранее
        serv = ImportantData.server!!

        connectionModel = ViewModelProvider(requireActivity()).get(ConnectionModel::class.java)
        connectionModel.clientUpdateIsNeeded().observe(viewLifecycleOwner) { newData ->
            // Обработка изменений в данных
            if (newData) {
                binding.clientPathField.setText("/")
                connectionModel.setClientUpdateIsNeeded(false)
            }
        }

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Получите ссылку на RecyclerView из вашего layout'а
        val fileListRecyclerView = binding.clientFileList
        val filePath = binding.clientPathField
        filePath.setText(ImportantData.clientPath)

        // Загрузите файловую систему сервера из ClientLogic и установите ее в адаптер
        var clientFiles: List<String>? = null
        val mainServingThread = Thread {
            clientFiles = serv.openClientDirectory(ImportantData.clientRoot + filePath.text.toString()) // Этот метод нужно реализовать в вашем ClientLogic
        }
        mainServingThread.start()
        mainServingThread.join()

        var fileItems = clientFiles!!.map { FileItem("", it, "", false) }

        val layoutManager = LinearLayoutManager(context)

        // Создайте адаптер для RecyclerView, который будет отображать файлы
        val adapter = FileListAdapter(fileItems)

        // Установите адаптер для RecyclerView
        fileListRecyclerView.adapter = adapter
        fileListRecyclerView.layoutManager = layoutManager

        adapter.setOnItemClickListener(object : FileListAdapter.OnItemClickListener {
            override fun onItemClick(position: Int) {
                // Ваш код обработки клика
                if (fileItems[position].name == "..") {
                    val splitedPath = filePath.text.toString().split("/").toMutableList()
                    splitedPath.removeAt(splitedPath.size - 2)
                    ImportantData.clientPath = splitedPath.joinToString("/")
                    filePath.setText(ImportantData.clientPath)
                    val additionalServingThread = Thread {
                        clientFiles = serv.openParentClientDirectory(ImportantData.clientRoot + filePath.text.toString())
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }
                else {
                    ImportantData.clientPath = filePath.text.toString() + fileItems[position].name
                    filePath.setText(ImportantData.clientPath)
                    val additionalServingThread = Thread {
                        clientFiles = serv.openClientDirectory(ImportantData.clientRoot + filePath.text.toString())
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }

                fileItems = clientFiles!!.map { FileItem("", it, "", false) }
                adapter.updateFileList(fileItems)
                adapter.notifyDataSetChanged()
            }
        })
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}