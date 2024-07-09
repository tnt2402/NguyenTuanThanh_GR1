import streamlit as st
import os
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
code_dir = pathlib.Path(__file__).parent.resolve()
pd.set_option("styler.render.max_elements", 1140542)
files_location = code_dir /  "../data/merged.csv"

# Đường dẫn tuyệt đối đến thư mục data
# data_dir = Path() 

st.title("Visualization")

data= pd.read_csv(files_location)
st.markdown("##### Có tổng cổng "+str(len(data))+ " bản ghi ô tô crawl được")
# st()
st.dataframe(data)



# Tính tỷ lệ phần trăm cho các hãng
make_name = data['make_name'].value_counts()
total_counts = len(data)
make_name_percentages = make_name / total_counts * 100

# Gộp các hãng dưới 1% vào nhóm 'Khác'
threshold = 1.0
make_names_to_group = make_name_percentages[make_name_percentages < threshold].index
data['make_name'] = data['make_name'].apply(lambda x: 'Other' if x in make_names_to_group else x)

# Tính lại số lượng cho nhóm 'Khác'
new_make_name_counts = data['make_name'].value_counts()

# # Vẽ biểu đồ mới
# fig=plt.figure(figsize=(15, 8))
# new_make_name_counts.plot(kind='pie', autopct='%1.1f%%', ylabel='')
# plt.title('Biểu đồ thể hiện số lượng xe theo hãng')
# plt.show()



fig, ax = plt.subplots(figsize=(15, 8))
round((data.isnull().sum() / (len(data)) * 100) , 2).sort_values().plot(kind = 'barh',color ='maroon')
ax.set_title('Biểu đồ missingvalue')
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(15, 8))
new_make_name_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, ylabel='')
ax.set_title('Biểu đồ thể hiện số lượng xe theo hãng')
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(25, 16))
sns.barplot(x='make_name', y='price', data=data, ax=ax)
ax.set_title('Biểu đồ thể hiện mức giá trung bình của các hãng xe')
st.pyplot(fig)


fig, ax = plt.subplots(figsize=(25, 16))
ax=sns.scatterplot(x='year',y='price',data=data,hue=data['make_name'])
ax.set_title('Biểu đồ thể hiện mức giá của các hãng xe theo năm sản xuất')
ax.set_xticklabels(ax.get_xticklabels(),rotation=40,ha='right')
st.pyplot(fig)

# fig, ax = plt.subplots(figsize=(25, 16))
# sns.barplot(x='make_name', y='price', data=data, ax=ax)
# ax.set_title('Biểu đồ thể hiện mức giá trung bình của các hãng xe')


categorical = ['name','make_name','drivetrain','model_name','normalized_color_exterior','transmission','normalized_color_interior','fuel_type','body_style','trim',]
numerical =[ 'price', 'door_count', 'mileage', 'year']
print(numerical)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
for i, ax in zip(numerical, axes.flatten()):
    sns.distplot(data[i], ax=ax, color='purple')
    ax.set_title("Distribution of %s" %i, fontsize=12)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis='x', labelsize=8)

st.pyplot(fig)

# fig, ax = plt.subplots(figsize=(25, 16))
# sns.heatmap(data[numerical].corr(), annot=True, cmap='Reds',ax=ax, linewidths=0.1)

# st.pyplot(fig)






# # Tạo một figure mới với kích thước phù hợp
# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

# # Lặp qua từng cột số và vẽ biểu đồ phân phối
# for i, ax in zip(numerical, axes.flatten()):
#     sns.distplot(data[i], ax=ax, color='purple')
#     ax.set_title("Distribution of %s" %i, fontsize=12)
#     ax.set_xlabel("")
#     ax.set_ylabel("")
#     ax.tick_params(axis='x', labelsize=8)

# # Điều chỉnh khoảng cách giữa các biểu đồ
# plt.subplots_adjust(wspace=0.3, hspace=0.5)

# st.pyplot(fig)