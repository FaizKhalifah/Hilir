package com.example.mobilehilir.data

data class AnakList(
    val child_id : Int,
    val name : String,
    val age : Int,
    val issue_name : String
)

val listItems = listOf(
    AnakList(1, "Ravi", 8, "ADHD"),
    AnakList(2, "Alfaiz", 6, "Autism"),
    AnakList(3, "Bagas", 7, "Anxiety"),
)
