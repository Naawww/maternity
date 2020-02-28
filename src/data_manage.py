import pathlib
import re
import pandas as pd

"""
Ok, so it seems there are actually three different file types:
msds
msms 2019-04 to 2019-08
msms < 2019-04

For now, just focus on the last one, it's got the most data.
"""

data_path = pathlib.Path(__file__).parents[1] / 'data'

def pull_csvs(glob_mask: str = '*.csv'):
    """
    This convenience function loads the maternity csvs. I've made it add the file name as some of the files have
    columns that are all over the place. It combines the csvs into a dataframe end on end.
    :param glob_mask: str
        this should be a glob expression to pull the required csvs
    :return concatenated_dataframe : pd.Dataframe
    """
    file_paths = data_path.glob(glob_mask)

    df_list = []
    for path in file_paths:
        df = pd.read_csv(path)
        df['file'] = path.name
        df_list.append(df)
    return pd.concat(df_list, axis=0, ignore_index=True)

def maternity_data():
    """
    Convenience function to get the raw maternity monthly data. Simply returns a dictionary maternity dataframes (for
    each file schema).
    :return dict_of_maternity_dataframes : dict
    """
    msds_df = pull_csvs("*msds*.csv")
    msms_df = pull_csvs("*msms*.csv")
    # some weird stuff going on here.
    # ['01/04/2019' '01/08/2019' '2019-07-01' '2019-06-01' '01/05/2019']
    # these files have a different structure
    start_date_blank_period = msms_df[msms_df.Period.isna()].ReportingPeriodStartDate.unique()
    msms_2_df = msms_df[msms_df.ReportingPeriodStartDate.isin(start_date_blank_period)]
    msms_1_df = msms_df[~msms_df.ReportingPeriodStartDate.isin(start_date_blank_period)]
    return dict(msds=msds_df, msms_1 = msms_1_df, msms_2 = msms_2_df)
