package com.fac.ftpandclient

import android.net.Uri

data class FileItem(
    val image: Uri,
    val name: String,
    val info: String,
    val isDirectory: Boolean
)
