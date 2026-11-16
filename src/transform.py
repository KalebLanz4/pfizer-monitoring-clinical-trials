import pandas as pd
from datetime import datetime

def transform_clinical_trials(trial_data):
    df = pd.DataFrame(trial_data)
    print('df.shape: ', df.shape)
    # check out many columns contain null
    print(df.isnull().sum())

    # drop duplicates if any have the same id
    print(df.duplicated(subset=['nct_id']))
    df = df.drop_duplicates(subset=['nct_id'])

    # check the length of the clean_location list
    print(df['clean_locations'].apply(len))

    date_columns = ['trial_start_date','trial_end_date', 'trial_finished_collecting_data_date','trial_last_update_date']

    

    for column in date_columns:
        df[column + '_precision'] = df[column].apply(get_date_format)
        df[column + '_valid'] = df[column].apply(validate_data)


    # check if the timelines make sense date wise
    df['trial_timeline_valid'] = df.apply(valid_timeline, axis=1)


    # create a new table for trial phases
    trial_phases = df[['nct_id', 'trial_phases']].explode('trial_phases')
    trial_phases = trial_phases.dropna(subset=['trial_phases'])

    # create a new table for trial medical conditions
    trial_conditions = df[['nct_id', 'trial_conditions']].explode('trial_conditions')
    trial_conditions = trial_conditions.dropna(subset=['trial_conditions'])

    # create a table for the trial locations
    trial_locations = df[['nct_id','clean_locations']].explode('clean_locations')
    trial_locations = trial_locations.dropna(subset=['clean_locations'])
    # fix the duplicate index problem
    trial_locations = trial_locations.reset_index(drop=True)
    # turn the json dictionary to column and values
    location_detail = pd.json_normalize(trial_locations['clean_locations'])
    #concat the locationdetial table with the correct nct_id
    trial_locations = trial_locations[['nct_id']].join(location_detail)

    # remove the columns that are in the other tables we created (where the values are lists)
    clinical_trials = df.drop(columns=['trial_phases', 'trial_conditions', 'clean_locations', 'trial_keywords'])

    return clinical_trials, trial_phases, trial_conditions, trial_locations


def valid_timeline(row):
    start_date = row['trial_start_date']
    end_date = row['trial_end_date']

    if pd.isna(start_date) or pd.isna(end_date):
        return None

    if not row['trial_start_date_valid'] or not row['trial_end_date_valid']:
            return False

    start_month = start_date[:7]
    end_month = end_date[:7]

    if start_month != end_month:
        return start_month < end_month

    if len(start_date) == 10 and len(end_date) == 10:
        return start_date <= end_date

    return True



def get_date_format(date):
    if pd.isna(date):
        return None

    if len(date) == 7:
        return "MONTH"

    if len(date) == 10:
        return "DAY"

    return "INVALID"

def validate_data(date):
    if pd.isna(date):
        return True

    try: 
        if len(date) == 7:
            datetime.strptime(date, "%Y-%m")

        elif len(date) == 10:
            datetime.strptime(date, "%Y-%m-%d")

        else:
            return False
        
        return True

    except ValueError:
        return False


