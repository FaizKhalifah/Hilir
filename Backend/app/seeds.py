from datetime import datetime, timedelta
from app.utils.db import db
from app.models.psychologist import Psychologist
from app.models.psychologist_schedule import PsychologistSchedule
from app.models.consultation import Consultation
from app.models.child import Child

def seed_psychologists():
    # Psychologists data
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

    # Creating psychologists
    psychologists = []
    for data in psychologists_data:
        psychologist = Psychologist(
            full_name=data["full_name"],
            email=data["email"],
            specialization=data["specialization"],
            bio=data["bio"]
        )
        psychologist.set_password(data["password"])  # Hash password
        db.session.add(psychologist)
        psychologists.append(psychologist)
    db.session.commit()

    # Psychologist schedules
    for psychologist in psychologists:
        for day in range(5):  # Creating a schedule for 5 days
            schedule_date = datetime.utcnow().date() + timedelta(days=day)
            schedule = PsychologistSchedule(
                psychologist_id=psychologist.id,
                schedule_date=schedule_date,
                is_available=(day % 2 == 0)  # Alternate days as available/unavailable
            )
            db.session.add(schedule)
    db.session.commit()

    return psychologists

def seed_consultations(psychologists):
    # Create consultations for children with IDs 1-4
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
    print("Seeding completed!")

