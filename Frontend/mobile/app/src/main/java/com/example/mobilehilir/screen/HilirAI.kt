package com.example.mobilehilir.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HilirAI() {
    val backgroundColor = Color(0xFF3BA3FF)
    var question by remember { mutableStateOf("") }
    var response by remember { mutableStateOf("") }
    var showQuestion by remember { mutableStateOf(false) } // State to track if the question should be shown

    Scaffold(
        topBar = {
            Box(
                modifier = Modifier
                    .height(70.dp)
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(bottomEnd = 20.dp, bottomStart = 20.dp))
                    .background(backgroundColor)
            ) {
                CenterAlignedTopAppBar(
                    colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                        containerColor = Color.Transparent,
                        titleContentColor = Color.White,
                    ),
                    title = {
                        Text(
                            text = "HilirAI+",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    },
                    navigationIcon = {
                        IconButton(onClick = { /* Handle navigation icon click */ }) {
                            Icon(
                                imageVector = Icons.Default.AccountCircle,
                                contentDescription = "Profile",
                                modifier = Modifier.size(45.dp)

                            )
                        }
                    },
                    actions = {
                        IconButton(onClick = { /* Handle notifications click */ }) {
                            Icon(
                                imageVector = Icons.Default.Notifications,
                                contentDescription = "Notifikasi"
                            )
                        }
                    }
                )
            }
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Display the user's question only after the button is clicked
            if (showQuestion && question.isNotBlank()) {
                Text(
                    text = question,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                        .background(Color.LightGray, shape = RoundedCornerShape(8.dp))
                        .padding(16.dp)
                        .clip(RoundedCornerShape(8.dp)) // Round corners for question
                )
            } else if (question.isBlank()) {
                Spacer(modifier = Modifier.height(8.dp)) // Add space if there's no question
            }

            // Display the API response
            if (response.isNotBlank()) {
                Spacer(modifier = Modifier.height(8.dp)) // Space between question and response
                Text(
                    text = response,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(8.dp)
                        .background(Color.LightGray, shape = RoundedCornerShape(8.dp))
                        .padding(16.dp)
                        .clip(RoundedCornerShape(8.dp)) // Round corners for response
                )
            } else if (response.isBlank() && showQuestion) {
                Spacer(modifier = Modifier.height(8.dp)) // Add space if there's no response
            }

            // Row to hold TextField and Submit Button
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // Input Field
                TextField(
                    value = question,
                    onValueChange = { question = it },
                    label = { Text("Ask a question...") },
                    modifier = Modifier
                        .weight(1f)
                        .border(1.dp, Color.Black, RoundedCornerShape(8.dp)), // Add border with rounded corners
                    colors = TextFieldDefaults.textFieldColors(
                        containerColor = Color.Transparent, // Make the background transparent
                        focusedIndicatorColor = Color.Transparent, // Remove the focused underline
                        unfocusedIndicatorColor = Color.Transparent // Remove the unfocused underline
                    )
                )

                // Submit Button
                Button(
                    onClick = {
                        // Here you would send the question to your API
                        // Example: response = sendQuestionToApi(question)
                        response = "Q : $question" // Mock response
                        showQuestion = true // Set the flag to show the question
                        question = "" // Clear the input field
                    },
                    colors = ButtonDefaults.buttonColors(backgroundColor),
                    modifier = Modifier.padding(start = 8.dp)
                ) {
                    Text("Ask")
                }
            }
        }
    }
}

@Preview(showBackground = true)
@Composable
fun PreviewChatScreen() {
    HilirAI()
}
