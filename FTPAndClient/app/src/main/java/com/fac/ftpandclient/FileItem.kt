package com.fac.ftpandclient

import android.net.Uri

data class FileItem(
    val image: Uri,
    val name: String,
    val info: String,
    val absolutPath: String,
    val isDirectory: Boolean,
    var isSelected: Boolean
)
