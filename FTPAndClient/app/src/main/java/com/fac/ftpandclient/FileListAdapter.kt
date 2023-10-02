package com.fac.ftpandclient

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView

class FileListAdapter(private var fileList: List<FileItem>) : RecyclerView.Adapter<FileListAdapter.FileViewHolder>() {

    private var listener: OnItemClickListener? = null

    interface OnItemClickListener {
        fun onItemClick(position: Int)
    }

    class FileViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val fileImage: ImageView = itemView.findViewById(R.id.fileImage)
        val fileName: TextView = itemView.findViewById(R.id.fileName)
        val fileInfo: TextView = itemView.findViewById(R.id.fileInfo)
//        val fileDir: TextView = itemView.findViewById(R.id.fileName)
    }

    fun updateFileList(newFileList: List<FileItem>) {
        fileList = newFileList
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): FileViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.fragment_file, parent, false)
        return FileViewHolder(view)
    }

    override fun onBindViewHolder(holder: FileViewHolder, position: Int) {
        val fileItem = fileList[position]

//        holder.fileImage.text = ""
        holder.fileName.text = fileItem.name
        holder.fileInfo.text = position.toString()

        holder.itemView.setOnClickListener {
            listener?.onItemClick(position)
        }

        // Установите другие свойства элементов интерфейса в зависимости от данных fileItem
    }

    override fun getItemCount(): Int = fileList.size

    fun setOnItemClickListener(listener: OnItemClickListener) {
        this.listener = listener
    }
}
