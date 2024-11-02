# app/seeds.py

from app.models.personalization_question import PersonalizationQuestion
from app.models.question_mental_health import QuestionMentalHealth
from app.models.mental_health_issue import MentalHealthIssue
from app.utils.db import db

def seed_questions():
    # Mental health issues
    adhd = MentalHealthIssue(name="ADHD", threshold_score=5)
    autism = MentalHealthIssue(name="Autism", threshold_score=5)
    anxiety = MentalHealthIssue(name="Anxiety", threshold_score=5)
    db.session.add_all([adhd, autism, anxiety])
    db.session.commit()
    
    # Questions and their impacts
    questions = [
        ("Does your child have difficulty focusing?", adhd.id, 2),
        ("Does your child exhibit repetitive actions?", autism.id, 3),
        ("Does your child have difficulty socializing?", autism.id, 2),
        ("Does your child seem overly anxious?", anxiety.id, 3),
        ("Does your child have trouble sitting still?", adhd.id, 2),
        ("Does your child avoid eye contact?", autism.id, 3),
        ("Does your child experience frequent mood changes?", anxiety.id, 2),
        ("Does your child have trouble following instructions?", adhd.id, 3),
        ("Does your child display a lack of interest in social activities?", autism.id, 2),
        ("Does your child often feel worried or fearful?", anxiety.id, 3)
    ]
    
    for text, issue_id, impact in questions:
        question = PersonalizationQuestion(question=text)
        db.session.add(question)
        db.session.flush()  # Gets the question.id after insertion
        relation = QuestionMentalHealth(question_id=question.id, mental_health_issue_id=issue_id, score_impact=impact)
        db.session.add(relation)
    
    db.session.commit()
