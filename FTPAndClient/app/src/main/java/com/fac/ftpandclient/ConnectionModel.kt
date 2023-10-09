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

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class ConnectionModel : ViewModel() {
    private val isConnectedLiveData = MutableLiveData<Boolean>()
    private val clientUpdateIsNeededLiveData = MutableLiveData<Boolean>()
    private val serverUpdateIsNeededLiveData = MutableLiveData<Boolean>()

    init {
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