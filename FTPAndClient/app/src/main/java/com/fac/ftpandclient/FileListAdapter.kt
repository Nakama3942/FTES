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

    private var listener: OnItemClickListener? = null

    interface OnItemClickListener {
        fun onItemClick(position: Int)
    }

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

        holder.itemView.setOnClickListener {
            if (!fileItem.isDirectory) {
                toggleSelection(position)
            }
            else {
                listener?.onItemClick(position)
            }
        }

        holder.itemView.setOnLongClickListener {
            // Обработка долгого нажатия на элементе списка
            if (fileItem.isDirectory) {
                toggleSelection(position)
                return@setOnLongClickListener true // Верните true, чтобы указать, что событие обработано
            }
            false
        }

        // Определение цвета фона элемента в зависимости от выбора
        val backgroundResId = if (fileItem.isSelected) {
            R.color.green_500_trans // Ресурс для выделенного элемента
        } else {
            Color.TRANSPARENT // Ресурс для не выделенного элемента
        }
        holder.itemView.setBackgroundResource(backgroundResId)
    }

    override fun getItemCount(): Int = fileList.size

    fun setOnItemClickListener(listener: OnItemClickListener) {
        this.listener = listener
    }

    private fun toggleSelection(position: Int) {
        val fileItem = fileList[position]
        fileItem.isSelected = !fileItem.isSelected
        notifyItemChanged(position)
    }
}
