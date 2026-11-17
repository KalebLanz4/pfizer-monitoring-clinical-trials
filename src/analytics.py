import psycopg


def trials_each_status():
    # Get the trial status and the count of trial statues, grouped by the trial statues
    query = """
            SELECT trial_status, COUNT(*) 
            FROM clinical_trials
            GROUP BY trial_status
            ORDER BY COUNT(*) DESC
            """
    
    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

            cursor.execute(query)
            result = cursor.fetchall()
            print("Clincal Trials Statuses: \n")
            for status, count in result:
                print(f"{status}: {count}")
            

def upcoming_trials(days):
    if days < 0:
        return "Please Enter a positive amount of days"

    # Select the title overview and trial end date of the sample for only estiamted end dates and the end date is valid and in progress
    # And also where adding the input days to the current day comes before the date of the samples
    # ordered by the dates that are closest to the current date
    query = """
            SELECT title_overview, trial_end_date
            FROM clinical_trials
            WHERE trial_end_date_type = 'ESTIMATED' 
            AND trial_end_date_valid = TRUE AND
            trial_status NOT IN ('COMPLETED', 'TERMINATED' , 'WITHDRAWN')
            AND (
            ( trial_end_date BETWEEN TO_CHAR(CURRENT_DATE, 'YYYY-MM-DD') AND TO_CHAR(CURRENT_DATE + %s, 'YYYY-MM-DD') 
            AND trial_end_date_precision = 'DAY' )
            OR
            ( trial_end_date_precision = 'MONTH'
            AND trial_end_date BETWEEN
            TO_CHAR(CURRENT_DATE, 'YYYY-MM') 
            AND TO_CHAR(CURRENT_DATE + %s, 'YYYY-MM') )
            )
            ORDER BY trial_end_date ASC
            """

    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

            cursor.execute(query, [days, days])
            result = cursor.fetchall()
            print("Clincal Trials Upcoming Completion dates: \n")
            for title_overview, trial_end_date in result:
                print(f"{title_overview}: {trial_end_date}")


def medical_conditions(limit):
    # Select the trial condiction and count of each condtion, group by the trial conditions and sort from high to low of the count of condtions
    query = """
            SELECT trial_conditions, COUNT(*) 
            FROM trial_conditions
            GROUP BY trial_conditions
            ORDER BY COUNT(*) DESC
            LIMIT %s
            """

    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

            cursor.execute(query, [limit])
            result = cursor.fetchall()
            print("Clincal Trials Most Popular Conditions: \n")
            for trial_conditions, count in result:
                print(f"{trial_conditions}: {count}")

def country_most_research(limit):
    # Select the country and the count of how many times each country appears, grouped by the country and ordered from most to least 
    query= """
            SELECT country, COUNT(*) 
            FROM trial_locations
            GROUP BY country
            ORDER BY COUNT(*) DESC
            LIMIT %s
            """
    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

            cursor.execute(query, [limit])
            result = cursor.fetchall()
            print("Countries with the Most Clinical Trial Research Locations:\n")
            for country, count in result:
                print(f"{country}: {count}")


def avg_patient_enrollment():
    # Select the trial phase and trial_enrollement, from clinical_trials inner joined by trial_phases, grouped by the trial phases
    query = """
            SELECT tp.trial_phases, ROUND(AVG(ct.trial_enrollment), 2)
            FROM clinical_trials ct
            INNER JOIN trial_phases tp ON ct.nct_id = tp.nct_id
            GROUP BY tp.trial_phases
            """

    with psycopg.connect('dbname=pfizer_clinical_trials') as conn:
        print('Successfully connected')

        with conn.cursor() as cursor:
            print('Cursor is created')

            cursor.execute(query)
            result = cursor.fetchall()
            print("Average patient Enrollment For Each Phase:\n")
            for trial_phases, AVG in result:
                print(f"{trial_phases}: {AVG}")


def main():
    print()
    print("Pfizer Clincial Trial Analytics")
    print("1.) How many Pfizer clinical trials are currently recruiting, completed, or in other statuses? ")
    print('2.) Which ongoing clinical trials have upcoming estimated completion dates?')
    print('3.) Which medical conditions have the most Pfizer clinical trials?')
    print('4.) Which countries have the most clinical trial research locations?')
    print('5.) What is the average patient enrollment for clinical trials in each phase?')

    print()
    choice = input("Select an option: ")

    if choice == '1':
        trials_each_status()
    elif choice == '2':
        days = int(input("How many days ahead would you like to search? "))
        upcoming_trials(days)
    elif choice == '3':
        limit = int(input("How many of the top medical conditions would you like to see? "))
        medical_conditions(limit)
    elif choice == '4':
        limit = int(input("How many top countries would you like to see? "))
        country_most_research(limit)
    elif choice == '5':
        avg_patient_enrollment()
    else:
        print('Incorrect input, Please enter a number 1-5')


if __name__ == "__main__":
    main()


