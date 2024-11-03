//package com.example.mobilehilir
//
//import androidx.lifecycle.LiveData
//import androidx.lifecycle.MutableLiveData
//import androidx.lifecycle.ViewModel
//import com.example.mobilehilir.data.AnakList
//import retrofit2.Call
//import retrofit2.Callback
//import retrofit2.Response
//
//class ChildrenViewModel : ViewModel() {
//
//    private val _childrenList = MutableLiveData<List<AnakList>>()
//    val childrenList: LiveData<List<AnakList>> = _childrenList
//
//    private val _errorMessage = MutableLiveData<String?>()
//    val errorMessage: LiveData<String?> = _errorMessage
//
//    fun getAllChildren() {
//        RetrofitInstance.api.getAllChildren().enqueue(object : Callback<List<AnakList>> {
//            override fun onResponse(call: Call<List<AnakList>>, response: Response<List<AnakList>>) {
//                if (response.isSuccessful) {
//                    _childrenList.value = response.body()
//                    _errorMessage.value = null
//                } else {
//                    _errorMessage.value = "Error: ${response.code()}"
//                }
//            }
//
//            override fun onFailure(call: Call<List<AnakList>>, t: Throwable) {
//                _errorMessage.value = "An unexpected error occurred: ${t.message}"
//            }
//        })
//    }
//}
