    package com.example.mobilehilir.screen

    import android.widget.TextView
    import androidx.compose.foundation.background
    import androidx.compose.foundation.layout.*
    import androidx.compose.foundation.shape.RoundedCornerShape
    import androidx.compose.material.icons.Icons
    import androidx.compose.material.icons.filled.AccountCircle
    import androidx.compose.material.icons.filled.ArrowBack
    import androidx.compose.material.icons.filled.Notifications
    import androidx.compose.material3.*
    import androidx.compose.runtime.Composable
    import androidx.compose.ui.Alignment
    import androidx.compose.ui.Modifier
    import androidx.compose.ui.draw.clip
    import androidx.compose.ui.graphics.Color
    import androidx.compose.ui.text.font.FontWeight
    import androidx.compose.ui.tooling.preview.Preview
    import androidx.compose.ui.unit.dp
    import androidx.compose.ui.unit.sp
    import com.example.mobilehilir.data.Article
    import java.text.SimpleDateFormat
    import java.util.*

    @OptIn(ExperimentalMaterial3Api::class)
    @Composable
    fun ArticleDetail(article: Article) {
        val backgroundColor = Color(0xFF3BA3FF)

        Scaffold(
            topBar = {
                Box(
                    modifier = Modifier
                        .height(70.dp)
                        .fillMaxWidth()
                        .clip(
                            RoundedCornerShape(
                                bottomEnd = 20.dp,
                                bottomStart = 20.dp
                            )
                        )
                        .background(backgroundColor)
                ) {
                    CenterAlignedTopAppBar(
                        colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                            containerColor = Color.Transparent,
                            titleContentColor = Color.White,
                        ),
                        title = {
                            Text(
                                text = "Berita Hilirian",
                                fontSize = 30.sp,
                                fontWeight = FontWeight.Bold
                            )
                        },
                        navigationIcon = {
                            IconButton(onClick = { /* Handle navigation icon click */ }) {
                                Icon(
                                    imageVector = Icons.Default.ArrowBack,
                                    contentDescription = "Profile",
                                    modifier = Modifier.size(45.dp)
                                )
                            }
                        },
                    )
                }
            }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
                    .padding(16.dp),
                horizontalAlignment = Alignment.Start,
                verticalArrangement = Arrangement.Top
            ) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "${article.judul}",
                    fontSize = 45.sp,
                    fontWeight = FontWeight.Bold
                )
                // Article Meta Data
                Text(
                    text = "By: ${article.author}",
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(article.publish),
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Light,
                    modifier = Modifier.padding(bottom = 8.dp)
                )

                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = article.isi,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Normal
                )
            }
        }
    }

    @Preview(showBackground = true)
    @Composable
    fun PreviewArticleDetail() {
        val sampleArticle = Article(
            news_id = 1,
            judul = "Sample Article",
            short_description = "This is a short description of the sample article.",
            isi = "Here is the full content of the sample article. It discusses various points related to the topic. " +
                    "This text will occupy more space to illustrate how the UI adapts when there is a lot of content. " +
                    "Adding more lines to ensure it takes up the screen properly, making the reading experience better.",
            publish = Date(), // Use the current date for the preview
            author = "Jane Doe"
        )
        ArticleDetail(article = sampleArticle)
    }
