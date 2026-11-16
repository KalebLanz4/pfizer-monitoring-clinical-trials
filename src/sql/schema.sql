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

CREATE TABLE IF NOT EXISTS trial_phases (
    nct_id VARCHAR(11) NOT NULL,
    trial_phases TEXT NOT NULL,

    PRIMARY KEY (nct_id, trial_phases),
    FOREIGN KEY (nct_id) REFERENCES clinical_trials(nct_id)
);


CREATE TABLE IF NOT EXISTS trial_conditions (
    nct_id VARCHAR(11) NOT NULL,
    trial_conditions TEXT NOT NULL,

    PRIMARY KEY (nct_id, trial_conditions),
    FOREIGN KEY (nct_id) REFERENCES clinical_trials(nct_id)
);


CREATE TABLE if NOT EXISTS trial_locations (
    location_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    nct_id VARCHAR(11) NOT NULL,
    facility TEXT,
    city TEXT,
    state TEXT,
    country TEXT,

    FOREIGN KEY (nct_id) REFERENCES clinical_trials(nct_id)
);