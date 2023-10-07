package com.fac.ftpandclient

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.widget.EditText
import androidx.fragment.app.DialogFragment

class DirectoryNameDialogFragment : DialogFragment() {
    // Определите интерфейс OnDirectoryNameEnteredListener
    interface OnDirectoryNameEnteredListener {
        fun onDirectoryNameEntered(directoryName: String)
    }

    // Добавьте переменную для слушателя
    private var listener: OnDirectoryNameEnteredListener? = null

    // Создайте метод для установки слушателя
    fun setOnDirectoryNameEnteredListener(listener: OnDirectoryNameEnteredListener) {
        this.listener = listener
    }

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        val builder = AlertDialog.Builder(requireContext())
        val inputField = EditText(requireContext())

        builder.setTitle(getString(R.string.directory_name_dialog_title))
            .setView(inputField)
            .setPositiveButton(getString(R.string.directory_name_dialog_positive_button)) { dialog, _ ->
                val directoryName = inputField.text.toString()
                // Вызываем метод слушателя и передаем введенное имя
                listener?.onDirectoryNameEntered(directoryName)
                dialog.dismiss()
            }
            .setNegativeButton(getString(R.string.directory_name_dialog_negative_button)) { dialog, _ ->
                dialog.cancel()
            }

        return builder.create()
    }
}