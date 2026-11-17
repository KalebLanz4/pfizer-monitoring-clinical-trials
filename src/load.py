import psycopg
import pandas as pd


def load_clinical_trials(clinical_trials):
    
    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

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

