package com.example.mobilehilir

import ChildrenViewModel
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Create
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.mobilehilir.data.getDummyArticles
import com.example.mobilehilir.navigation.NavigationItem
import com.example.mobilehilir.navigation.Screen
import com.example.mobilehilir.screen.ArticleDetail
import com.example.mobilehilir.screen.Artikel
import com.example.mobilehilir.screen.HilirAI

import com.example.mobilehilir.screen.RuangHilir
import com.example.mobilehilir.ui.theme.MobileHilirTheme
import androidx.lifecycle.viewmodel.compose.viewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MobileHilirTheme {
                MainScreen()
            }
        }
    }
}

@Composable
private fun MainScreen(
    navController: NavHostController = rememberNavController(),
    modifier: Modifier = Modifier,
    viewModel: ChildrenViewModel = viewModel()
) {
    Scaffold(
        bottomBar = { BottomBar(navController) },
        modifier = modifier
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.ruangHilir.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.ruangHilir.route) {
                // Call `getAllChildren` to fetch data when `RuangHilir` is loaded
                LaunchedEffect(Unit) {
                    viewModel.getAllChildren()
                }
                RuangHilir(navController = navController, viewModel = viewModel)
            }
//            composable(
//                route = "ruangAnak/{childId}",
//                arguments = listOf(navArgument("childId") { type = NavType.IntType })
//            ) { backStackEntry ->
//                val childId = backStackEntry.arguments?.getInt("childId") ?: 0
//                RuangAnak(navController, childId)
//            }
            composable(Screen.hilirAI.route) {
                HilirAI()
            }
            composable(Screen.artikel.route) {
                Artikel(navController)
            }
            composable(
                route = "articleDetail/{news_id}",
                arguments = listOf(navArgument("news_id") { type = NavType.IntType })
            ) { backStackEntry ->
                val newsId = backStackEntry.arguments?.getInt("news_id") ?: 0
                val article = getDummyArticles().find { it.news_id == newsId } // Fetch the article based on news_id
                if (article != null) {
                    ArticleDetail(article, navController) // Pass the navController here
                }
            }
        }
    }
}

@Composable
private fun BottomBar(
    navController: NavController,
    modifier: Modifier = Modifier
) {
    val currentBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = currentBackStackEntry?.destination?.route

    val navigationItems = listOf(
        NavigationItem(
            title = "Ruang Hilir",
            icon = Icons.Default.Home,
            selectedIcon = Icons.Filled.Home,
            screen = Screen.ruangHilir
        ),
        NavigationItem(
            title = "Hilir AI+",
            icon = Icons.Default.Search,
            selectedIcon = Icons.Filled.Search,
            screen = Screen.hilirAI
        ),
        NavigationItem(
            title = "Artikel",
            icon = Icons.Default.Create,
            selectedIcon = Icons.Filled.Create,
            screen = Screen.artikel
        )
    )

    val backgroundColor = Color(0xFF3BA3FF)
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(topStart = 20.dp, topEnd = 20.dp))
            .background(backgroundColor)
    ) {
        NavigationBar(modifier = modifier, containerColor = backgroundColor) {
            navigationItems.forEach { item ->
                val isSelected = currentRoute == item.screen.route

                NavigationBarItem(
                    label = {
                        Text(
                            text = item.title,
                            fontWeight = FontWeight.Bold,
                            fontSize = 14.sp,
                            color = if (isSelected) Color.White else Color.LightGray
                        )
                    },
                    alwaysShowLabel = false,
                    selected = isSelected,
                    onClick = {
                        if (!isSelected) {
                            navController.navigate(item.screen.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                restoreState = true
                                launchSingleTop = true
                            }
                        }
                    },
                    icon = {
                        Icon(
                            imageVector = if (isSelected) item.selectedIcon else item.icon,
                            contentDescription = item.title,
                            tint = if (isSelected) Color.White else Color.LightGray
                        )
                    }
                )
            }
        }
    }
}
