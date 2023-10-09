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

package com.fac.ftpandclient

import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class FileListAdapter(
    private var fileList: List<FileItem>
) : RecyclerView.Adapter<FileListAdapter.FileViewHolder>() {

    // Listener interface
    interface OnItemClickListener {
        fun onItemClick(position: Int)
    }

    // Listener variable
    private var listener: OnItemClickListener? = null

    class FileViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val fileImage: ImageView = itemView.findViewById(R.id.fileImage)
        val fileName: TextView = itemView.findViewById(R.id.fileName)
        val fileInfo: TextView = itemView.findViewById(R.id.fileInfo)
    }

    fun updateFileList(newFileList: List<FileItem>) {
        fileList = newFileList
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FileViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.fragment_file, parent, false)
        return FileViewHolder(view)
    }

    override fun onBindViewHolder(holder: FileViewHolder, position: Int) {
        val fileItem = fileList[position]

        holder.fileImage.setImageURI(fileItem.image)
        holder.fileName.text = fileItem.name
        holder.fileInfo.text = fileItem.info

        // Handling a short click on a list item
        holder.itemView.setOnClickListener {
            // If the selected element is a file - select it, else - react to the click
            if (!fileItem.isDirectory) {
                toggleSelection(position)
            }
            else {
                listener?.onItemClick(position)
            }
        }

        // Handling a long press on a list item
        holder.itemView.setOnLongClickListener {
            // If the selected element is a directory - select it
            if (fileItem.isDirectory) {
                toggleSelection(position)
                return@setOnLongClickListener true // Return true to indicate the event has been processed
            }
            false
        }

        // Determine the background color of an element depending on whether the element is selected
        val backgroundResId = if (fileItem.isSelected) {
            R.color.green_500_trans // Resource for the selected element
        } else {
            Color.TRANSPARENT // Resource for an unselected element
        }
        holder.itemView.setBackgroundResource(backgroundResId)
    }

    override fun getItemCount(): Int = fileList.size

    fun setOnItemClickListener(listener: OnItemClickListener) {
        this.listener = listener
    }

    private fun toggleSelection(position: Int) {
        // Selecting an element
        val fileItem = fileList[position]
        fileItem.isSelected = !fileItem.isSelected
        notifyItemChanged(position)
    }

    fun getSelectedFiles(): List<FileItem> {
        // Method for getting a list of selected elements
        return fileList.filter { it.isSelected }
    }
}
