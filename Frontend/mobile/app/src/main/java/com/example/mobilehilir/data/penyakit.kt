package com.example.mobilehilir.data

data class penyakit(
    val id : Int,
    val namaPenyakit : String,
    val detail : String
)


val penyakitList = listOf(
        penyakit(
            id = 1,
            namaPenyakit = "Anxiety Disorder",
            detail = "Anxiety disorder is characterized by feelings of worry, anxiety, or fear that are strong enough to interfere with daily activities. Common symptoms include restlessness, fatigue, and difficulty concentrating."
        ),
        penyakit(
            id = 2,
            namaPenyakit = "ADHD",
            detail = "ADHD is a disorder marked by an ongoing pattern of inattention and/or hyperactivity-impulsivity that interferes with functioning or development. Symptoms include difficulty staying focused, hyperactivity, and impulsive behavior."
        ),
        penyakit(
            id = 3,
            namaPenyakit = "ASD",
            detail = "ASD is a developmental disorder that affects communication and behavior. It is known for challenges with social skills, repetitive behaviors, and communication difficulties, but each case is unique."
        ),
        penyakit(
            id = 4,
            namaPenyakit = "Depression",
            detail = "Depression is a mood disorder that causes a persistent feeling of sadness and loss of interest. It can affect how you feel, think, and handle daily activities, such as sleeping, eating, or working."
        ),
        penyakit(
            id = 5,
            namaPenyakit = "OCD",
            detail = "OCD is a disorder in which people have recurring, unwanted thoughts (obsessions) that drive them to do repetitive behaviors (compulsions). These behaviors can significantly interfere with daily activities."
        )
    )

