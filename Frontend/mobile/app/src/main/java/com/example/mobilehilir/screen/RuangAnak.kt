package com.example.mobilehilir.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.mobilehilir.data.ChildDetail
import com.example.mobilehilir.data.Exercise
import com.example.mobilehilir.data.ExerciseList
import com.example.mobilehilir.data.assessmentItems
import com.example.mobilehilir.data.listItems
import com.example.mobilehilir.data.psikologiList

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RuangAnak(childDetail: ChildDetail) {
    val scrollBehavior = TopAppBarDefaults.pinnedScrollBehavior(rememberTopAppBarState())
    val backgroundColor = Color(0xFF3BA3FF)

    Scaffold(
        topBar = {
            Box(
                modifier = Modifier
                    .height(150.dp)
                    .fillMaxWidth()
                    .clip(
                        RoundedCornerShape(
                            bottomEnd = 20.dp,
                            bottomStart = 20.dp
                        )
                    )
                    .background(backgroundColor)
            ) {
                LargeTopAppBar(
                    colors = TopAppBarDefaults.largeTopAppBarColors(
                        containerColor = Color.Transparent,
                        titleContentColor = Color.White,
                    ),
                    title = {
                        Text(
                            text = "${childDetail.child.name}",
                            fontSize = 30.sp,
                            fontWeight = FontWeight.Bold
                        )
                    },
                    navigationIcon = {
                        IconButton(onClick = { /* Handle navigation icon click */ }) {
                            Icon(
                                imageVector = Icons.Default.ArrowBack,
                                contentDescription = "Back"
                            )
                        }
                    },
                    scrollBehavior = scrollBehavior
                )
            }
        }
    ) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp),
            verticalArrangement = Arrangement.Top
        ) {
            item {
                Text(
                    text = "Psikolog Pilihan",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    color = backgroundColor
                )
            }
            item {
                childDetail.psikolog?.let {
                    Spacer(modifier = Modifier.height(16.dp))
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .border(1.dp, Color.Black, shape = RoundedCornerShape(12.dp)),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(containerColor = Color.White)
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = "${it.full_name}",
                                fontSize = 20.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = "${it.specialization}",
                                fontSize = 15.sp,
                                color = Color.Gray
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(30.dp))
            }
            item {
                // Row for Assessments heading and button
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Assessments:",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = backgroundColor
                    )
                    Button(
                        onClick = { /* Handle Tanya Hilirian click */ },
                        colors = ButtonDefaults.buttonColors(containerColor = backgroundColor)
                    ) {
                        Text(text = "Tanya Hilirian", color = Color.White)
                    }
                }
            }
            items(childDetail.assessments) { assessment ->
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(90.dp)
                        .background(if (assessment.selesai) backgroundColor else Color.Transparent)
                        .border(
                            width = 1.dp,
                            color = if (assessment.selesai) Color.Transparent else Color.DarkGray,
                            shape = RoundedCornerShape(16.dp)
                        )
                        .padding(16.dp)
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = assessment.assesmet,
                            fontWeight = FontWeight.Bold,
                            fontSize = 21.sp,
                            color = Color.Black
                        )
                        Spacer(modifier = Modifier.height(5.dp))
                        Text(
                            text = assessment.description,
                            fontWeight = FontWeight.Normal,
                            fontSize = 13.sp,
                            color = Color.Gray
                        )
                    }
                    if (!assessment.selesai) {
                        Button(
                            onClick = { assessment.selesai = true },
                            colors = ButtonDefaults.buttonColors(containerColor = Color.DarkGray)
                        ) {
                            Text(text = "Selesai", color = Color.White)
                        }
                    }
                }
            }
            item {
                Spacer(modifier = Modifier.height(30.dp))
                // Row for Exercises heading and button
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Exercises:",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = backgroundColor
                    )
                    Button(
                        onClick = { /* Handle Tanya Hilirian click */ },
                        colors = ButtonDefaults.buttonColors(containerColor = backgroundColor)
                    ) {
                        Text(text = "Tanya Hilirian", color = Color.White)
                    }
                }
            }
            items(childDetail.exercise) { exercise ->
                Spacer(modifier = Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(90.dp)
                        .background(color = Color.Transparent)
                        .border(
                            width = 1.dp,
                            color = Color.DarkGray,
                            shape = RoundedCornerShape(16.dp)
                        )
                        .padding(16.dp)
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = exercise.exercise,
                            fontWeight = FontWeight.Bold,
                            fontSize = 21.sp,
                            color = Color.Black
                        )
                        Spacer(modifier = Modifier.height(5.dp))
                        Text(
                            text = exercise.description,
                            fontWeight = FontWeight.Normal,
                            fontSize = 13.sp,
                            color = Color.Gray
                        )
                    }
                }
            }
        }
    }
}


@Preview(showBackground = true)
@Composable
fun RuangAnakPreview() {
    val sampleChild = listItems[0]
    val samplePsychologist = psikologiList.find { it.psikolog_id == sampleChild.psikolog_id }
    val sampleAssessments = assessmentItems.filter { it.child_id == sampleChild.child_id }
    val sampleExercise = ExerciseList.filter { it.child_id == sampleChild.child_id }

    val childDetail = ChildDetail(
        child = sampleChild,
        assessments = sampleAssessments,
        psikolog = samplePsychologist,
        exercise = sampleExercise
    )

    RuangAnak(childDetail = childDetail)
}

