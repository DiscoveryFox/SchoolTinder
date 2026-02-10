import sqlite3
import random
import time
from faker import Faker
from datetime import datetime

# Konfiguration
DB_NAME = "schooltinder.db"
NUM_PROFILES = 100_000
BATCH_SIZE = 10000  

# Faker initialisieren (optional: locale='de_DE' für deutsche Daten)
fake = Faker('de_DE')



def generate_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fremdschlüssel aktivieren
    # Tabellen erstellen
    print(f"Starte Generierung von {NUM_PROFILES} Profilen...")
    start_time = time.time()

    # Wir nutzen eine einzige Transaktion für maximale Geschwindigkeit
    cursor.execute("BEGIN TRANSACTION")

    try:
        for i in range(NUM_PROFILES):
            # 1. USER erstellen
            username = fake.user_name()
            email = fake.email()
            password = fake.sha256() # Simulierter Hash
            
            cursor.execute("INSERT INTO User (username, email, password) VALUES (?, ?, ?)", 
                           (username, email, password))
            
            # Die ID des gerade erstellten Users holen
            user_id = cursor.lastrowid

            # 2. PROFILE erstellen
            first_name = fake.first_name()
            last_name = fake.last_name()
            # Datum in Unix Timestamp umwandeln
            dob_date = fake.date_of_birth(minimum_age=18, maximum_age=90)
            dob_timestamp = int(datetime(dob_date.year, dob_date.month, dob_date.day).timestamp())
            gender = random.choice([0, 1]) # 0=M, 1=W (Beispiel)
            address = fake.address().replace("\n", ", ")
            hair_colour = random.choice(["Blond", "Brunette", "Black", "Red", "Grey", "White"])

            cursor.execute("""
                INSERT INTO Profile (user_id, first_name, last_name, date_of_birth, gender, home_address, hair_colour) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, first_name, last_name, dob_timestamp, gender, address, hair_colour))
            
            profile_id = cursor.lastrowid

            # 3. PREFERENCES erstellen
            age_base = random.randint(18, 80)
            lower_bound = max(18, age_base - 5)
            upper_bound = age_base + 5
            sex_pref = random.choice([0, 1, 2]) # 0=M, 1=W, 2=Both

            cursor.execute("""
                INSERT INTO Preferences (profile_id, lower_age_bound, upper_age_bound, sexual_preference)
                VALUES (?, ?, ?, ?)
            """, (profile_id, lower_bound, upper_bound, sex_pref))

            # 4. PICTURES erstellen (0 bis 3 Bilder pro Profil)
            for _ in range(random.randint(0, 3)):
                path = f"/images/{profile_id}/{fake.file_name(extension='jpg')}"
                cursor.execute("INSERT INTO Pictures (profile_id, path) VALUES (?, ?)", (profile_id, path))

            # 5. HOBBIES erstellen (1 bis 4 Hobbys pro Profil)
            # Einfache Liste von Hobbys, damit es realistisch aussieht
            possible_hobbies = ["Fußball", "Lesen", "Reisen", "Kochen", "Gaming", "Musik", "Wandern", "Kino", "Tanzen"]
            
            # Wähle 1-3 zufällige Hobbys aus
            selected_hobbies = random.sample(possible_hobbies, k=random.randint(1, 3))
            
            for hobby in selected_hobbies:
                cursor.execute("INSERT INTO Hobby (profile_id, hobby_name) VALUES (?, ?)", (profile_id, hobby))

            # Fortschrittsanzeige
            if (i + 1) % BATCH_SIZE == 0:
                print(f"{i + 1} Profile erstellt...")

        # Alles auf einmal festschreiben
        conn.commit()
        
    except Exception as e:
        print(f"Fehler aufgetreten: {e}")
        conn.rollback() # Änderungen rückgängig machen bei Fehler
    finally:
        conn.close()

    end_time = time.time()
    duration = end_time - start_time
    print(f"Fertig! {NUM_PROFILES} Profile in {duration:.2f} Sekunden erstellt.")

if __name__ == "__main__":
    generate_data()