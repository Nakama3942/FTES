package com.fac.ftpandclient

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class ConnectionModel : ViewModel() {
    private val isConnectedLiveData = MutableLiveData<Boolean>()
    private val clientUpdateIsNeededLiveData = MutableLiveData<Boolean>()
    private val serverUpdateIsNeededLiveData = MutableLiveData<Boolean>()

    init {
        // Установите изначальное значение, например, true или false
        isConnectedLiveData.value = false
        clientUpdateIsNeededLiveData.value = false
        serverUpdateIsNeededLiveData.value = false
    }

    fun setConnected(isConnected: Boolean) {
        isConnectedLiveData.value = isConnected
    }

    fun isConnected(): LiveData<Boolean> {
        return isConnectedLiveData
    }

    fun setClientUpdateIsNeeded(clientUpdateIsNeeded: Boolean) {
        clientUpdateIsNeededLiveData.value = clientUpdateIsNeeded
    }

    fun clientUpdateIsNeeded(): LiveData<Boolean> {
        return clientUpdateIsNeededLiveData
    }

    fun setServerUpdateIsNeeded(serverUpdateIsNeeded: Boolean) {
        serverUpdateIsNeededLiveData.value = serverUpdateIsNeeded
    }

    fun serverUpdateIsNeeded(): LiveData<Boolean> {
        return serverUpdateIsNeededLiveData
    }
}