# Project ERD

## Visualize ERD

![ERD](ERD%20-%20Doctor%20Reservation%20System.png)

---

## Entities and Relationships:

## User
### NOTE: In this project we use django default user.
Attributes: id, username, password, first_name, last_name, email

## Doctor

Attributes: id, specialty_id, phone_number, address, fee, created, updated
Relationships: One-to-One with User, Many-to-One with Specialty

## Specialty

Attributes: id, name, description, created, updated

## Patient

Attributes: id, user_id, phone_number, address, date_of_birth, wallet, created, updated
Relationships: One-to-One with User

## Schedule

Attributes: id, doctor_id, day_of_week, start_time, end_time, created, updated
Relationships: Many-to-One with Doctor

## Appointment

Attributes: id, doctor_id, patient_id, start_date, attended, created, updated
Relationships: Many-to-One with Doctor, Many-to-One with Patient

## Comment

Attributes: id, patient_id, doctor_id, title, content, created, updated
Relationships: Many-to-One with Doctor, Many-to-One with Doctor

## Rate

Attributes: id, patient_id, doctor_id, score, created, updated
Relationships: Many-to-One with Doctor, Many-to-One with Doctor