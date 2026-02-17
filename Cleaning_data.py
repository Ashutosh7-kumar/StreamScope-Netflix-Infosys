import numpy as np
import pandas as pd

# Load the dataset from the CSV file
df = pd.read_csv('netflix_titles.csv')

# Display the column names before capitalization
print("Before Capitalize header:")
print(df.columns)

# Capitalize the first letter of each column name
print("After Capitalize header:")
new_column_names = []
for i in df.columns:
    new_column_names.append(i.capitalize())
df.columns = new_column_names
print(df.columns)

# Check if the dataset has duplicated values
print("Number of duplicated values in the dataset:")
print(df.duplicated().sum())

# Drop duplicated rows if any exist
df.drop_duplicates(inplace=True)

# Check if the dataset has null values
print("Number of null values in the dataset:")
print(df.isna().sum())

# Drop rows with null values
# Note: This approach removes all rows with any missing data
print("Drop the null values")
df.dropna(inplace=True)
print(df.isna().sum())

# Display unique values in the 'Show_id' column
print(df["Show_id"].unique())

# Print column names to verify the dataset structure
print("Column names in the dataset:")
print(df.columns)

# Check if 'date_added' column exists before accessing it
if 'Date_added' in df.columns:
    # Check the data type of the 'date_added' column
    print(df['Date_added'].dtype)

    # Clean and convert the 'date_added' column to datetime format
    # Strip any leading/trailing whitespace and convert to datetime
    df['Date_added'] = df['Date_added'].str.strip()
    df['Date_added'] = pd.to_datetime(df['Date_added'])
    print(df['Date_added'].dtype)

    # Extract the year and month from the 'date_added' column
    df['Year_added'] = df['Date_added'].dt.year
    df['Month_added'] = df['Date_added'].dt.month
else:
    print("The column 'Date_added' does not exist in the dataset.")

# Strip any leading/trailing whitespace
df['Country'] = df['Country'].str.split(',').str[0]
df['Country'] = df['Country'].str.strip()

# Extract the primary genre from the 'listed_in' column
# Strip any leading/trailing whitespace
df['Primary_genre'] = df['Listed_in'].str.split(',').str[0]
df['Primary_genre'] = df['Primary_genre'].str.strip()

# Clean the 'rating' column by stripping any leading/trailing whitespace
df['Rating'] = df['Rating'].str.strip()

# Display the dataframe information to verify changes
print(df.info())


df['Listed_in'] = df['Listed_in'].str.lower().str.strip()
df['Genre_list'] = df['Listed_in'].str.split(', ')
df[['Listed_in', 'Genre_list']].head()

#new table or data set after cleaning
print("Cleaned dataset:")
df.to_csv("new.csv", index=False)