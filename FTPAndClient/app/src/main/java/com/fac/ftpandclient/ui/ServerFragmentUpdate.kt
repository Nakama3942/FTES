package com.fac.ftpandclient.ui

import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.documentfile.provider.DocumentFile
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.ConnectionModel
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ImportantData
import com.fac.ftpandclient.R
import com.fac.ftpandclient.databinding.FragmentServerUpdateBinding

class ServerFragmentUpdate : Fragment() {

    private var _binding: FragmentServerUpdateBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var selectedDirectoryUri: Uri
    private lateinit var selectedServerFileNames: List<String>

    private lateinit var serv: ClientLogic
    private lateinit var connectionModel: ConnectionModel

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentServerUpdateBinding.inflate(inflater, container, false)
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

        // Элементы интерфейса
        val copyChip = binding.copyChip
        val newDirButt = binding.newDirButt
        val removeButt = binding.removeButt
        val uploadButt = binding.uploadButt
        val downloadButt = binding.downloadButt

        //Работа с файловой системой
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

        var fileItems = serverFiles!!.map { fileName ->
            val imageUri: Uri
            var info: String = ""
            val isDir: Boolean
            if (fileName == "..") {
                imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.undo)
                info = "Return"
                isDir = true
            }
            else {
                isDir = fileName.contains("/")
                if (isDir) {
                    imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.folder)
                }
                else {
                    imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.file)
                }
                val additionalServingThread = Thread {
                    info = serv.getServerFileSize(ImportantData.serverRoot + ImportantData.serverPath + fileName).toString()
                }
                additionalServingThread.start()
                additionalServingThread.join()
            }
            FileItem(imageUri,  fileName, info, isDir, false)
        }

        val layoutManager = LinearLayoutManager(context)

        // Создайте адаптер для RecyclerView, который будет отображать файлы
        val adapter = FileListAdapter(fileItems)

        // Установите адаптер для RecyclerView
        fileListRecyclerView.adapter = adapter
        fileListRecyclerView.layoutManager = layoutManager

        adapter.setOnItemClickListener(object : FileListAdapter.OnItemClickListener {
            override fun onItemClick(position: Int) {
                // Ваш код обработки клика
                if (!fileItems[position].isDirectory) {
                    return
                }

                if (fileItems[position].name == "..") {
                    if (filePath.text.toString() == "/") {
                        val myToast = Toast.makeText(
                            activity,
                            "Already open the root",
                            Toast.LENGTH_LONG
                        )
                        myToast.show()
                        return
                    }
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

                fileItems = serverFiles!!.map { fileName ->
                    val imageUri: Uri
                    var info: String = ""
                    val isDir: Boolean
                    if (fileName == "..") {
                        imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.undo)
                        info = "Return"
                        isDir = true
                    }
                    else {
                        isDir = fileName.contains("/")
                        if (isDir) {
                            imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.folder)
                        }
                        else {
                            imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.file)
                        }
                        val additionalServingThread = Thread {
                            info = serv.getServerFileSize(ImportantData.serverRoot + ImportantData.serverPath + fileName).toString()
                        }
                        additionalServingThread.start()
                        additionalServingThread.join()
                    }
                    FileItem(imageUri,  fileName, info, isDir, false)
                }
                adapter.updateFileList(fileItems)
            }
        })

        copyChip.setOnClickListener {  }

        newDirButt.setOnClickListener {  }

        removeButt.setOnClickListener {  }

        uploadButt.setOnClickListener {
            uploadContent.launch("*/*")
        }

        downloadButt.setOnClickListener {
            val selectedFiles = adapter.getSelectedFiles()
            selectedServerFileNames = selectedFiles.map { it.name }

            downloadContent.launch(null)
        }
    }

    private fun download(serverFile: String) {
        println(selectedDirectoryUri.toString())
        val userDirectory = DocumentFile.fromTreeUri(requireContext(), selectedDirectoryUri)

        var isServerFile = true
        val downloadThread1 = Thread {
            isServerFile = serv.isServerFile(serverFile)
        }
        downloadThread1.start()
        downloadThread1.join()

        if (isServerFile) {
            // Сохранение содержимого на телефоне
            val file = userDirectory?.createFile("", serverFile)
            file?.uri?.let { fileUri ->
                context?.contentResolver?.openOutputStream(fileUri)?.use { outputStream ->
                    val downloadThread2 = Thread {
                        serv.downloadAndroid(serverFile, outputStream)
                    }
                    downloadThread2.start()
                    downloadThread2.join()
                    outputStream.close()
                }
            }
        }
        else {
            userDirectory?.createDirectory(serverFile)
            var nestedFiles: List<String>? = null
            val downloadThread3 = Thread {
                nestedFiles = serv.openServerDirectory(serv.currentDir() + serverFile)
            }
            downloadThread3.start()
            downloadThread3.join()
            for (nestedFile in nestedFiles!!) {
                download(serverFile)
            }
            val downloadThread4 = Thread {
                serv.openParentServerDirectory()
            }
            downloadThread4.start()
            downloadThread4.join()
        }
    }

    private val uploadContent = registerForActivityResult(ActivityResultContracts.GetMultipleContents()) { uris ->
        if (uris != null) {
            // Обработайте полученные URI файлов здесь
            for (uri in uris) {
                val fileName = uri.pathSegments.last().split(":").last().split("/").last() // Здесь вы должны получить имя файла из URI
                val contentStream = context?.contentResolver?.openInputStream(uri) // Получите поток содержимого файла из URI
                if (fileName != null && contentStream != null) {
                    val additionalServingThread = Thread {
                        serv.uploadAndroid(fileName, contentStream)
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }
            }
        }
    }

    private val downloadContent = registerForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri ->
        if (uri != null) {
            selectedDirectoryUri = uri
            for (serverFile in selectedServerFileNames) {
                if (serverFile == "..") {
                    continue
                }

                download(serverFile)

//                if (clear) {
//                    removeServerPath(ftpClient.printWorkingDirectory() + "/" + serverFile)
//                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}