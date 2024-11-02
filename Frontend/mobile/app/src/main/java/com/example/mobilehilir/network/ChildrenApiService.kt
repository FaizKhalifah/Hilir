import com.example.mobilehilir.data.AnakList
import retrofit2.http.GET
import retrofit2.Call

interface ChildrenApiService {
    @GET("api/parents/get_all_children/")
    fun getAllChildren(): Call<List<AnakList>>
}
