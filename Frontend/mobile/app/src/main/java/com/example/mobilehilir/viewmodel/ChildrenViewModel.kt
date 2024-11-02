import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.mobilehilir.data.AnakList
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ChildrenViewModel : ViewModel() {

    // MutableLiveData to store the list of children
    private val _childrenList = MutableLiveData<List<AnakList>>()
    val childrenList: LiveData<List<AnakList>> = _childrenList

    // Method to fetch all children
    fun getAllChildren() {
        val call = RetrofitClient.instance.getAllChildren()
        call.enqueue(object : Callback<List<AnakList>> {
            override fun onResponse(call: Call<List<AnakList>>, response: Response<List<AnakList>>) {
                if (response.isSuccessful) {
                    _childrenList.value = response.body()  // Update LiveData with the fetched data
                } else {
                    // Handle error response, maybe log an error or show a message to the user
                }
            }

            override fun onFailure(call: Call<List<AnakList>>, t: Throwable) {
                // Handle the failure (e.g., log the error or show an error message to the user)
            }
        })
    }
}
