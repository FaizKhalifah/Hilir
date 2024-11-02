package com.example.mobilehilir.navigation

sealed class Screen(val route: String) {
    object ruangHilir : Screen("ruang_hilir")
    object hilirAI : Screen("hilir_ai")
    object artikel : Screen("artikel")
    object ruangAnak : Screen("ruang_anak/{child_id}") // Add this line
}

