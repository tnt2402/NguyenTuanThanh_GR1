import pandas as pd
import threading
import ssl
import concurrent.futures
import cloudscraper
# url = "https://www.thecarconnection.com/inventory?zip=07001&distance=500&page="

# data=carconnection.manage_crawling(url)

# write_to_csv(data,'data.csv' )
import pathlib
import os
code_dir = pathlib.Path(__file__).parent.resolve()

df=pd.read_csv(code_dir/'../data/thecarconnection.csv')
if os.path.exists(code_dir/"../data/cars_thecarconnection.csv"):
    crawled_df=pd.read_csv(code_dir/"../data/cars_thecarconnection.csv")
    df=df[df['id'].isin(crawled_df['id']) ==False]
else:
    pd.DataFrame({
                'id': [],
                'vin':[],
                'name':[],
                'make_name':[],
                'model_name':[],
                'price':[],
                'transmission':[],
                'trim':[],
                'drivetrain':[],
                'normalized_color_exterior':[],
                'normalized_color_interior':[],
                'fuel_type': [],
                'doors': [],
                'body_style': [],
                'mileage': [],
                'year':[],
    }).to_csv(code_dir/"../data/cars_thecarconnection.csv",index=False)


def call_api(id):
    scraper = cloudscraper.CloudScraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            
        },
        ssl_context=ssl._create_unverified_context()
    )
    headers = {
    "accept": "application/json",
    "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "priority": "u=1, i",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x_requested_with": "XMLHttpRequest"
    }
    num_retries=10
    url='https://www.thecarconnection.com/inventory/get-listing/'
    num_attempts = 0
    while num_attempts < num_retries:
        try:
            response = scraper.get(url+str(id), headers=headers)
            return response.json()['listing']
        except response.exceptions.RequestException as e:
            print(f"Lỗi xảy ra khi gọi API: {e}")
            num_attempts += 1
            if num_attempts < num_retries:
                print(f"Đang thử lại lần {num_attempts}...")
            else:
                print("Đã hết số lần thử lại. Không thể gọi API.")
                raise e



def process_chunk(df_chunk):
    results = []
    cnt=0
    for index, row in df_chunk.iterrows():
        car_id = row['id']
        car_info = call_api(car_id)
        
        # Thêm thông tin về door vào kết quả
        result = {
            'id': car_id,
            'vin':row['vin'],
            'name':row['name'],
            'make_name':row['make_name'],
            'model_name':row['model_name'],
            'price':row['price'],
            'transmission':row['transmission'],
            'trim':row['trim'],
            'drivetrain':row['drivetrain'],
            'normalized_color_exterior':row['normalized_color_exterior'],
            'normalized_color_interior':row['normalized_color_interior'],
            'fuel_type': car_info['fuelType'],
            'doors': car_info['doors'],
            'body_style': car_info['segment'],
            'mileage': row['mileage'],
            'year': row['year'],
        }
        cnt+=1
        results.append(result)
        pd.DataFrame([result]).to_csv(code_dir/'../data/cars_thecarconnection.csv',mode='a',header=None,index=False)
        if(cnt%50==0) :print('progress',cnt/len(df_chunk))
    return pd.DataFrame(results)

import numpy as np
# Chia dataframe thành 10 phần
print(len(df))
num_rows = 10
df_chunks =  [df[i::10] for i in range(10)]
def get_detail_car():
    # Xử lý các phần dataframe song song
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_chunk, df_chunks))