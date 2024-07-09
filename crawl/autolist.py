import requests
import json
import csv

def write_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def crawl_pages(url,my_bar):
    page = 1
    results = []
    count_car = 0
    while True:
        print("[+] Page: %d\n" % page)
        my_bar.progress(page/6)
        page_url = url + str(page)
        # Send a GET request to the URL
        response = requests.get(page_url)
        # Parse the JSON response
        data = json.loads(response.text)

        list_of_cars = data['records']
        if len(list_of_cars) > 0:
            for car in list_of_cars:
                tmp_car = {}
                tmp_car['id'] = car['id']
                tmp_car['vin'] = car['vin']
                tmp_car['name'] = car['make_name'] + ' ' + car['model_name']
                tmp_car['model_id'] = car['model_id']
                tmp_car['make_name'] = car['make_name']
                tmp_car['model_name'] = car['model_name']
                tmp_car['body_style'] = car['body_style']
                tmp_car['condition'] = car['condition']

                tmp_car['door_count'] = car['door_count']
                tmp_car['driveline'] = car['driveline']
                tmp_car['engine_cylinders'] = car['engine_cylinders']
                tmp_car['fuel_type'] = car['fuel_type']
                tmp_car['previous_price'] = car['previous_price']
                tmp_car['price'] = car['price']
                tmp_car['quality_score'] = car['quality_score']
                tmp_car['transmission'] = car['transmission']
                tmp_car['trim'] = car['trim']
                tmp_car['year'] = car['year']
                tmp_car['total_price_change'] = car['total_price_change']
                tmp_car['rear_wheel'] = car['rear_wheel']
                tmp_car['heated_seats'] = car['heated_seats']
                tmp_car['leather'] = car['leather']
                tmp_car['normalized_color_exterior'] = car['normalized_color_exterior']
                tmp_car['normalized_color_interior'] = car['normalized_color_interior']

                tmp_car['mileage'] = car['mileage']
                results.append(tmp_car)
                count_car += 1
        else:
            break
    
        page += 1
    
    print("[+] Total cars: %d\n" % count_car)
    return results

# Example usage
url="https://www.autolist.com/api/v2/search?ads=true&include_total_price_change=true&include_time_on_market=true&include_relative_price_difference=true&latitude=21.0292&limit=2000&longitude=105.8526&radius=Any&page="


def crawl_autolist(st):
    st.write("#### Crawling car from autolist")
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    all_results = crawl_pages(url,my_bar)
    st.write('crawled:',len(all_results),'cars')
    # print(all_results)
    write_to_csv(all_results, 'data/cars_autolist.csv')
