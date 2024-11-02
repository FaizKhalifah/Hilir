# app/seeds.py

from datetime import datetime, timedelta
from app.utils.db import db
from app.models.psychologist import Psychologist
from app.models.psychologist_schedule import PsychologistSchedule
from app.models.consultation import Consultation
from app.models.exercise import Exercise
from app.models.child import Child

def seed_psychologists():
    psychologists_data = [
        {
            "full_name": "Dr. John Doe",
            "email": "john.doe@psychology.com",
            "password": "password123",  # Will be hashed in the model
            "specialization": "ADHD",
            "bio": "Expert in ADHD treatment and behavioral therapy."
        },
        {
            "full_name": "Dr. Jane Smith",
            "email": "jane.smith@psychology.com",
            "password": "password123",  # Will be hashed in the model
            "specialization": "Autism",
            "bio": "Specialist in Autism Spectrum Disorder."
        },
        {
            "full_name": "Dr. Emily Johnson",
            "email": "emily.johnson@psychology.com",
            "password": "password123",  # Will be hashed in the model
            "specialization": "Anxiety",
            "bio": "Focused on managing anxiety and stress."
        }
    ]

    psychologists = []
    for data in psychologists_data:
        psychologist = Psychologist(
            full_name=data["full_name"],
            email=data["email"],
            specialization=data["specialization"],
            bio=data["bio"]
        )
        psychologist.set_password(data["password"])
        db.session.add(psychologist)
        psychologists.append(psychologist)
    db.session.commit()

    for psychologist in psychologists:
        for day in range(5):
            schedule_date = datetime.utcnow().date() + timedelta(days=day)
            schedule = PsychologistSchedule(
                psychologist_id=psychologist.id,
                schedule_date=schedule_date,
                is_available=(day % 2 == 0)
            )
            db.session.add(schedule)
    db.session.commit()

    return psychologists

def seed_exercises():
    exercises_data = [
        {"title": "Focus Exercise", "description": "Improves focus", "mental_health_issue_id": 1},  # ADHD
        {"title": "Behavior Tracking", "description": "Track behaviors daily", "mental_health_issue_id": 1},  # ADHD
        {"title": "Social Skills Practice", "description": "Practice social interactions", "mental_health_issue_id": 2},  # Autism
        {"title": "Sensory Processing", "description": "Manage sensory sensitivities", "mental_health_issue_id": 2},  # Autism
        {"title": "Breathing Exercise", "description": "Calm anxiety through breathing", "mental_health_issue_id": 3},  # Anxiety
        {"title": "Mindfulness Meditation", "description": "Increase mindfulness and reduce stress", "mental_health_issue_id": 3},  # Anxiety
    ]

    for data in exercises_data:
        exercise = Exercise(
            title=data["title"],
            description=data["description"],
            mental_health_issue_id=data["mental_health_issue_id"]
        )
        db.session.add(exercise)
    db.session.commit()

def seed_consultations(psychologists):
    for child_id in range(1, 5):
        for psychologist in psychologists:
            consultation_date = datetime.utcnow().date() - timedelta(days=child_id * 7)
            consultation = Consultation(
                child_id=child_id,
                psychologist_id=psychologist.id,
                consultation_date=consultation_date,
                is_paid=True,
                notes=f"Consultation for child {child_id} with {psychologist.specialization} specialist."
            )
            db.session.add(consultation)
    db.session.commit()

def run_seeds():
    print("Seeding psychologists and schedules...")
    psychologists = seed_psychologists()
    print("Seeding consultations...")
    seed_consultations(psychologists)
    print("Seeding exercises...")
    seed_exercises()
    print("Seeding completed!")
