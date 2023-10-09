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

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.widget.EditText
import androidx.fragment.app.DialogFragment

class DirectoryNameDialogFragment : DialogFragment() {

    // Listener interface
    interface OnDirectoryNameEnteredListener {
        fun onDirectoryNameEntered(directoryName: String)
    }

    // Listener variable
    private var listener: OnDirectoryNameEnteredListener? = null

    // Method for setting a listener
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
                listener?.onDirectoryNameEntered(directoryName)
                dialog.dismiss()
            }
            .setNegativeButton(getString(R.string.directory_name_dialog_negative_button)) { dialog, _ ->
                dialog.cancel()
            }

        return builder.create()
    }
}