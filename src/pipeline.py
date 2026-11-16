from extract import extract_clinical_trials
from transform import transform_clinical_trials

trial_data = extract_clinical_trials()

clinical_trials, trial_phases, trial_conditions, trial_locations = transform_clinical_trials(trial_data)



