package com.example.mobilehilir.navigation

    sealed class Screen(val route:String) {
        object ruang_hilir : Screen("Ruang Hilir")
        object teman_hilir : Screen("Teman Hilir")
        object psikolog : Screen("Psikolog")
}