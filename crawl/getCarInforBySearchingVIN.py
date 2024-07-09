import csv
from tqdm import tqdm
from vpic import TypedClient
from joblib import Parallel, delayed

c = TypedClient()


def write_to_csv(data, filename):
    keys = data[0].keys() if data else []
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


# Open the CSV file
with open('../data/merged.csv', 'r') as file:
    reader = csv.DictReader(file)

    # Create a list to store the vin attributes
    vin_list = []

    # Iterate over each row in the CSV file
    for row in reader:
        # Check if the row has a "vin" attribute
        if 'vin' in row:
            # Append the vin attribute to the list
            tmp_vin = {
                'vin': row['vin'],
                'name': row['name'],
                'model_id': row['model_id'],
                'make_name': row['make_name'],
                'model_name': row['model_name'],
                'body_style': row['body_style'],
                'price': row['price'],
                'year': row['year'],
                'normalized_color_exterior': row['normalized_color_exterior'],
                'normalized_color_interior': row['normalized_color_interior'],
                'transmission': row['transmission'],
                'trim': row['trim'],
                'engine_cylinders': row['engine_cylinders']
            }
            vin_list.append(tmp_vin)


data = {}
for each_vin in tqdm(vin_list):
    result = c.decode_vin(each_vin['vin'])
    # print(result)
    tmp_car = each_vin
    tmp_car['displacement_l'] = result.displacement_l
    tmp_car['drive_type'] = result.drive_type
    tmp_car['engine_model'] = result.engine_model
    tmp_car['fuel_type_primary'] = result.fuel_type_primary
    tmp_car['doors'] = result.doors
    # tmp_car['transmission_style'] = result.transmission_style
    # tmp_car['transmission_speeds'] = result.transmission_speeds
    # print(tmp_car)
    # print(result)
    # break

write_to_csv(data, "merged_data_with_vin_data.csv")

