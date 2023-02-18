import pandas as pd
import os
import requests
import re
import matplotlib.pyplot as plt
import numpy as np


def load_data() -> pd.DataFrame:
    """
    Load data from Nobel_laureates.json file.
    :return: DataFrame with data.
    """
    if not os.path.exists('./Data'):
        os.mkdir('./Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('./Data'):
        print('Nobel_laureates.json')
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        with open('./Data/Nobel_laureates.json', 'wb') as f:
            f.write(r.content)
        print('Loaded.')
    return pd.read_json('./Data/Nobel_laureates.json')


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare data (remove duplicates, drop NaN values, etc.) and return DataFrame with prepared data.
    :param df: DataFrame with data.
    :return: DataFrame with prepared data.
    """
    # print(df.duplicated().any())
    df.dropna(subset=['gender'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    # print(df.filter(items=['country', 'name']).head(20).to_dict())

    for i in range(0, df.shape[0]):
        if df.iloc[i, 0] == '':
            if re.findall(',', str(df.iloc[i, 8])):
                df.iloc[i, 0] = (df.iloc[i, 8]).split(',')[-1].strip()
            else:
                df.iloc[i, 0] = None

    df.dropna(subset=['born_in'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df.replace({'born_in': {'US': 'USA', 'United States': 'USA', 'U.S.': 'USA', 'United Kingdom': 'UK'}})


def count_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the age of obtaining the Nobel Prize for each Nobel laureate by using the information from various columns.
    :param df: DataFrame with data.
    :return: DataFrame with data and new column 'age_of_winning'.
    """
    df['year_born'] = df.date_of_birth

    for i in range(0, df.shape[0]):
        if re.findall(',', str(df.iloc[i, -1])):
            df.iloc[i, -1] = int(df.iloc[i, -1].split(',')[-1].strip())
        elif re.findall('-', str(df.iloc[i, -1])):
            df.iloc[i, -1] = int(df.iloc[i, -1].split('-')[0])
        else:
            df.iloc[i, -1] = int(df.iloc[i, -1].split(' ')[-1])

    df['age_of_winning'] = df.year - df.year_born
    return df


def plot_pie_chart(df: pd.DataFrame):
    """
    Plot a pie chart representing the fraction of the Nobel laureates by country.
    :param df: DataFrame with data.
    :return: None
    """
    nob_counts = df['born_in'].value_counts()
    print(df.columns.tolist())
    nob_counts = nob_counts.loc[nob_counts.values >= 25].to_dict()
    print(nob_counts)

    for i in range(0, df.shape[0]):
        if df.iloc[i, 0] not in nob_counts:
            df.iloc[i, 0] = 'Other countries'

    new_counts = df['born_in'].value_counts().to_dict()
    labels = list(new_counts.keys())
    data = list(new_counts.values())
    plt.figure(figsize=(12, 12))
    colors = ['blue', 'orange', 'red', 'yellow',
              'green', 'pink', 'brown', 'cyan', 'purple']
    explode = [0.0, 0.0, 0.0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    plt.pie(data, labels=labels, colors=colors, explode=explode,
            autopct=lambda p: f'{p:.2f}%\n({p * sum(data) / 100 :.0f})')
    plt.show()


def plot_bar(df: pd.DataFrame):
    """
    Plot a grouped bar chart representing the number of male and female Nobel laureates in each category.
    :param df: DataFrame with data.
    :return: None
    """
    df = df[df.category != '']
    male_count = df[df.gender == 'male'].groupby(
        ['category']).count()['born_in']
    category = male_count.index
    male = male_count.tolist()
    female = df[df.gender == 'female'].groupby(
        ['category']).count()['born_in'].tolist()

    x_axis = np.arange(len(category))
    plt.figure(figsize=(10, 10))
    plt.bar(x_axis - 0.2, male, width=0.4, label='Males')
    plt.bar(x_axis + 0.2, female, width=0.4, label='Females')
    plt.xticks(x_axis, category)
    plt.xlabel('Category', fontsize=14)
    plt.ylabel('Nobel Laureates Count', fontsize=14)
    plt.title(
        'The total count of male and female Nobel Prize winners in each category', fontsize=20)
    plt.legend()
    plt.show()


def box_plot(df: pd.DataFrame):
    """
    Generate a box plot for ages of getting the Nobel Prize for each category.
    :param df: DataFrame with data.
    :return: None
    """
    df = df[df['category'] != '']
    categories = {}
    all_categories = []

    for cat in df['category'].unique():
        values = df[df['category'] == cat]['age_of_winning'].tolist()
        categories[cat] = values
        all_categories.extend(values)
    categories['All categories'] = all_categories

    plt.figure(figsize=(10, 10))
    plt.boxplot(categories.values(), labels=categories.keys(), showmeans=True)
    plt.title(
        'The total count of male and female Nobel Prize winners in each category', fontsize=20)
    plt.ylabel('Age of obtaining the Nobel Price', fontsize=14)
    plt.xlabel('Category', fontsize=14)
    plt.show()


def main():
    df = load_data()
    df = prepare_data(df)
    df = count_age(df)
    # plot_pie_chart(df)
    # plot_bar(df)
    box_plot(df)


if __name__ == '__main__':
    main()
