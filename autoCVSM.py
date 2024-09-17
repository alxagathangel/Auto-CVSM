import os
import pandas as pd
from connection import *
from mail import *
from plotting import *
import passkeys as pk

def plot_excel(df,file_name,new_dir_path):
    try:
        plotBar(df,file_name,new_dir_path)
        plotArea(df,file_name,new_dir_path)
        plotBox(df,file_name,new_dir_path)

        print(f"- Plots saved to {new_dir_path}.")
        mail_img(file_name,new_dir_path)
    except Exception as e:
        print(f">> Error saving plots: {e}")


def clean_excel(file_name):
    file_path = os.path.join(input_dir,file_name)
    df = pd.read_excel(file_path)

    before = len(df.index)

    seenVars = ['seen','Seen','SEEN']
    deliVars = ['delivered','Delivered','DELIVERED']

    df.rename(columns={'minimata':'msgs_count'},inplace=True)

    df.dropna(inplace=True)

    df['full_date'] = pd.to_datetime(df['full_date'],errors='coerce')

    if df['account_id'].nunique() == 1:
        thisID = df['account_id'].iloc[0]
    else:
        thisID = df['account_id'].mode()[0]
    df['account_id'] == thisID

    df = df[ df['msgs_count'] > 0 ]

    df = df[ df['im_state'].isin(seenVars + deliVars) ]

    after = len(df.index)
    print(f"- Deleted {before-after} row(s).")

    return df


def process(input_dir,output_dir):

    excel_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.xlsx')]
    if not excel_files:
        print(">> ERROR: No Excel files found in input directory.")
        return
    
    os.makedirs(output_dir,exist_ok=True)

    for file_name in excel_files:
        print(f"\n\nProcessing file: {file_name}...")

        df = clean_excel(file_name)

        new_dir_path = os.path.join(output_dir,f'{os.path.splitext(file_name)[0]}_folder')
        if not os.path.exists(new_dir_path):
            os.mkdir(new_dir_path)
            print(f"- Created path {new_dir_path}.")
        else:
            print(f"- Path {new_dir_path} already exists.") 
        output_path = os.path.join(new_dir_path,f'clean_{file_name}')
        df.to_excel(output_path,index=False)

        db_name = file_name.split('.')[0]+'_db'
        create_database_Alchemy(db_name,df)

        plot_excel(df,file_name,new_dir_path)

    print("\n\nProcess completed for all files.\n")


input_dir = pk.input_dir
output_dir = pk.output_dir

if not os.path.exists(input_dir):
    print(f">> ERROR: Directory {input_dir} does not exist.")
else:
    if not os.listdir(input_dir):
        print(f">> ERROR: Directory {input_dir} is empty.")
    else:
        print(f".\n.\n.\n-> Input Directory Content:\n{os.listdir(input_dir)}\n")
        process(input_dir,output_dir)
        print(f"-> Output Directory Content:\n{os.listdir(output_dir)}.\n.\n.")
