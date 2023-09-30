package com.fac.ftpandclient

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class ConnectionModel : ViewModel() {
    private val isConnectedLiveData = MutableLiveData<Boolean>()

    init {
        // Установите изначальное значение, например, true или false
        isConnectedLiveData.value = false
    }

    fun setConnected(isConnected: Boolean) {
        isConnectedLiveData.value = isConnected
    }

    fun isConnected(): LiveData<Boolean> {
        return isConnectedLiveData
    }
}