import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('data/KLHK_allyears.csv')

# Filter data for the year 2021
df_2021 = df[df['Tahun'] == 2021]

# Calculate total annual waste generation for each province
total_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].sum().reset_index()

# Calculate average annual waste generation for each province
average_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].mean().reset_index()

# Find the province producing the most and least waste in 2021
most_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmax()]
least_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmin()]

# Categorize provinces based on average annual waste generation
average_annual_waste['Category'] = pd.cut(
    average_annual_waste['Timbulan Sampah Tahunan(ton)'],
    bins=[-float('inf'), 100000, 700000, float('inf')],
    labels=['GREEN', 'ORANGE', 'RED']
)

# Print the results
print("Total Annual Waste Generation in 2021:")
print(total_annual_waste)

print("Average Annual Waste Generation in 2021:")
print(average_annual_waste)

print("Province Producing Most Waste in 2021:")
print(most_waste_province)

print("Province Producing Least Waste in 2021:")
print(least_waste_province)

plt.figure(figsize=(10, 6))
plt.bar(total_annual_waste['Provinsi'], total_annual_waste['Timbulan Sampah Tahunan(ton)'])
plt.xlabel('Province')
plt.ylabel('Total Annual Waste Generation (tons)')
plt.title('Total Annual Waste Generation by Province in 2021')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('static/total_annual_waste.png')
plt.show()


plt.figure(figsize=(10, 6))
plt.bar(average_annual_waste['Provinsi'], average_annual_waste['Timbulan Sampah Tahunan(ton)'])
plt.xlabel('Province')
plt.ylabel('Average Annual Waste Generation (tons)')
plt.title('Average Annual Waste Generation by Province in 2021')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('static/average_annual_waste.png')
plt.show()

print(f"Province Producing Most Waste in 2021: {most_waste_province['Provinsi']} with {most_waste_province['Timbulan Sampah Tahunan(ton)']} tons")

print(f"Province Producing Least Waste in 2021: {least_waste_province['Provinsi']} with {least_waste_province['Timbulan Sampah Tahunan(ton)']} tons")

plt.figure(figsize=(10, 6))
colors = {'GREEN': 'green', 'ORANGE': 'orange', 'RED': 'red'}
plt.bar(average_annual_waste['Provinsi'], average_annual_waste['Timbulan Sampah Tahunan(ton)'], color=average_annual_waste['Category'].map(colors))
plt.xlabel('Province')
plt.ylabel('Average Annual Waste Generation (tons)')
plt.title('Categorization of Average Annual Waste Generation by Province in 2021')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('static/categorized_annual_waste.png')
plt.show()

from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# def load_data():
#     df = pd.read_csv('data/KLHK_allyears.csv')
#     df_2021 = df[df['Tahun'] == 2021]
#     total_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].sum().reset_index()
#     average_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].mean().reset_index()
#     most_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmax()]
#     least_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmin()]
#     average_annual_waste['Category'] = pd.cut(
#         average_annual_waste['Timbulan Sampah Tahunan(ton)'],
#         bins=[-float('inf'), 100000, 700000, float('inf')],
#         labels=['GREEN', 'ORANGE', 'RED']
#     )
#     return total_annual_waste, average_annual_waste, most_waste_province, least_waste_province

# def create_plot(data, xlabel, ylabel, title, filename, color_column=None):
#     plt.figure(figsize=(10, 6))
#     if color_column:
#         colors = {'GREEN': 'green', 'ORANGE': 'orange', 'RED': 'red'}
#         plt.bar(data['Provinsi'], data[ylabel], color=data[color_column].map(colors))
#     else:
#         plt.bar(data['Provinsi'], data[ylabel])
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(f'static/{filename}.png')
#     plt.close()
def load_data():
    df = pd.read_csv('data/KLHK_allyears.csv')
    return df

def create_plots():
    df = load_data()

    # Calculate average annual waste generation for each province
    average_annual_waste_all_years = df.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].mean().reset_index()
    
    # Categorize provinces based on average annual waste generation
    average_annual_waste_all_years['Category'] = pd.cut(
        average_annual_waste_all_years['Timbulan Sampah Tahunan(ton)'],
        bins=[-float('inf'), 100000, 700000, float('inf')],
        labels=['GREEN', 'ORANGE', 'RED']
    )
    
    # Count the number of provinces in each category
    category_counts = average_annual_waste_all_years['Category'].value_counts().sort_index()
    
    # Create the bar plot for category counts
    plt.figure(figsize=(10, 6))
    plt.bar(category_counts.index, category_counts.values, color=['green', 'orange', 'red'])
    plt.xlabel('Category')
    plt.ylabel('Number of Provinces')
    plt.title('Number of Provinces by Average Waste Generation Category (2018-2023)')
    plt.tight_layout()
    plt.savefig('static/category_counts.png')
    plt.close()

    # Line graph for total annual waste generation
    total_annual_waste_all_years = df.groupby(['Tahun', 'Provinsi'])['Timbulan Sampah Tahunan(ton)'].sum().unstack()
    plt.figure(figsize=(14, 8))
    for province in total_annual_waste_all_years.columns:
        plt.plot(total_annual_waste_all_years.index, total_annual_waste_all_years[province], marker='o', label=province)
    plt.xlabel('Year')
    plt.ylabel('Total Annual Waste Generation (tons)')
    plt.title('Total Annual Waste Generation by Province (2018-2023)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('static/total_annual_waste_all_years.png')
    plt.close()

    # Data for 2021
    df_2021 = df[df['Tahun'] == 2021]
    total_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].sum().reset_index()
    average_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].mean().reset_index()

    most_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmax()]
    least_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmin()]

    average_annual_waste['Category'] = pd.cut(
        average_annual_waste['Timbulan Sampah Tahunan(ton)'],
        bins=[-float('inf'), 100000, 700000, float('inf')],
        labels=['GREEN', 'ORANGE', 'RED']
    )

    # Total Annual Waste Generation Plot for 2021
    plt.figure(figsize=(10, 6))
    plt.bar(total_annual_waste['Provinsi'], total_annual_waste['Timbulan Sampah Tahunan(ton)'])
    plt.xlabel('Province')
    plt.ylabel('Total Annual Waste Generation (tons)')
    plt.title('Total Annual Waste Generation by Province in 2021')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('static/total_annual_waste.png')
    plt.close()

    # Average Annual Waste Generation Plot for 2021
    plt.figure(figsize=(10, 6))
    plt.bar(average_annual_waste['Provinsi'], average_annual_waste['Timbulan Sampah Tahunan(ton)'])
    plt.xlabel('Province')
    plt.ylabel('Average Annual Waste Generation (tons)')
    plt.title('Average Annual Waste Generation by Province in 2021')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('static/average_annual_waste.png')
    plt.close()

    # Categorization Plot for 2021
    plt.figure(figsize=(10, 6))
    colors = {'GREEN': 'green', 'ORANGE': 'orange', 'RED': 'red'}
    plt.bar(average_annual_waste['Provinsi'], average_annual_waste['Timbulan Sampah Tahunan(ton)'], color=average_annual_waste['Category'].map(colors))
    plt.xlabel('Province')
    plt.ylabel('Average Annual Waste Generation (tons)')
    plt.title('Categorization of Average Annual Waste Generation by Province in 2021')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('static/categorized_annual_waste.png')
    plt.close()



# @app.route('/')
# def index():
#     total_annual_waste, average_annual_waste, most_waste_province, least_waste_province = load_data()
#     create_plot(total_annual_waste, 'Province', 'Timbulan Sampah Tahunan(ton)', 'Total Annual Waste Generation by Province in 2021', 'total_annual_waste')
#     create_plot(average_annual_waste, 'Province', 'Timbulan Sampah Tahunan(ton)', 'Average Annual Waste Generation by Province in 2021', 'average_annual_waste')
#     create_plot(average_annual_waste, 'Province', 'Timbulan Sampah Tahunan(ton)', 'Categorization of Average Annual Waste Generation by Province in 2021', 'categorized_annual_waste', 'Category')
#     return render_template('index.html', 
#                            most_waste_province=most_waste_province, 
#                            least_waste_province=least_waste_province)

@app.route('/')
def index():
    create_plots()
    df = load_data()
    df_2021 = df[df['Tahun'] == 2021]
    total_annual_waste = df_2021.groupby('Provinsi')['Timbulan Sampah Tahunan(ton)'].sum().reset_index()
    most_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmax()]
    least_waste_province = total_annual_waste.loc[total_annual_waste['Timbulan Sampah Tahunan(ton)'].idxmin()]
    return render_template('index.html', 
                           most_waste_province=most_waste_province, 
                           least_waste_province=least_waste_province)



if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return "Hello, World!"

# if __name__ == '__main__':
#     app.run(debug=True)