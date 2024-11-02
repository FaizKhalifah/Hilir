package com.example.mobilehilir.data

data class Psikologi(
    val psikolog_id: Int,
    val full_name: String,
    val email: String,
    val password: String,
    val specialization: String,
    val bio: String
)

val psikologiList = listOf(
    Psikologi(
        psikolog_id = 1,
        full_name = "Dr. Anita Putri",
        email = "anita.putri@example.com",
        password = "securePassword1",
        specialization = "Child Psychology",
        bio = "Dr. Anita Putri has 10 years of experience specializing in child psychology and therapy for ADHD and anxiety disorders."
    ),
    Psikologi(
        psikolog_id = 2,
        full_name = "Dr. Budi Santoso",
        email = "budi.santoso@example.com",
        password = "securePassword2",
        specialization = "Behavioral Therapy",
        bio = "Dr. Budi Santoso focuses on behavioral therapy techniques to help children manage symptoms of autism and develop social skills."
    ),
    Psikologi(
        psikolog_id = 3,
        full_name = "Dr. Clara Wijaya",
        email = "clara.wijaya@example.com",
        password = "securePassword3",
        specialization = "Cognitive Development",
        bio = "Dr. Clara Wijaya is an expert in cognitive development, assisting children in overcoming learning difficulties and enhancing concentration."
    )
)

