# Milestone1: Data Cleaning and Preprocessing
# Importing necessary libraries for data analysis and visualization
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Reading the Netflix dataset
df = pd.read_csv("netflix_titles.csv")

# Displaying the first few rows of the dataset
df.head()

# Checking the number of rows and columns in the dataset
df.shape

# Getting a summary of the dataset
df.info()

# Checking for missing values in each column
df.isnull().sum()

# Creating a table to show missing values per column
missing_df = df.isnull().sum().reset_index()
missing_df.columns = ['column', 'missing_count']

# Visualizing missing values using a bar plot
plt.figure(figsize=(10,5))
sns.barplot(data=missing_df, x='column', y='missing_count')
plt.xticks(rotation=90)
plt.title("Missing Values Per Column")
plt.show()

# Filling missing values with appropriate replacements
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('No Data')
df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
df['duration'] = df['duration'].fillna(df['duration'].mode()[0])

# Converting 'date_added' to a proper date format
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Removing rows where 'date_added' is missing
df = df.dropna(subset=['date_added'])

# Adding new columns for the year and month when added
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# Checking for duplicate rows in the dataset
df[df.duplicated()]

# Checking for missing values again after cleaning
df.isnull().sum()

# Saving the cleaned dataset to a new CSV file
df.to_csv("cleaned_netflix_data.csv", index=False)

# Reading the cleaned dataset for further analysis
data = pd.read_csv("cleaned_netflix_data.csv")




# -------------------------------------------------------------------------------------------------------------------------------#


# Milestone2: Exploratory Data Analysis (EDA)

# Plotting the count of Movies vs TV Shows
sns.countplot(data=data , x = 'type')
plt.title("Movies vs TV Shows in Netflix")
plt.figure(figsize = (12,6))
plt.show()

# Removing invalid ratings (like durations)
data = data[~data['rating'].str.contains('min', na = False)]

# Plotting the distribution of ratings
data['rating'].value_counts().plot(kind='bar')
plt.title("Distribution of Ratings")
plt.xlabel("Rating")
plt.show()

# Adding a new column for decades
data['decade'] = (data['release_year'] // 10) * 10

# Plotting the number of shows added per decade
data['decade'].value_counts().sort_index().plot(kind='line')
plt.title("Shows Added in Netflix Per Decade")
plt.xlabel("Decade")
plt.show()

# Plotting the top 10 countries producing the most shows
data['country'].value_counts().head(10).plot(kind = 'bar')
plt.title("Top 10 Countries Producing More Shows")
plt.show()

# Plotting the top 10 countries excluding 'No Data'
data[data['country'] != 'No Data']['country'].value_counts().head(10).plot(kind = 'bar')
plt.title("Top 10 Countries Without 'No Data'")

# Plotting Movies vs TV Shows per decade
year_type = data.groupby(['decade', 'type']).size().unstack()
year_type.plot(figsize=(12,6))
plt.title("Movies vs TV Shows in a Decade")
plt.ylabel("Count")
plt.xlabel("Release Decade")
plt.show()

# Plotting the type of content for each rating
sns.countplot(data=data, x='rating', hue = 'type')
plt.title("Type of Content Got Rated")
plt.xticks(rotation = 90)
plt.show()

# Analyzing genres in the dataset
data_analyse = data.copy()
data_analyse['genre'] = data_analyse['listed_in'].str.split(',')
data_analyse = data_analyse.explode('genre')
data_analyse['genre'] = data_analyse['genre'].str.strip()

# Removing rows with null values in 'genre' or 'type'
data_analyse = data_analyse.dropna(subset=['genre', 'type'])

# Dropping duplicate rows to avoid reindexing issues
data_analyse = data_analyse.drop_duplicates(subset=['genre', 'type'])

# Creating a heatmap for top genres vs type of content
genre_type = pd.crosstab(data_analyse['genre'], data_analyse['type'])
top_genre = data_analyse['genre'].value_counts().head(20).index
sns.heatmap(genre_type.loc[top_genre], annot=True, fmt='d', cmap='YlGnBu')
plt.title("Genre vs Type")
plt.show()

# Plotting trends of top 5 genres over decades
data_analyse['decade'] = (data_analyse['release_year'] // 10) * 10
genre_year = pd.crosstab(data_analyse['decade'], data_analyse['genre'])
top_5 = data_analyse['genre'].value_counts().head(5).index
genre_year[top_5].plot(figsize=(12,6))
plt.title("Trends of Top 5 Genres from All Decades")
plt.xlabel('Decade')
plt.xticks(rotation = 0)
plt.ylabel('Count')
plt.show()

# Analyzing content type in the USA
sns.countplot(data=data[data['country'] == 'United States'], x='type')
plt.title("Type of Content in USA")
plt.xticks(rotation = 0)
plt.show()

# Analyzing top genres in the USA
usa = data[data['country'] == 'United States']
usa_genre = usa['listed_in'].str.split(',').explode().str.strip()
usa_Gcount = usa_genre.value_counts()
usa_Gcount.head(10).plot(kind='bar')
plt.title("Top 10 Genres in USA")
plt.show()

# Analyzing content type in India
sns.countplot(data=data[data['country'] == 'India'], x='type')
plt.title("Type of Content in India")
plt.xticks(rotation = 0)
plt.show()

# Analyzing top genres in India
india = data[data['country'] == 'India']
india_genre = india['listed_in'].str.split(',').explode().str.strip()
india_Gcount = india_genre.value_counts().head(10)
india_Gcount.plot(kind='bar')
plt.title("Top 10 Genres in India")
plt.show()

# Analyzing content with no country data
sns.countplot(data=data[data['country'] == 'No Data'], x='type')
plt.title("Rating Distribution for Shows with No Country Data")
plt.xticks(rotation = 90)
plt.show()