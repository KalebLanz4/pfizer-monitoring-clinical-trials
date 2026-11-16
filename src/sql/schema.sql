CREATE TABLE IF NOT EXISTS clinical_trials (
    nct_id VARCHAR(11) PRIMARY KEY,
    title_overview TEXT,
    medical_title TEXT,
    trial_status TEXT,

    trial_start_date TEXT,
    trial_start_date_precision TEXT,
    trial_start_date_valid BOOLEAN,

    trial_end_date TEXT,
    trial_end_date_type TEXT,
    trial_end_date_precision TEXT,
    trial_end_date_valid BOOLEAN,

    trial_finished_collecting_data_date TEXT,
    trial_finished_collecting_data_date_type TEXT,
    trial_finished_collecting_data_date_precision TEXT,
    trial_finished_collecting_data_date_valid BOOLEAN,

    trial_last_update_date TEXT,
    trial_last_update_date_precision TEXT,
    trial_last_update_date_valid BOOLEAN,

    trial_timeline_valid BOOLEAN,

    trial_treatment_purpose TEXT,
    trial_enrollment INTEGER,
    trial_enrollment_type TEXT,
    trial_study_type TEXT,

    lead_sponsor TEXT,
    lead_sponsor_class TEXT
);