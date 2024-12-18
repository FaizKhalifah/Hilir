
package com.example.mobilehilir.data

fun getAssessmentsForChild(childId: Int): List<Assesment> {
    return assessmentItems.filter { it.child_id == childId }
}

fun getExercisesForChild(childId: Int): List<Exercise> {
    return ExerciseList.filter { it.child_id == childId }
}

fun getPsikologForChild(psikologId: Int): Psikologi? {
    return psikologiList.find { it.psikolog_id == psikologId }
}

fun getChildDetailById(childId: Int): ChildDetail? {
    return listItems.find { it.child_id == childId }?.let { child ->
        val assessments = getAssessmentsForChild(childId)
        val exercises = getExercisesForChild(childId)
        val psikolog = getPsikologForChild(child.psikolog_id)
        ChildDetail(child, assessments, exercises, psikolog)
    }
}



data class ChildDetail(
    val child: AnakList,
    val assessments: List<Assesment>,
    val exercise: List<Exercise>,
    val psikolog: Psikologi?
)
