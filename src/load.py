import psycopg
import pandas as pd


def load_trials(clinical_trials, trial_phases, trial_conditions, trial_locations):
    
    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

            trial_ids = clinical_trials['nct_id']

            load_clinical_trials(clinical_trials, cursor)
            load_trial_phases(trial_phases, cursor, trial_ids)
            load_trial_conditions(trial_conditions, cursor, trial_ids)
            load_trial_locations(trial_locations, cursor, trial_ids)



def load_trial_locations(trial_locations, cursor, trial_ids):
    column_list = trial_locations.columns.tolist()
    placeholders = ', '.join(['%s'] * len(column_list))

    columns = ', '.join(column_list)


    # Delete old trial locations of the new trial locations that are being inserted
    query_delete = f"""
                    DELETE FROM trial_locations WHERE nct_id = %s
                    """

    # Insert the trial location value into the trial_locations table
    query_insert = f"""
            INSERT INTO trial_locations ({columns})
            VALUES ({placeholders})
            """

    # Delete all records in trial_location that have their nct_id in clinical_trials
    for nct_id in trial_ids:
        cursor.execute(query_delete, [nct_id])

    for index, row in trial_locations.iterrows():
        nct_id = row['nct_id']
        facility = row['facility']
        city = row['city']
        state = row['state']
        country = row['country']

        # Converting NaN to None when loading into PostgreSQL
        record = [nct_id, facility, city, state, country]
        for i in range(len(record)):
            if pd.isna(record[i]):
                record[i] = None

        cursor.execute(query_insert, record)


def load_trial_conditions(trial_conditions, cursor, trial_ids):
    column_list = trial_conditions.columns.tolist()
    placeholders = ', '.join(['%s'] * len(column_list))

    columns = ', '.join(column_list)

    query_delete = "DELETE FROM trial_conditions WHERE nct_id = %s"
    
    # Delete all records that contain the nct_id from this new batch to update the condtions table
    for nct_id in trial_ids:
        cursor.execute(query_delete, [nct_id])

    # Insert (nct_id, condition)
    query = f"""
            INSERT INTO trial_conditions ({columns})
            VALUES ({placeholders})
            """
    for index, row in trial_conditions.iterrows():
        nct_id = row['nct_id']
        condition = row['trial_conditions']

        cursor.execute(query, [nct_id,condition])



def load_trial_phases(trial_phases, cursor, trial_ids):

    column_list = trial_phases.columns.tolist()
    placeholders = ', '.join(['%s'] * len(column_list))

    columns = ', '.join(column_list)


    query_delete = "DELETE FROM trial_phases WHERE nct_id = %s"

    # Delete all records that contain the nct_id from this new batch to update the phase
    for nct_id in trial_ids:
        cursor.execute(query_delete, [nct_id])

    # insert the (nct_id, phase)
    query = f"""
            INSERT INTO trial_phases ({columns})
            VALUES ({placeholders})
            """

    for index, row in trial_phases.iterrows():
        nct_id = row['nct_id']
        phase = row['trial_phases']

        cursor.execute(query, [nct_id, phase])


      
def load_clinical_trials(clinical_trials, cursor):
    columns = clinical_trials.columns.tolist()
    updated_columns = columns.copy()

    # remove nct_id from updated
    updated_columns.remove('nct_id')

    # insert statement
    insert_columns = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))

    # update statement
    updates = ', '.join(f'{column} = EXCLUDED.{column}' for column in updated_columns)

    # get the current values from the record
    old_values = ', '.join(f'clinical_trials.{column}' for column in updated_columns)

    # get the new values that could be added
    new_values = ', '.join(f'EXCLUDED.{column}' for column in updated_columns)

    # insert the record if there is no conflict on nct_id
    # update the record (besides nct_id) when the new values are different than the old values
    query = f"""
            INSERT INTO clinical_trials ({insert_columns})
            VALUES ({placeholders})
            ON CONFLICT (nct_id)
            DO UPDATE SET {updates}
            WHERE ROW({old_values}) IS DISTINCT FROM ROW({new_values})
            """

    # conert the dataframe into a list of dictionaries
    for row in clinical_trials.to_dict(orient='records'):
        for column in row:
            # convert NaN to None for PSQL
            if pd.isna(row[column]):
                row[column] = None

        # Collect the values from this row
        record = [row[column] for column in columns]

        cursor.execute(query, record)