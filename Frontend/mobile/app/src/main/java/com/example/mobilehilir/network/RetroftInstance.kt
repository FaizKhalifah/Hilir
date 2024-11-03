//package com.example.mobilehilir.network
//
//import retrofit2.Retrofit
//import retrofit2.converter.gson.GsonConverterFactory
//
//object RetrofitInstance {
//    private const val BASE_URL = "http://127.0.0.1:5000/" // Ganti dengan URL yang sesuai
//
//    private val retrofit: Retrofit by lazy {
//        Retrofit.Builder()
//            .baseUrl(BASE_URL)
//            .addConverterFactory(GsonConverterFactory.create())
//            .build()
//    }
//
//    val api: ChildrenApiService by lazy {
//        retrofit.create(ChildrenApiService::class.java)
//    }
//}
