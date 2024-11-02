package com.example.mobilehilir.data

import java.text.SimpleDateFormat
import java.util.Date

data class Article(
    val news_id : Int,
    val judul : String,
    val short_description : String,
    val isi : String,
    val publish : Date,
    val author : String
)


fun getDummyArticles(): List<Article> {
    val dateFormat = SimpleDateFormat("yyyy-MM-dd")
    return listOf(
        Article(
            news_id = 1,
            judul = "The Benefits of Mindfulness",
            short_description = "An overview of how mindfulness can improve mental health.",
            isi = """
                Mindfulness is the practice of being present and fully engaged in the moment without judgment. 
                Studies have shown that mindfulness can reduce stress, improve emotional regulation, and enhance 
                overall well-being. By practicing mindfulness, individuals can learn to recognize and manage 
                their thoughts and feelings, leading to better mental health outcomes.
            """.trimIndent(),
            publish = dateFormat.parse("2024-01-01")!!,
            author = "John Doe"
        ),
        Article(
            news_id = 2,
            judul = "Exploring Nature: The Key to Happiness",
            short_description = "Discover how spending time in nature can boost your mood.",
            isi = """
                Nature has a profound effect on our well-being. Research suggests that spending time outdoors 
                can lower stress levels, enhance mood, and promote a sense of belonging. 
                Whether it's a walk in the park or a hike in the mountains, being in nature can help us reconnect 
                with ourselves and find happiness.
            """.trimIndent(),
            publish = dateFormat.parse("2024-01-02")!!,
            author = "Jane Smith"
        ),
    )
}

