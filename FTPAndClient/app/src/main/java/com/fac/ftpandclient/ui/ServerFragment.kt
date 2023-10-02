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
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.ConnectionModel
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ImportantData
import com.fac.ftpandclient.databinding.FragmentServerBinding

class ServerFragment : Fragment() {

    private var _binding: FragmentServerBinding? = null

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
        _binding = FragmentServerBinding.inflate(inflater, container, false)
        val root: View = binding.root

        // Получите экземпляр ClientLogic, который вы создали ранее
        serv = ImportantData.server!!

        connectionModel = ViewModelProvider(requireActivity()).get(ConnectionModel::class.java)
        connectionModel.serverUpdateIsNeeded().observe(viewLifecycleOwner) { newData ->
            // Обработка изменений в данных
            if (newData) {
                binding.servetPathField.setText(ImportantData.serverRoot)
                connectionModel.setServerUpdateIsNeeded(false)
            }
        }

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Получите ссылку на RecyclerView из вашего layout'а
        val fileListRecyclerView = binding.serverFileList
        val filePath = binding.servetPathField
        filePath.setText(ImportantData.serverRoot + ImportantData.serverPath)

        // Загрузите файловую систему сервера из ClientLogic и установите ее в адаптер
        var serverFiles: List<String>? = null
        val mainServingThread = Thread {
            serverFiles = serv.openServerDirectory(filePath.text.toString()) // Этот метод нужно реализовать в вашем ClientLogic
        }
        mainServingThread.start()
        mainServingThread.join()

        var fileItems = serverFiles!!.map { FileItem("", it, "", false) }

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
                    val splitedPath = ImportantData.serverPath.split("/").toMutableList()
                    splitedPath.removeAt(splitedPath.size - 2)
                    ImportantData.serverPath = splitedPath.joinToString("/")
                    filePath.setText(ImportantData.serverRoot + ImportantData.serverPath)
                    val additionalServingThread = Thread {
                        serverFiles = serv.openParentServerDirectory()
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }
                else {
                    ImportantData.serverPath = ImportantData.serverPath + fileItems[position].name
                    filePath.setText(ImportantData.serverRoot + ImportantData.serverPath)
                    val additionalServingThread = Thread {
                        serverFiles = serv.openServerDirectory(filePath.text.toString())
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }

                fileItems = serverFiles!!.map { FileItem("", it, "", false) }
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