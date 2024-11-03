
package com.example.mobilehilir.data

data class AnakList(
    val child_id : Int,
    val name : String,
    val age : Int,
    val issue_name : String,
    val psikolog_id: Int
)

val listItems = listOf(
    AnakList(1, "Ravi", 8, "ADHD",1),
    AnakList(2, "Alfaiz", 6, "Autism",1),
    AnakList(3, "Bagas", 7, "Anxiety",2),
)
