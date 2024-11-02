# app/seeds.py

from app.models import (
    Parent,
    Psychologist,
    Child,
    Consultation,
    Assessment,
    Exercise,
    ChildExercise,
    ChildPersonalization,
    MentalHealthIssue,
    OTPVerification,
    PersonalizationQuestion,
    PersonalizationResponse,
    PsychologistSchedule,
    QuestionMentalHealth,
    Report,
)
from app.utils.db import db


def seed_database():
    # Seeding Mental Health Issues
    adhd = MentalHealthIssue(name="ADHD", description="Attention Deficit Hyperactivity Disorder", threshold_score=10)
    anxiety = MentalHealthIssue(name="Anxiety", description="Anxiety Disorder", threshold_score=8)
    autism = MentalHealthIssue(name="Autism", description="Autism Spectrum Disorder", threshold_score=15)
    db.session.add_all([adhd, anxiety, autism])
    db.session.commit()

    # Seeding Parents
    parent1 = Parent(username="parent1", email="parent1@example.com")
    parent1.set_password("password1")
    parent2 = Parent(username="parent2", email="parent2@example.com")
    parent2.set_password("password2")
    parent3 = Parent(username="parent3", email="parent3@example.com")
    parent3.set_password("password3")
    db.session.add_all([parent1, parent2, parent3])
    db.session.commit()

    # Seeding Psychologists
    psychologist1 = Psychologist(full_name="Dr. Smith", email="psych1@example.com", specialization="ADHD")
    psychologist1.set_password("password1")
    psychologist2 = Psychologist(full_name="Dr. Johnson", email="psych2@example.com", specialization="Anxiety")
    psychologist2.set_password("password2")
    psychologist3 = Psychologist(full_name="Dr. Brown", email="psych3@example.com", specialization="Autism")
    psychologist3.set_password("password3")
    db.session.add_all([psychologist1, psychologist2, psychologist3])
    db.session.commit()

    # Seeding Children
    child1 = Child(name="Child1", gender="Male", date_of_birth="2015-03-25", parent_id=parent1.id)
    child2 = Child(name="Child2", gender="Female", date_of_birth="2016-05-12", parent_id=parent2.id)
    child3 = Child(name="Child3", gender="Male", date_of_birth="2014-08-19", parent_id=parent3.id)
    db.session.add_all([child1, child2, child3])
    db.session.commit()

    # Seeding Consultations
    consultation1 = Consultation(child_id=child1.id, psychologist_id=psychologist1.id, consultation_date="2024-01-01", is_paid=True)
    consultation2 = Consultation(child_id=child2.id, psychologist_id=psychologist2.id, consultation_date="2024-02-01", is_paid=True)
    consultation3 = Consultation(child_id=child3.id, psychologist_id=psychologist3.id, consultation_date="2024-03-01", is_paid=True)
    db.session.add_all([consultation1, consultation2, consultation3])
    db.session.commit()

    # Seeding Assessments
    assessment1 = Assessment(child_id=child1.id, psychologist_id=psychologist1.id, task_description="Behavioral Therapy", due_date="2024-02-01", frequency=48)
    assessment2 = Assessment(child_id=child2.id, psychologist_id=psychologist2.id, task_description="Cognitive Therapy", due_date="2024-03-01", frequency=72)
    assessment3 = Assessment(child_id=child3.id, psychologist_id=psychologist3.id, task_description="Speech Therapy", due_date="2024-04-01", frequency=24)
    db.session.add_all([assessment1, assessment2, assessment3])
    db.session.commit()

    # Seeding Exercises
    exercise1 = Exercise(title="Mindfulness Practice", mental_health_issue_id=anxiety.id)
    exercise2 = Exercise(title="Focus Exercises", mental_health_issue_id=adhd.id)
    exercise3 = Exercise(title="Social Skills Training", mental_health_issue_id=autism.id)
    db.session.add_all([exercise1, exercise2, exercise3])
    db.session.commit()

    # Seeding Child Exercises
    child_exercise1 = ChildExercise(child_id=child1.id, exercise_id=exercise1.id, assigned_date="2024-02-05")
    child_exercise2 = ChildExercise(child_id=child2.id, exercise_id=exercise2.id, assigned_date="2024-03-05")
    child_exercise3 = ChildExercise(child_id=child3.id, exercise_id=exercise3.id, assigned_date="2024-04-05")
    db.session.add_all([child_exercise1, child_exercise2, child_exercise3])
    db.session.commit()

    # Seeding Child Personalizations
    personalization1 = ChildPersonalization(child_id=child1.id, mental_health_issue_id=anxiety.id, personalization_score=5)
    personalization2 = ChildPersonalization(child_id=child2.id, mental_health_issue_id=adhd.id, personalization_score=8)
    personalization3 = ChildPersonalization(child_id=child3.id, mental_health_issue_id=autism.id, personalization_score=12)
    db.session.add_all([personalization1, personalization2, personalization3])
    db.session.commit()

    # Seeding OTP Verifications
    otp1 = OTPVerification(parent_id=parent1.id, otp_code="123456", expiration_date="2024-03-01")
    otp2 = OTPVerification(parent_id=parent2.id, otp_code="654321", expiration_date="2024-04-01")
    otp3 = OTPVerification(parent_id=parent3.id, otp_code="112233", expiration_date="2024-05-01")
    db.session.add_all([otp1, otp2, otp3])
    db.session.commit()

    # Seeding Personalization Questions
    question1 = PersonalizationQuestion(assessment_id=assessment1.id, question="How often does the child feel anxious?")
    question2 = PersonalizationQuestion(assessment_id=assessment2.id, question="How often does the child have trouble focusing?")
    question3 = PersonalizationQuestion(assessment_id=assessment3.id, question="How well does the child communicate with others?")
    db.session.add_all([question1, question2, question3])
    db.session.commit()

    # Seeding Personalization Responses
    response1 = PersonalizationResponse(child_id=child1.id, question_id=question1.id, response_score=4)
    response2 = PersonalizationResponse(child_id=child2.id, question_id=question2.id, response_score=3)
    response3 = PersonalizationResponse(child_id=child3.id, question_id=question3.id, response_score=5)
    db.session.add_all([response1, response2, response3])
    db.session.commit()

    # Seeding Psychologist Schedules
    schedule1 = PsychologistSchedule(psychologist_id=psychologist1.id, schedule_date="2024-03-05")
    schedule2 = PsychologistSchedule(psychologist_id=psychologist2.id, schedule_date="2024-04-05")
    schedule3 = PsychologistSchedule(psychologist_id=psychologist3.id, schedule_date="2024-05-05")
    db.session.add_all([schedule1, schedule2, schedule3])
    db.session.commit()

    # Seeding Question Mental Health
    question_mental_health1 = QuestionMentalHealth(question_id=question1.id, mental_health_issue_id=anxiety.id, score_impact=2)
    question_mental_health2 = QuestionMentalHealth(question_id=question2.id, mental_health_issue_id=adhd.id, score_impact=3)
    question_mental_health3 = QuestionMentalHealth(question_id=question3.id, mental_health_issue_id=autism.id, score_impact=1)
    db.session.add_all([question_mental_health1, question_mental_health2, question_mental_health3])
    db.session.commit()

    # Seeding Reports
    report1 = Report(child_id=child1.id, report_data="Initial observation report for Child1.")
    report2 = Report(child_id=child2.id, report_data="Initial observation report for Child2.")
    report3 = Report(child_id=child3.id, report_data="Initial observation report for Child3.")
    db.session.add_all([report1, report2, report3])
    db.session.commit()

    print("Seeding completed successfully.")