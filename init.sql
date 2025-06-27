-- Create tables
CREATE TABLE patients (
                          patient_id TEXT PRIMARY KEY,
                          first_name TEXT,
                          last_name TEXT,
                          gender TEXT,
                          date_of_birth DATE,
                          age int64,
                          address TEXT,
                          city TEXT,
                          state TEXT,
                          zip_code INTEGER,
                          phone_number TEXT
);

CREATE TABLE encounters (
                            encounter_id TEXT PRIMARY KEY,
                            patient_id TEXT REFERENCES patients(patient_id),
                            visit_type TEXT,
                            admission_date DATE,
                            discharge_date DATE,
                            attending_physician_id TEXT
);

CREATE TABLE observations (
                              observation_id TEXT PRIMARY KEY,
                              patient_id TEXT REFERENCES patients(patient_id),
                              encounter_id TEXT REFERENCES encounters(encounter_id),
                              observation_code TEXT,
                              observation_description TEXT,
                              observation_datetime TIMESTAMP,
                              units TEXT,
                              value_numeric NUMERIC,
                              value_text TEXT
);

CREATE TABLE diagnoses (
                           diagnosis_id TEXT PRIMARY KEY,
                           patient_id TEXT REFERENCES patients(patient_id),
                           encounter_id TEXT REFERENCES encounters(encounter_id),
                           diagnosis_code TEXT,
                           diagnosis_description TEXT,
                           date_recorded DATE
);

CREATE TABLE procedures (
                            procedure_id TEXT PRIMARY KEY,
                            patient_id TEXT REFERENCES patients(patient_id),
                            encounter_id TEXT REFERENCES encounters(encounter_id),
                            procedure_code INTEGER,
                            procedure_description TEXT,
                            date_performed DATE
);

CREATE TABLE medications (
                             medication_order_id TEXT PRIMARY KEY,
                             patient_id TEXT REFERENCES patients(patient_id),
                             encounter_id TEXT REFERENCES encounters(encounter_id),
                             drug_code INTEGER,
                             drug_name TEXT,
                             dosage TEXT,
                             route TEXT,
                             frequency TEXT,
                             start_date DATE,
                             end_date DATE
);