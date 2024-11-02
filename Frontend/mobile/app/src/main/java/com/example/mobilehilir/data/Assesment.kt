package com.example.mobilehilir.data

data class Assesment(
    val child_id: Int,
    val assesmet: String,
    val description: String,
    val dueDate: String,
    var selesai: Boolean
)

val assessmentItems = listOf(
    Assesment(1, "Speech Therapy", "Practice pronunciation of basic words", "11-02-2024", false),
    Assesment(1, "Behavioral Exercise", "Follow a simple routine for 30 minutes", "15-02-2024",false),
    Assesment(1, "Music Therapy", "Listen to and mimic calming melodies", "18-02-2024", false),

    Assesment(2, "Occupational Therapy", "Engage in sensory play activities", "12-02-2024", false),
    Assesment(2, "Social Skills Training", "Practice greeting others in a friendly manner", "16-02-2024", false),
    Assesment(2, "Art Therapy", "Create a simple art project using safe materials", "20-02-2024", false),

    Assesment(3, "Mindfulness Exercise", "Practice deep breathing for relaxation", "13-02-2024", false),
    Assesment(3, "Cognitive Exercise", "Solve basic puzzles to improve concentration", "17-02-2024", false),
    Assesment(3, "Story Time", "Read a story and discuss the main characters", "21-02-2024", false)
)



