# Project ERD

## Visualize ERD

![ERD](./ERD%20-%20Doctor%20Reservation%20Project.png)

---

## Entities and Relationships:

## User
### NOTE: In this project we use django default user.
Attributes: id, username, password, first_name, last_name, email

## Doctor

Attributes: id, specialty_id, phone_number, address
Relationships: One-to-One with User, Many-to-One with Specialty

## Specialty

Attributes: id, name, description

## Patient

Attributes: id, user_id, phone_number, address, date_of_birth
Relationships: One-to-One with User

## Schedule

Attributes: id, doctor_id, day_of_week, start_time, end_time
Relationships: Many-to-One with Doctor

## Appointment

Attributes: id, doctor_id, patient_id, appointment_date, appointment_time, created_at, status
Relationships: Many-to-One with Doctor, Many-to-One with Patient
