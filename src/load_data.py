import os 
import yaml
import pandas as pd
import argparse
from pkgutil import get_data
from get_data import get_data, read_params



def load_and_save(config_path):
    config = read_params(config_path)
    df = get_data(config_path)
    df = preprocess_data(df)
    new_cols = [col.replace(" ", "_") for col in df.columns]
    raw_data_path = config['load_data']['raw_dataset_csv']
    df.to_csv(raw_data_path, sep=',', index=False, header=new_cols)
    


def preprocess_data(df):
    df['Journey_Day']=df['Date_of_Journey'].apply(lambda x: x.split('/')[0])
    df['Journey_month']=df['Date_of_Journey'].apply(lambda x: x.split('/')[1])
    df.drop('Date_of_Journey',axis=1,inplace=True)
    df.dropna(inplace=True)
    df['Dep_Hour']=df['Dep_Time'].apply(lambda x: x.split(':')[0])
    df['Dep_Min']=df['Dep_Time'].apply(lambda x: x.split(':')[1])
    df.drop('Dep_Time',axis=1,inplace=True)
    df['Arrival_Hour']=pd.to_datetime(df['Arrival_Time']).dt.hour  
    df['Arrival_min']=pd.to_datetime(df['Arrival_Time']).dt.minute
    df.drop('Arrival_Time',axis=1,inplace=True)
    duration=list(df['Duration'])
    for i in range(len(duration)):
        if len(duration[i].split())!=2:
            if 'h' in duration[i]:
                duration[i]=duration[i].strip() + " 0m "
            else:
                duration[i]=' 0h ' + duration[i] 
    duration_hours=[]
    duration_mins=[]
    for i in range(len(duration)):
        duration_hours.append(int(duration[i].split(sep='h')[0]))
        duration_mins.append(int(duration[i].split(sep='m')[0].split()[-1]))
    df['Duration_hours']=duration_hours
    df['Duration_mins']=duration_mins
    df.drop('Duration',axis=1,inplace=True)
    df.drop(['Route','Additional_Info'],axis=1,inplace=True)
    df.replace({'non-stop':0, '1 stop':1, '2 stops':2, '3 stops':3, '4 stops':4},inplace=True)
    df['Airline'].replace({
        'IndiGo':0, 'Air India':1, 'Jet Airways':2, 'SpiceJet':3, 'Multiple carriers':4, 'GoAir':5,
        'Vistara':6, 'Air Asia':7, 'Vistara Premium economy':8, 'Jet Airways Business':9, 'Multiple carriers Premium economy':10,
        'Trujet':11
    }, inplace=True)
    df['Source'].replace({
        'Banglore':0, 'Kolkata':1, 'Delhi':2, 'Chennai':3, 'Mumbai':4
    }, inplace=True)
    df['Destination'].replace({
        'Banglore':0, 'Kolkata':1, 'Delhi':2, 'New Delhi':2, 'Cochin':3, 'Hyderabad':4
    }, inplace=True)
    return df



if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)