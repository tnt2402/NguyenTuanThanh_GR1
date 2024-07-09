import pandas as pd
import numpy as np
import pathlib

code_dir = pathlib.Path(__file__).parent.resolve()

def merge():
    cars_autolist_df = pd.read_csv(code_dir/"cars_autolist.csv")
    cars_autolist_df.rename(columns={"driveline":"drivetrain"}, inplace=True)
    cars_autolist_df=cars_autolist_df.drop(['condition','previous_price','engine_cylinders','model_id','quality_score','total_price_change','rear_wheel','heated_seats','leather', 'year'],axis=1)
    cars_autolist_df['drivetrain'] = cars_autolist_df['drivetrain'].str.replace(r'[^a-zA-Z0-9]', '', regex=True)
    cars_autolist_df['drivetrain'] = cars_autolist_df['drivetrain'].str.replace(" ", "")
    car_thecarconnection_df = pd.read_csv(code_dir/"cars_thecarconnection.csv")
    car_thecarconnection_df.rename(columns={"doors":"door_count"}, inplace=True)

    df = pd.concat([car_thecarconnection_df, cars_autolist_df])
    df.drop_duplicates(subset=['vin'], keep='first',inplace=True)
    df = df[df['price'] > 0]
    df = df.map(lambda s: s.lower() if type(s) == str else s)

    # Xóa tất cả dấu space thừa trong col drivetrain
    df["drivetrain"] = df["drivetrain"].str.replace(r"[^a-zA-Z0-9]", "", regex=True)
    df["drivetrain"] = df["drivetrain"].replace("", np.nan)
    
    df.to_csv(code_dir/'merged.csv',index=False)
# merge()
