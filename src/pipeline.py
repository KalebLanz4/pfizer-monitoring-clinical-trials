from extract import extract_clinical_trials
from transform import transform_clinical_trials
from load import load_clinical_trials

# call our extract function the reads the Clinical Trial API
trial_data = extract_clinical_trials()

# call our transformation function that cleans and prepares the data
clinical_trials, trial_phases, trial_conditions, trial_locations = transform_clinical_trials(trial_data)

load_clinical_trials(clinical_trials)

