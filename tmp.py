from datetime import datetime, timedelta
from google.cloud import storage
import json
import csv
import pandas
import requests
import os
import glob
import sys
import re
import time
import logging
from config import (BUSINESS_UNIT_ID,
                    CUSTOM_CONV_DEVICES,
                    CUSTOM_CONV_FORFAIT,
                    CUSTOM_CONV_FIXE,
                    TOKEN_ID,
                    FACEBOOK_BUCKET
                    )


def store_file_to_gcs(input_path, path_on_gcs):
    """ Store a file on Google Cloud Storage (input name = name on GCS)

    Args:
        input_fule (string): path of the file to upload on GCS
    Returns:
        blob.public_url (string): path of the file uploaded on GCS 

    """
    client = storage.Client()
    bucket = client.get_bucket(FACEBOOK_BUCKET)
    blob = bucket.blob(path_on_gcs)
    blob.upload_from_filename(input_path)
    return blob.public_url


def get_facebook_api_data(requested_data_type, custom_conversion_id):
    """Call the Facebook Attribution API, extract the JSON response and remove unnecessary data. 

    Args:
        requested_data_type (string): either channel or campaigns
        custom_conversion_id (int): ID provived by Facebook based on the conversion model
        business_unit_id (int): ID speficif to the RED-SFR app. Available directly on developers.facebook 

    Returns:
        facebook_attribution_data_list (list): list of items requested for the dashboard 
    Raises:
        Exception: if the response from the API call is empty or does not contain the appropriate data 

    Facebook Attribution API documentation: https://developers.facebook.com/docs/marketing-api/attribution/
    """

    if requested_data_type == 'channels':
        url = 'https://graph.facebook.com/v9.0/?ids=' + BUSINESS_UNIT_ID + \
            '&fields=conversion_events.filter_by({"ids":[' + custom_conversion_id + ']}).metric_scope({"filters":{"click_lookback_window":"2419200","view_lookback_window":"86400","visit_configuration":"include_paid_organic"},"time_period":"last_thirty_days"}){id,name,cost_per_1k_impressions,cost_per_click,cost_per_visit,net_media_cost,report_click_through_rate,report_clicks,report_impressions,report_visits,last_touch_convs,last_touch_convs_per_1k_impress,last_touch_convs_per_click,last_touch_convs_per_visit,last_touch_cpa,last_touch_revenue,last_touch_roas,total_conversions,metrics_breakdown.dimensions(["source_channel"]){source_channel,last_click_convs,last_click_revenue,data_driven_convs,data_driven_revenue}}&access_token='
    else:
        url = f'https://graph.facebook.com/v9.0/?ids=' + BUSINESS_UNIT_ID + \
            '&fields=conversion_events.filter_by( {"ids":[' + custom_conversion_id + ']}).count(1).summary(1).metric_scope({"filters":{"click_lookback_window":"2419200","view_lookback_window":"86400","visit_configuration":"include_paid_organic","version_id":"latest"},"should_include_prior_period":false,"time_period":"yesterday", "metric_context":{"active_pane":"ALL_CHANNELS"}}){alias,id,name, metrics_breakdown.dimensions(["campaign_id"]).limit(500){campaign_id,timestamp, campaign_name,net_media_cost,last_click_convs, last_click_revenue}}&access_token='
    try:
        facebook_request_url = ''.join([
            url,
            TOKEN_ID
        ])
        facebook_request_url = re.sub("'", "", facebook_request_url)
        request = requests.get(facebook_request_url)
        response_to_json = request.json()
        facebook_attribution_data_list = response_to_json[BUSINESS_UNIT_ID][
            'conversion_events']['data'][0]['metrics_breakdown']['data']
        return facebook_attribution_data_list
    except Exception as e:
        logging.error("An error occured during the API call for the custom conversion id: " +
                      custom_conversion_id + " with the error: ", e)
        sys.exit()


def list_to_csv(input_list, csv_path):
    """ Convert a single list to a .csv file 

    Args:
        input_list (list): list of items
        csv_path (string): name of the .csv final file
    Returns:
        csv_path (string): name of the .csv final file

    """
    with open(csv_path, 'w', newline='') as outfile:
        w = csv.DictWriter(outfile, fieldnames=input_list[0].keys())
        w.writeheader()
        w.writerows(input_list)
    return csv_path


def add_static_columns_to_csv(csv_path, dataframes):
    """ Add one or multiple columns to a csv file 

    Args:
        input_list (list): list of items
        csv_path (string): name of the .csv final file
    Returns:
        csv_path (string): name of the .csv final file

    """
    for dataframe in dataframes:
        csv_input = pandas.read_csv(csv_path)
        cols = [x for x in csv_input.columns]
        csv_input[dataframe[0]] = dataframe[1]
        csv_input = csv_input[[dataframe[0], *cols]]
        csv_input.to_csv(csv_path, index=0)
    return dataframes


def convert_to_date(timestamps):
    """Convert a list of timestramps to dates 

    Args:
        timestamps (list): list of timestamps

    Returns:
        dates (list): list of dates YYYY-MM-DD
    """
    dates = []
    for timestamp in timestamps:
        dt_object = datetime.fromtimestamp(timestamp)
        dates.append(dt_object.date())
    return dates


def timestamp_to_date(dataframe):
    """ Convert timestamp to a date - <METHOD NOT USED ANYMORE AS WE ARE NOT REQUIREMENT TO GET THE DATE AS THE IMPORT IS DAILY FOR YESTERDAY>
    """
    df = dataframe.rename(columns={'timestamp': 'date'})
    df['date'] = convert_to_date(df['date'])
    return df


def csv_to_dataFrame(csv_path):
    """Convert a .csv file to a Pandas dataframe object

    Args:
        csv_path (string): path of a .csv file 

    Returns:
        df (Dataframe): dataframe object 
    """
    df = pandas.DataFrame(data=pandas.read_csv(csv_path))
    df.to_csv(csv_path, index=0)
    return df


def get_yesterday_date():
    """ Get the date of yesterday - The reason is we call the Facebook attribution API with the parameter "time_period":"yesterday".

    Returns:
        date (string): YYYY-MM-DD
    """
    today = datetime.today()
    yesterday = (today - timedelta(days=1))
    return yesterday.strftime('%Y-%m-%d')


def get_campaign_additional_columns(input_campaign_data):
    custom_conversion_name = 'total-fixe'
    if re.search('devices', input_campaign_data[0]):
        custom_conversion_name = 'total-device'
    if re.search('forfait', input_campaign_data[0]):
        custom_conversion_name = 'total-forfait'
    return [('custom_conversion_id', input_campaign_data[1]), ('custom_conversion_name', custom_conversion_name), ('datetime', get_yesterday_date())]


def combine_dataframes_to_csv(list_of_dataframes_files, outputfile):
    """ Combine a list of pandas Dataframes to a single .csv file

    Args:
        list_of_dataframes_files (list): list of pandas Dataframes
        outputfile (string): name of the final .csv file 

    """
    df = pandas.concat(list_of_dataframes_files)
    df.to_csv(outputfile, index=0)


def helper(dataset, facebook_type):
    dataframes = []
    for data in dataset:
        json_api_response_data = get_facebook_api_data(facebook_type, data[1])
        csv_file = list_to_csv(json_api_response_data, data[0])
        add_static_columns_to_csv(
            csv_file, get_campaign_additional_columns(data))
        dataframe = csv_to_dataFrame(data[0])
        dataframes.append(dataframe)
        time.sleep(7)
    return dataframes


def generate_report_name(type):
    """ Generate the name of the report to be stored on Google Cloud Storage 

    Args:
        type (string): either campaigns or channels 

    Returns:
        name (string): YYYY-MM-DD_type.csv 
    """
    yesterday = get_yesterday_date()
    name = f"{yesterday}_{type}.csv"
    return name



def extract_and_store_facebook_reports(extract_type):
    folder_name = 'tmp/'
    csv_file_local_name = generate_report_name(extract_type)
    local_path_csv_file = folder_name + csv_file_local_name

    export_data = [ (f'{folder_name}{extract_type}_{CUSTOM_CONV_DEVICES[0]}.csv', CUSTOM_CONV_DEVICES[1]),
                    (f'{folder_name}{extract_type}_{CUSTOM_CONV_FORFAIT[0]}.csv',  CUSTOM_CONV_FORFAIT[1]),
                    (f'{folder_name}{extract_type}_{CUSTOM_CONV_FIXE[0]}.csv',  CUSTOM_CONV_FIXE[1])]


    csv_dataframes_to_merge = helper(export_data, extract_type)
    combine_dataframes_to_csv(csv_dataframes_to_merge, local_path_csv_file)
    store_file_to_gcs(local_path_csv_file, csv_file_local_name)

    
extract_and_store_facebook_reports('campaigns')
extract_and_store_facebook_reports('channels')
