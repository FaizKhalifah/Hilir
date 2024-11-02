package com.example.mobilehilir.data

data class Exercise(
val child_id: Int,
val exercise: String,
val description: String,
)

val ExerciseList = listOf(
    Exercise(
        child_id = 1,
        exercise = "Deep Breathing",
        description = "A relaxation technique that involves taking slow, deep breaths to reduce stress and anxiety."
    ),
    Exercise(
        child_id = 1,
        exercise = "Mindfulness Meditation",
        description = "A practice that involves focusing on the present moment and observing thoughts without judgment."
    ),
    Exercise(
        child_id = 2,
        exercise = "Journaling",
        description = "Writing down thoughts and feelings to help process emotions and improve mental clarity."
    ),
    Exercise(
        child_id = 2,
        exercise = "Nature Walk",
        description = "Taking a walk in nature to improve mood and connect with the environment."
    ),
    Exercise(
        child_id = 3,
        exercise = "Guided Visualization",
        description = "A technique that involves imagining peaceful scenes to promote relaxation and reduce anxiety."
    ),
    Exercise(
        child_id = 3,
        exercise = "Progressive Muscle Relaxation",
        description = "A method of relaxing the body by tensing and then relaxing different muscle groups."
    ),
    Exercise(
        child_id = 4,
        exercise = "Yoga for Kids",
        description = "Simple yoga poses that promote physical and mental well-being while enhancing flexibility and relaxation."
    ),
    Exercise(
        child_id = 4,
        exercise = "Art Therapy",
        description = "Using creative activities like drawing or painting to express feelings and reduce stress."
    )
)



