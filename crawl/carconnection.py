import ssl
import threading
import requests
import json
import csv
import cloudscraper
import urllib3
from streamlit.runtime.scriptrunner import add_script_run_ctx
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from datetime import datetime

total_urls = 0
data_lock = threading.Lock()
processed_urls = 0
car_crawls = 0
counter_lock = threading.Lock()
data_cars = []
def get_current_time_string():
    # Get the current time
    now = datetime.now()
    # Format the time as YYYYMMDD_HHMMSS
    time_string = now.strftime("%Y%m%d_%H%M%S")
    return time_string

def write_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def crawl_url(url,my_bar):
    global processed_urls,data_cars
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
    response = scraper.get(url, headers=headers)
    data = json.loads(response.text)['data']
    list_of_cars = data['listings']
    tmp_cars = []
    # print("    Number of cars: %s\n" % len(list_of_cars))
    if len(list_of_cars) > 0:
        for car in list_of_cars:
            tmp_car = {}
            tmp_car['id'] = car['id']
            tmp_car['vin'] = car['vin']
            tmp_car['name'] = car['make'] + ' ' + car['model']
            tmp_car['make_name'] = car['make']
            tmp_car['model_name'] = car['model']
            tmp_car['price'] = car['price']
            tmp_car['transmission'] = car['transmission']
            tmp_car['trim'] = car['trim']
            tmp_car['year'] = car['year']
            tmp_car['drivetrain'] = car['drivetrain']
            tmp_car['normalized_color_exterior'] = car['exteriorColor']
            tmp_car['normalized_color_interior'] = car['interiorColor']

            tmp_car['mileage'] = car['mileage']
            tmp_cars.append(tmp_car)
            
    with data_lock:
        data_cars.extend(tmp_cars)
        print('crawled car',len(data_cars))
    with counter_lock:
        processed_urls += 1
        progress = (processed_urls / total_urls) 
        print(f'Progress: {progress:f}')
        my_bar.progress(progress)
        print(f'processed_urls: {processed_urls:.2f}')
        print(f'total_urls: {total_urls:.2f}')
           


def manage_crawling(url,my_bar):
    threads = []
    urls=[]
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
 
 
    print('Starting crawling',url)
    response = scraper.get(url, headers=headers)
    data = json.loads(response.text)['data']
    total_page=data['numberOfPages']
    global total_urls
    total_urls=total_page
    print('total_urls', total_urls)
    for page_id in range(1,total_page+1):
        urls.append(url+str(page_id))
    # Create and start 10 threads
    while urls:
        for _ in range(10):
            if urls:
                url = urls.pop(0)
                t = threading.Thread(target=crawl_url, args=(url,my_bar,))
                t.start()
                threads.append(t)
                add_script_run_ctx(t)
        
        # Wait for all threads to finish
        for t in threads:
            t.join()
        threads.clear()
    
   

def crawl_pages(url):
    # bypass cloudflare
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
    
    results = []
    count_car = 0
    print('Starting crawling')
    response = scraper.get(url+"1", headers=headers)
    data = json.loads(response.text)['data']
    total_page=data['numberOfPages']
    print("    total_page:" , (total_page))
    
    for page_id in range(1,total_page+1):
        print("[+] Page : %i\n" % page_id)
        page_url = url + str(page_id)

        response = scraper.get(page_url, headers=headers)
        
        # Parse the JSON response
        data = json.loads(response.text)['data']
        list_of_cars = data['listings']
        if len(list_of_cars) > 0:
            for car in list_of_cars:
                tmp_car = {}
                tmp_car['id'] = car['id']
                tmp_car['vin'] = car['vin']
                tmp_car['name'] = car['make'] + ' ' + car['model']
                tmp_car['make_name'] = car['make']
                tmp_car['model_name'] = car['model']
                tmp_car['price'] = car['price']
                tmp_car['transmission'] = car['transmission']
                tmp_car['trim'] = car['trim']
                tmp_car['year'] = car['year']
                tmp_car['drivetrain'] = car['drivetrain']
                tmp_car['normalized_color_exterior'] = car['exteriorColor']
                tmp_car['normalized_color_interior'] = car['interiorColor']

                tmp_car['mileage'] = car['mileage']
                results.append(tmp_car)
                count_car += 1
        print("count_car:" , (count_car))
     
    print("[+] Total cars: %d\n" % count_car)
    return results

def crawl_all_car(st):
    st.write("#### Crawling basic info from car connection")

    progress_text = "Operation in progress. Please wait."
    # global my_bar
    my_bar = st.progress(0, text=progress_text)
    url = "https://www.thecarconnection.com/inventory?zip=07001&distance=150&page="
    manage_crawling(url,my_bar)
    write_to_csv(data_cars, 'data/thecarconnection'  + '.csv' )


# # old car with new-flag=0
# url = "https://www.thecarconnection.com/blocks/listings-ppc/retrieve?numListings=2000&numColumns=4&model=&zip=90245&range=&new-flag=&category=&categories=&year-low=&year-high=&price-low=&price-high=&noprice-flag=1&make="

# make_brands = [
#     'acura', 'alfa-romeo', 'audi', 'bmw', 'buick', 'cadillac', 'chevrolet', 'chrysler', 'dodge', 'fiat', 'ford', 'genesis', 'gmc', 'honda', 'hyundai', 'infiniti', 'jaguar', 'jeep', 'kia', 'land-rover', 'lexus', 'lincoln', 'lucid', 'mazda', 'mercedes-benz', 'mini', 'mitsubishi', 'nissan', 'polestar', 'porsche', 'ram', 'rivian', 'subaru', 'tesla', 'toyota', 'volkswagen', 'volvo'
# ]
# make_brands = ['acura']

# new car with new-flag=0
# url = "https://www.thecarconnection.com/inventory?zip=07001&distance=50&page="
# all_results = manage_crawling(url)
    

# # all_results.extend(crawl_pages(url, make_brands))


