# datasense.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Loading the data you want to clean (Creating a function)
def load_data(filepath):
    if not os.path.exists(filepath):
        print("File does not exist.")
        return None
    try:
        df = pd.read_csv(filepath)
        print("File found and loaded succesfully!\n")
        return df
    except Exception as e:
        print("Error reading this file:", e)
        return None

# Show basic info
def show_basic_info(df):
    print("Data Info")
    print("-" * 30) #For clarity and readability
    print("Shape:", df.shape)
    print("\nColumns:\n", df.columns.tolist()) 
    print("\nData Types:\n", df.dtypes)
    print("\nMissing Values:\n", df.isnull().sum())
    print("\nDuplicate Rows:", df.duplicated().sum())

#Decribe function for showing stats of the file 
def describe_data(df):
    print("--- Descriptive Stats ----")
    print(df.describe(include='all').T)
    print("-----------------\n")

# Cleaning Data (Duplicates & Missing Values)
def clean_data(df):
    print("\n--Cleaning Data--")

    # Check and remove duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Dropped {duplicates} duplicate rows.")
    else:
        print("No duplicate rows found.")

    # Check and handle missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"Found {missing} missing values.")
        choice = input("Do you want to (d)rop or (f)ill missing values? (d/f/skip): ")

        if choice == 'd':
            df = df.dropna()
            print("Dropped rows with missing values.")
        elif choice == 'f':
            df = df.fillna(method='ffill')  # It means Forward fill
            print("Filled missing values (forward fill).")
        else:
            print("Skipped handling missing values.")
    else:
        print("No missing values found.")

    print("New shape of data:", df.shape)
    print("------------\n")
    return df

# Show Charts
def visualize_data(df):
    print("\n-- Creating Charts --")

    # Columns
    numeric = df.select_dtypes(include=['int64', 'float64']).columns
    categorical = df.select_dtypes(include=['object']).columns

    # Make outputs folder if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # Histograms
    for col in numeric:
        sns.histplot(df[col], kde=True)
        plt.title(f"Histogram - {col}")
        plt.savefig(f"outputs/hist_{col}.png")
        plt.clf()

    # Countplots
    for col in categorical:
        if df[col].nunique() < 15:
            sns.countplot(x=df[col])
            plt.title(f"Count Plot - {col}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"outputs/count_{col}.png")
            plt.clf()

    # Box plots for checking the outliers in it 
    for col in numeric:
        sns.boxplot(x=df[col])
        plt.title(f"Boxplot - {col}")
        plt.savefig(f"outputs/box_{col}.png")
        plt.clf()

    # Correlation heatmap
    if len(numeric) > 1:
        plt.figure(figsize=(8, 6))
        sns.heatmap(df[numeric].corr(), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig("outputs/heatmap_correlation.png")
        plt.clf()

    print("All charts saved in 'outputs' folder.")


# Main (File handling)
if __name__ == "__main__":
    filepath = input("Enter path of CSV file: ").strip()
    df = load_data(filepath)
    if df is not None:
        show_basic_info(df)
        describe_data(df)
        df = clean_data(df)
        visualize_data(df)

        save = input("Do you want to save the cleaned file? (y/n): ").lower()
        if save == 'y':
            df.to_csv("outputs/cleaned_data.csv", index=False)
            print("Cleaned file saved as 'outputs/cleaned_data.csv'")


