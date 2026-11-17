import requests


def extract_clinical_trials():
    # GET request for Pfizer as Lead
    query_params = {
        'query.lead' : 'pfizer',
        'pageSize' : 20
    }
    response = requests.get("https://clinicaltrials.gov/api/v2/studies", params=query_params)

    print('status code: ', response.status_code)
    
    studies = response.json().get('studies', [])
    trial_data = []
    for study in studies:
        print(study.keys())
        print(study.get('protocolSection', {}).get('identificationModule'))

        trial_dict = {}

        nct_id = study.get('protocolSection', {}).get('identificationModule', {}).get('nctId')
        trial_dict['nct_id'] = nct_id
        print('NCT ID: ', nct_id)

        title_overview = study.get('protocolSection', {}).get('identificationModule', {}).get('briefTitle')
        trial_dict['title_overview'] = title_overview
        print('title overview: ', title_overview)

        medical_title = study.get('protocolSection', {}).get('identificationModule', {}).get('officialTitle')
        trial_dict['medical_title'] = medical_title
        print('specific title: ', medical_title)

        print()

        print(study.get('protocolSection', {}).get('statusModule'))

        trial_status = study.get('protocolSection', {}).get('statusModule', {}).get('overallStatus')
        trial_dict['trial_status'] = trial_status
        print('trial overall status: ', trial_status)

        trial_start_date = study.get('protocolSection', {}).get('statusModule', {}).get('startDateStruct', {}).get('date')
        trial_dict['trial_start_date'] = trial_start_date
        print('trial start date: ', trial_start_date)

        trial_end_date = study.get('protocolSection', {}).get('statusModule', {}).get('completionDateStruct', {}).get('date')
        trial_dict['trial_end_date'] = trial_end_date
        print('trial end date: ', trial_end_date)

        trial_end_date_type = study.get('protocolSection', {}).get('statusModule', {}).get('completionDateStruct', {}).get('type')
        trial_dict['trial_end_date_type'] = trial_end_date_type
        print('trial end date type: ', trial_end_date_type)

        trial_finished_collecting_data_date = study.get('protocolSection', {}).get('statusModule', {}).get('primaryCompletionDateStruct', {}).get('date')
        trial_dict['trial_finished_collecting_data_date'] = trial_finished_collecting_data_date
        print('trial finished collecting data date: ', trial_finished_collecting_data_date)

        trial_finished_collecting_data_date_type = study.get('protocolSection', {}).get('statusModule', {}).get('primaryCompletionDateStruct', {}).get('type')
        trial_dict['trial_finished_collecting_data_date_type'] = trial_finished_collecting_data_date_type
        print('trial finished collecting data type: ', trial_finished_collecting_data_date_type)

        trial_last_update_date = study.get('protocolSection', {}).get('statusModule', {}).get('lastUpdatePostDateStruct', {}).get('date')
        trial_dict['trial_last_update_date'] = trial_last_update_date
        print('trial last update date: ', trial_last_update_date)



        print(study.get('protocolSection', {}).get('designModule'))
        trial_phases = study.get('protocolSection', {}).get('designModule', {}).get('phases')
        trial_dict['trial_phases'] = trial_phases
        print('trial phases: ', trial_phases)

        trial_treatment_purpose = study.get('protocolSection', {}).get('designModule', {}).get('designInfo', {}).get('primaryPurpose')
        trial_dict['trial_treatment_purpose'] = trial_treatment_purpose
        print('trial treatment purpose: ', trial_treatment_purpose)

        trial_enrollment = study.get('protocolSection', {}).get('designModule', {}).get('enrollmentInfo', {}).get('count')
        trial_dict['trial_enrollment'] = trial_enrollment
        print('trial enrollment: ', trial_enrollment)

        trial_enrollment_type = study.get('protocolSection', {}).get('designModule', {}).get('enrollmentInfo', {}).get('type')
        trial_dict['trial_enrollment_type'] = trial_enrollment_type
        print('trial enrollment type: ', trial_enrollment_type)

        trial_study_type = study.get('protocolSection', {}).get('designModule', {}).get('studyType')
        trial_dict['trial_study_type'] = trial_study_type
        print('trial studytype: ', trial_study_type)


        print()
        trial_conditions = study.get('protocolSection', {}).get('conditionsModule', {}).get('conditions')
        trial_dict['trial_conditions'] = trial_conditions
        print('trial conditions: ', trial_conditions)

        trial_keywords = study.get('protocolSection', {}).get('conditionsModule', {}).get('keywords')
        trial_dict['trial_keywords'] = trial_keywords
        print('trial condition keywords: ', trial_keywords)



        print()
        locations = study.get('protocolSection', {}).get('contactsLocationsModule', {}).get('locations', [])
        clean_locations = []
        for location in locations:
            clean_locations.append(
                {'facility' : location.get('facility'), 'city' : location.get('city'),
                'state' : location.get('state'), 'country' : location.get('country')}
            )
        print('clean_locations: ', clean_locations)
        trial_dict['clean_locations'] = clean_locations
        #print('trial contactsLocationsModule: ', study.get('protocolSection', {}).get('contactsLocationsModule'))


        print()
        lead_sponsor = study.get('protocolSection', {}).get('sponsorCollaboratorsModule', {}).get('leadSponsor', {}).get('name')
        trial_dict['lead_sponsor'] = lead_sponsor
        lead_sponsor_class = study.get('protocolSection', {}).get('sponsorCollaboratorsModule', {}).get('leadSponsor', {}).get('class')
        trial_dict['lead_sponsor_class'] = lead_sponsor_class
        print(lead_sponsor)
        print(lead_sponsor_class)

        trial_data.append(trial_dict)

    print("# of trials ran: ", len(trial_data))
    return trial_data