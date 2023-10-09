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
import com.fac.ftpandclient.DirectoryNameDialogFragment
import com.fac.ftpandclient.FileItem
import com.fac.ftpandclient.FileListAdapter
import com.fac.ftpandclient.ImportantData
import com.fac.ftpandclient.R
import com.fac.ftpandclient.databinding.FragmentServerSafBinding

class ServerSafFragment : Fragment() {

    private var _binding: FragmentServerSafBinding? = null

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
        _binding = FragmentServerSafBinding.inflate(inflater, container, false)
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
        val syncButt = binding.serverSafSyncButt
        val newDirButt = binding.newDirButt
        val removeButt = binding.removeButt
        val uploadButt = binding.uploadButt
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

        uploadButt.setOnClickListener {
            // Uploading selected elements to the server
            // Run SAF activity
            uploadContent.launch("*/*")
        }

        downloadButt.setOnClickListener {
            // Downloading selected elements from the server
            val selectedFiles = adapter.getSelectedFiles()
            selectedServerFileNames = selectedFiles.map { it.name }

            // Run SAF activity
            downloadContent.launch(null)
        }
    }

    private val uploadContent = registerForActivityResult(ActivityResultContracts.GetMultipleContents()) { uris ->
        // SAF activity for uploading
        if (uris != null) {
            // Processing all user selected files in SAF
            for (uri in uris) {
                // Getting file name from URI and its contents
                val fileName = uri.pathSegments.last().split(":").last().split("/").last()
                val contentStream = context?.contentResolver?.openInputStream(uri)

                // If the contents of the file are received - upload it to the server
                if (contentStream != null) {
                    val additionalServingThread = Thread {
                        serv.uploadStream(fileName, contentStream)
                    }
                    additionalServingThread.start()
                    additionalServingThread.join()
                }
            }
        }
    }

    private val downloadContent = registerForActivityResult(ActivityResultContracts.OpenDocumentTree()) { uri ->
        // SAF activity for downloading
        if (uri != null) {
            selectedDirectoryUri = uri

            // Processing all user selected files in Server File Manager
            for (serverFile in selectedServerFileNames) {
                // Ignore the return element
                if (serverFile == "..") {
                    continue
                }

                // Calling the adapted recursive load function
                val downloadThread = Thread {
                    download(serverFile)
                }
                downloadThread.start()
                downloadThread.join()

                // Here files will never be deleted
            }
        }
    }

    private fun download(serverFile: String) {
        val userDirectory = DocumentFile.fromTreeUri(requireContext(), selectedDirectoryUri)

        // If the current element is a file - load it on the phone, else - create
        // a directory and repeat the operation recursively for its nested elements
        if (serv.isServerFile(serverFile)) {
            val file = userDirectory?.createFile("", serverFile)
            file?.uri?.let { fileUri ->
                context?.contentResolver?.openOutputStream(fileUri)?.use { outputStream ->
                    serv.downloadStream(serverFile, outputStream)
                    outputStream.close()
                }
            }
        }
        else {
            userDirectory?.createDirectory(serverFile)
            for (nestedFile in serv.openServerDirectory(serv.currentServerDir() + serverFile)!!) {
                download(serverFile)
            }
            serv.openParentServerDirectory()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}