import pandas as pd
import numpy as np

class DataAnalysis:
    def __init__(self, populations_file, fillna_file):
        self.populations_file = populations_file
        self.fillna_file = fillna_file
        self.populations_df = None
        self.fillna_df = None

    def read_fillna_data(self):
        # Read the data from the fillna CSV file
        self.fillna_df = pd.read_csv(self.fillna_file)

    def fill_na_with_mean(self):
        if self.fillna_df is None:
            raise ValueError("Fillna data not loaded. Please call read_fillna_data() first.")
        
        # Apply fillna only to numeric columns
        numeric_cols = self.fillna_df.select_dtypes(include=[np.number]).columns
        self.fillna_df[numeric_cols] = self.fillna_df[numeric_cols].fillna(self.fillna_df[numeric_cols].mean())
        
        # Save the updated DataFrame to a new CSV file
        self.fillna_df.to_csv('q3_fillna_filled.csv', index=False)
        return self.fillna_df

    def read_populations_data(self):
        # Read the data from the populations file
        self.populations_df = pd.read_csv(self.populations_file)

    def largest_species(self):
        if self.populations_df is None:
            raise ValueError("Populations data not loaded. Please call read_populations_data() first.")
        
        self.populations_df['largest'] = self.populations_df[['hare', 'lynx', 'fox']].idxmax(axis=1)
        largest_df = self.populations_df[['year', 'largest']]
        largest_df.to_csv('q3_largest.csv', index=False)
        return largest_df

    def lynxes_when_hares(self):
        if self.populations_df is None:
            raise ValueError("Populations data not loaded. Please call read_populations_data() first.")
        
        condition = self.populations_df['hare'] > self.populations_df['fox']
        result_df = self.populations_df[condition][['year', 'lynx']]
        result_df.to_csv('q3_lynx.csv', index=False)
        return result_df

    def normalized_mean_number_of_animals(self):
        if self.populations_df is None:
            raise ValueError("Populations data not loaded. Please call read_populations_data() first.")
        
        self.populations_df['mean'] = self.populations_df[['hare', 'lynx', 'fox']].mean(axis=1)
        self.populations_df['mean_norm'] = (self.populations_df['mean'] - self.populations_df['mean'].min()) / (self.populations_df['mean'].max() - self.populations_df['mean'].min())
        self.populations_df.to_csv('q3_mean.csv', index=False)
        return self.populations_df

def main():
    # File paths
    populations_file = 'C:/Users/shell/homweork/homework-5-Shellygur4/hw5-2024/tests_data/populations.txt'
    fillna_file = 'C:/Users/shell/homweork/homework-5-Shellygur4/hw5-2024/tests_data/q3_fillna.csv'
    
    # Create an instance of the DataAnalysis class
    analysis = DataAnalysis(populations_file, fillna_file)
    
    # Fill NA with mean
    print("Filling NA with mean...")
    analysis.read_fillna_data()
    filled_df = analysis.fill_na_with_mean()
    print(filled_df.head())
    
    # Largest species
    print("\nFinding largest species...")
    analysis.read_populations_data()
    largest_df = analysis.largest_species()
    print(largest_df.head())
    
    # Lynxes when hares outgrew foxes
    print("\nFinding lynxes when hares outgrew foxes...")
    lynxes_df = analysis.lynxes_when_hares()
    print(lynxes_df.head())
    
    # Normalized mean number of animals
    print("\nAdding normalized mean number of animals...")
    mean_df = analysis.normalized_mean_number_of_animals()
    print(mean_df.head())

if __name__ == "__main__":
    main()
