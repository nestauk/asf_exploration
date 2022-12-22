"""
Functions to download and get RECC complaints data.
"""

# package imports
import boto3
import os
import logging
import pandas as pd
import config

# paths and file names
inputs_local_path = config.inputs_local_path
s3_bucket = config.s3_bucket
s3_path = config.s3_path
raw_recc_data_filename_xlsx = config.raw_recc_data_filename_xlsx
raw_recc_data_filename_csv = config.raw_recc_data_filename_csv
outputs_local_path = config.outputs_local_path
processed_recc_data_filename = config.processed_recc_data_filename


# getter functions
def download_recc_data_from_s3():
    """
    Creates inputs folder (if does not exist) and downloads RECC data from S3
    and stores it in local inputs path (if not already there).
    """
    if not os.path.exists(inputs_local_path):
        os.mkdir(inputs_local_path)

    if not os.path.exists(inputs_local_path + raw_recc_data_filename_xlsx):
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(s3_bucket)
        bucket.download_file(
            s3_path + raw_recc_data_filename_xlsx,
            inputs_local_path + raw_recc_data_filename_xlsx,
        )
        logging.info(
            "Download of <{}> is complete!".format(raw_recc_data_filename_xlsx)
        )
    else:
        logging.info(
            "File <{}> already in local folder!".format(raw_recc_data_filename_xlsx)
        )


def raw_recc_data_to_one_sheet():
    """
    Raw RECC data comes in multiple sheets. This function adds all data to one sheet.
    The resulting data frame is stored in the inputs folder as a csv. 
    """

    sheets_names = pd.ExcelFile(
        inputs_local_path + raw_recc_data_filename_xlsx
    ).sheet_names

    raw_recc_data = pd.DataFrame()

    for sheet in sheets_names:
        aux = pd.read_excel(
            inputs_local_path + raw_recc_data_filename_xlsx, sheet_name=sheet
        )
        raw_recc_data = pd.concat([raw_recc_data, aux])

    raw_recc_data.to_csv(inputs_local_path + raw_recc_data_filename_csv)


def get_raw_recc_data() -> pd.DataFrame:
    """
    Reads raw RECC complaints data.

    Returns:
        A csv file with raw RECC complaints data.
    """
    return pd.read_csv(inputs_local_path + raw_recc_data_filename_csv)


def get_processed_recc_data() -> pd.DataFrame:
    """
    Reads processed RECC complains data.

    Returns:
        A csv file with processed RECC complaints data.
    """
    return pd.read_csv(outputs_local_path + processed_recc_data_filename)
