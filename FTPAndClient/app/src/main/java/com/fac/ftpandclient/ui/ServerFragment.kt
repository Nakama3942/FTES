package com.fac.ftpandclient.ui

import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.fac.ftpandclient.ClientLogic
import com.fac.ftpandclient.ConnectionModel
import com.fac.ftpandclient.DirectoryNameDialogFragment
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ImportantData
import com.fac.ftpandclient.R
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

        // Getting a ClientLogic instance
        serv = ImportantData.server!!

        // Accessing the ConnectionViewModel
        connectionModel = ViewModelProvider(requireActivity())[ConnectionModel::class.java]
        connectionModel.serverUpdateIsNeeded().observe(viewLifecycleOwner) { newData ->
            // Resetting the path to the root after disconnecting from the server
            if (newData) {
                binding.servetPathField.text = ImportantData.serverRoot
                connectionModel.setServerUpdateIsNeeded(false)
            }
        }

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Links to interface buttons
        val syncButt = binding.serverSyncButt
        val newDirButt = binding.newDirButt
        val removeButt = binding.removeButt
        val downloadButt = binding.downloadButt

        // Links to file manager elements
        val serverFileList = binding.serverFileList
        val filePath = binding.servetPathField
        filePath.text = getString(R.string.path_field, ImportantData.serverRoot, ImportantData.serverPath)

        // Loading the Server File System
        var serverFiles: List<String>? = null
        val mainServingThread = Thread {
            serverFiles = serv.openServerDirectory(filePath.text.toString())
        }
        mainServingThread.start()
        mainServingThread.join()

        // Converting a list of file names to a list of file objects
        var fileItems = serverFiles!!.map { fileName ->
            val imageUri: Uri
            var info = ""
            val isDir: Boolean
            if (fileName == "..") {
                imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.undo)
                info = "Return"
                isDir = true
            }
            else {
                isDir = fileName.contains("/")
                imageUri = if (isDir) {
                    Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.folder)
                } else {
                    Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.file)
                }
                val additionalServingThread = Thread {
                    info = serv.getServerFileSize(ImportantData.serverRoot + ImportantData.serverPath + fileName).toString()
                }
                additionalServingThread.start()
                additionalServingThread.join()
            }
            FileItem(imageUri,  fileName, info, isDir, false)
        }

        // Creating and installing an adapter and manager in the File Manager
        val adapter = FileListAdapter(fileItems)
        val layoutManager = LinearLayoutManager(context)
        serverFileList.adapter = adapter
        serverFileList.layoutManager = layoutManager

        // Processing a click on a list item in the File Manager
        adapter.setOnItemClickListener(object : FileListAdapter.OnItemClickListener {
            override fun onItemClick(position: Int) {
                // If the selected item is NOT a directory - do nothing
                if (!fileItems[position].isDirectory) {
                    return
                }

                // If a return element is selected - need to return to the
                // parent directory, else - open the selected child directory
                if (fileItems[position].name == "..") {
                    // But if the current directory is already the root - just display a warning
                    if (filePath.text.toString() == "/") {
                        val myToast = Toast.makeText(
                            activity,
                            "Already open the root",
                            Toast.LENGTH_LONG
                        )
                        myToast.show()
                        return
                    }
                    // Defining and return to the parent directory
                    val splittedPath = ImportantData.serverPath.split("/").toMutableList()
                    splittedPath.removeAt(splittedPath.size - 2)
                    ImportantData.serverPath = splittedPath.joinToString("/")
                    filePath.text = getString(R.string.path_field, ImportantData.serverRoot, ImportantData.serverPath)
                    val additionalServingThread = Thread {
                        serverFiles = serv.openParentServerDirectory()
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }
                else {
                    // Defining the contents of a child directory
                    ImportantData.serverPath = ImportantData.serverPath + fileItems[position].name
                    filePath.text = getString(R.string.path_field, ImportantData.serverRoot, ImportantData.serverPath)
                    val additionalServingThread = Thread {
                        serverFiles = serv.openServerDirectory(filePath.text.toString())
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }

                // Converting a list of file names to a list of file objects
                fileItems = serverFiles!!.map { fileName ->
                    val imageUri: Uri
                    var info = ""
                    val isDir: Boolean
                    if (fileName == "..") {
                        imageUri = Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.undo)
                        info = "Return"
                        isDir = true
                    }
                    else {
                        isDir = fileName.contains("/")
                        imageUri = if (isDir) {
                            Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.folder)
                        } else {
                            Uri.parse("android.resource://" + requireContext().packageName + "/" + R.drawable.file)
                        }
                        val additionalServingThread = Thread {
                            info = serv.getServerFileSize(ImportantData.serverRoot + ImportantData.serverPath + fileName).toString()
                        }
                        additionalServingThread.start()
                        additionalServingThread.join()
                    }
                    FileItem(imageUri,  fileName, info, isDir, false)
                }

                // Updating File Manager
                adapter.updateFileList(fileItems)
            }
        })

        syncButt.setOnClickListener {
            // Updating Fragment
            onViewCreated(view, savedInstanceState)
        }

        newDirButt.setOnClickListener {
            // Requesting the name of the new directory and create it
            val directoryInputFragment = DirectoryNameDialogFragment()
            directoryInputFragment.setOnDirectoryNameEnteredListener(object : DirectoryNameDialogFragment.OnDirectoryNameEnteredListener {
                // Listener to process the result after input
                override fun onDirectoryNameEntered(directoryName: String) {
                    val creatingThread = Thread {
                        serv.createServerDirectory(directoryName)
                    }
                    creatingThread.start()
                    creatingThread.join()
                }
            })
            directoryInputFragment.show(requireActivity().supportFragmentManager, "DirectoryNameDialog")
        }

        removeButt.setOnClickListener {
            // Removing selected items
            val selectedFiles = adapter.getSelectedFiles()
            val fileNames: List<String> = selectedFiles.map { it.name }
            val filePaths = mutableListOf<String>()

            for (fileName in fileNames) {
                filePaths.add(ImportantData.serverRoot + ImportantData.serverPath + fileName)
            }

            val creatingThread = Thread {
                serv.removeServerPath(filePaths)
            }
            creatingThread.start()
            creatingThread.join()
        }

        downloadButt.setOnClickListener {
            // Downloading selected elements from the server
            val selectedFiles = adapter.getSelectedFiles()
            val fileNames: List<String> = selectedFiles.map { it.name }

            val uploadThread = Thread {
                serv.downloadAll(ImportantData.clientRoot + ImportantData.clientPath, fileNames, !binding.copyChip.isChecked)
            }
            uploadThread.start()
            uploadThread.join()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}