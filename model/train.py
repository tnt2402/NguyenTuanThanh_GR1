import datetime
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from lightgbm import LGBMRegressor
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import (
    mean_absolute_error,
    accuracy_score,
    mean_squared_error,
    r2_score,
)


import warnings

warnings.filterwarnings("ignore")
# Đọc file
import pathlib
import re
import string
code_dir = pathlib.Path(__file__).parent.resolve()


def preprocess_data(df):
    # Chuyển hết giá trị về ký tự chữ cái thường
    df = df.applymap(lambda s: s.lower() if type(s) == str else s)
    # Xóa tất cả dấu space thừa trong col drivetrain
    df["drivetrain"] = df["drivetrain"].str.replace(r"[^a-zA-Z0-9]", "", regex=True)
    df["drivetrain"] = df["drivetrain"].replace("", np.nan)
    # loại bỏ các giá trị có giá bằng 0
    df = df[df["price"] > 0]
    # Thay các giá trị có cửa bằng 0 thành giá trị phổ biến nhất là 4
    df["door_count"] = df["door_count"].replace(0, 4, inplace=True)
    df["drivetrain"] = df["drivetrain"].replace("unknown", "awd", inplace=True)
  


def df_dopcol(df, columns_to_drop=[]):
    df.drop(columns_to_drop, axis=1, inplace=True)


def df_dropna(df, columns_to_check=[]):
    df = df.dropna(subset=columns_to_check, inplace=True)


def save_data(df, file_name):
    # Ghi DataFrame đã gộp ra file CSV với tên file có chứa thông tin ngày giờ
    df.to_csv(file_name, index=False)

    print(f"Dữ liệu đã được gộp và ghi ra file '{file_name}'")


def convert_to_category_codes(df):
    columns_to_convert = [
        "name",
        "make_name",
        "drivetrain",
        "model_name",
        "normalized_color_exterior",
        "transmission",
        "normalized_color_interior",
        "fuel_type",
        "body_style",
        "trim",
    ]
    le = LabelEncoder()
    listDict={}
    for col in columns_to_convert:
        df[col]=le.fit_transform(df[[col]])
        le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
        listDict[col]=le_name_mapping
    with open(code_dir/"mapping.txt", "w", encoding="utf-8") as f:
        f.write(str(listDict))

def training():
    filename_carsAutolist = code_dir/"../data/cars_autolist.csv"
    filename_demo = code_dir/"../data/cars_thecarconnection.csv"

    demo_df = pd.read_csv(filename_demo)
    # Đổi tên col doors thành door_count
    demo_df.rename(columns={"doors": "door_count"}, inplace=True)

    cars_autolist_df = pd.read_csv(filename_carsAutolist)
    # Đổi tên col driveline -> drivetrain
    cars_autolist_df.rename(columns={"driveline": "drivetrain"}, inplace=True)
    # Bỏ các col dữ liệu không có trong file demo.csv ở file cars_autolist.csv
    col_to_check = [
        "condition",
        "previous_price",
        "engine_cylinders",
        "model_id",
        "quality_score",
        "total_price_change",
        "rear_wheel",
        "heated_seats",
        "leather",
    ]
    df_dopcol(cars_autolist_df, col_to_check)

    # Tiền xử lý dữ liệu ở

    preprocess_data(demo_df)
    preprocess_data(cars_autolist_df)
    # drop NaN value
    columns_to_check = [
        "normalized_color_exterior",
        "normalized_color_interior",
        "door_count",
        "body_style",
        "fuel_type",
        "transmission",
        "trim",
        "drivetrain",
        "year",
    ]
    df_dropna(demo_df, columns_to_check)
    columns_to_check = [
        "mileage",
        "normalized_color_exterior",
        "normalized_color_interior",
        "door_count",
        "body_style",
        "drivetrain",
        "fuel_type",
        "transmission",
        "trim",
        "year",
    ]
    df_dropna(cars_autolist_df, columns_to_check)
    print(cars_autolist_df.shape)
    print(demo_df.shape)
    # Nối dữ liệu
    df = pd.concat([demo_df, cars_autolist_df])
    # Xóa các giá trị trùng
    df = df.drop_duplicates(subset=["vin"], keep="first")
    df = df.map(lambda s: s.lower() if type(s) == str else s)

    # Xóa tất cả dấu space thừa trong col drivetrain
    df["drivetrain"] = df["drivetrain"].str.replace(r"[^a-zA-Z0-9]", "", regex=True)
    df["drivetrain"] = df["drivetrain"].replace("", np.nan)
    # loại bỏ các giá trị có giá bằng 0
    df = df[df["price"] > 0]
    # Thay các giá trị có cửa bằng 0 thành giá trị phổ biến nhất là 4
    df["door_count"] = df["door_count"].replace(0, 4)
    df["drivetrain"] = df["drivetrain"].replace("unknown", "awd")
    # Xoa cac ky tu la
    df["transmission"] = df["transmission"].str.replace(
        r"[^a-zA-Z0-9 ]", " ", regex=True
    )
    df["trim"] = df["trim"].str.replace(r"[^a-zA-Z0-9 ]", " ", regex=True)
    df["normalized_color_exterior"] = df["normalized_color_exterior"].str.replace(
        r"[^a-zA-Z0-9 ]", " ", regex=True
    )
    df["normalized_color_interior"] = df["normalized_color_interior"].str.replace(
        r"[^a-zA-Z0-9 ]", " ", regex=True
    )
    columns_to_check = ["drivetrain"]
    df_dropna(df, columns_to_check)
    print(df.shape)
    # categorical = list(df.dtypes[df.dtypes == "object"].index)

    df = df.drop(["id", "vin"], axis=1)

    # current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = code_dir/"../data/output.csv"
    save_data(df, file_name)
    # Tạo tên file với thông tin ngày giờ
    df = pd.read_csv(file_name)
    print(df.dtypes)
    convert_to_category_codes(df)
    print(df.head(5))

    x = df[
        [
            "name",
            "make_name",
            "model_name",
            "fuel_type",
            "transmission",
            "drivetrain",
            "normalized_color_exterior",
            "normalized_color_interior",
            "door_count",
            "body_style",
            "mileage",
            "trim",
            "year",
        ]
    ].values
    y = df["price"].values
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    print(x_train.shape)
    print(y_train.shape)
    print(x_test.shape)
    print(y_test.shape)

 
    xgb = XGBRegressor(
        random_state=123, learning_rate=0.2, max_depth=5, n_estimators=1500
    )
    xgb.fit(x_train, y_train)
    with open(code_dir/"../model/xgb.pkl", "wb") as file:
        pickle.dump(xgb, file)

    rf = RandomForestRegressor(random_state=123, max_depth=35, n_estimators=600)
    rf.fit(x_train, y_train)
    with open(code_dir/"../model/rf.pkl", "wb") as file:
        pickle.dump(rf, file)

    lgbm = LGBMRegressor(
        random_state=123,
        num_leaves=750,
        learning_rate=0.01,
        max_bin=1200,
        n_estimators=1000,
    )
    lgbm.fit(x_train, y_train)
    with open(code_dir/"../model/lgbm.pkl", "wb") as file:
        pickle.dump(lgbm, file)
   
    xgb_pred = xgb.predict(x_test)
    rf_pred = rf.predict(x_test)
    lgbm_pred = lgbm.predict(x_test)

    y_test = y_test
    # Generalisation
    best_model = pd.DataFrame(
        {
            "model": ["Random forest", "XGBRegressor", "lgbm"],
            "mae": [
                mean_absolute_error(y_test, rf_pred),
                mean_absolute_error(y_test, xgb_pred),
                mean_absolute_error(y_test, lgbm_pred),
            ],
            "mse": [
                mean_squared_error(y_test, rf_pred),
                mean_squared_error(y_test, xgb_pred),
                mean_squared_error(y_test, lgbm_pred),
            ],
            "rmse": [
                np.sqrt(mean_squared_error(y_test, rf_pred)),
                np.sqrt(mean_squared_error(y_test, xgb_pred)),
                np.sqrt(mean_squared_error(y_test, lgbm_pred)),
            ],
            "r2_score": [
                r2_score(y_test, rf_pred),
                r2_score(y_test, xgb_pred),
                r2_score(y_test, lgbm_pred),
            ],
        }
    )
    best_model
    print(best_model)
    