import pandas as pd
import numpy as np
from typing import Tuple

class QuestionnaireAnalysis:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        """Finds, in the original DataFrame, the subjects that didn't answer
        all questions, and replaces that missing value with the mean of the
        other grades for that student.

        Returns
        -------
        df : pd.DataFrame
          The corrected DataFrame after insertion of the mean grade
        arr : np.ndarray
          Row indices of the students that their new grades were generated
        """
        # Ensure data is a DataFrame
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("The data must be a pandas DataFrame.")

        # Columns that represent the questions
        question_columns = ['q1', 'q2', 'q3', 'q4', 'q5']

        # Create a copy of the DataFrame to avoid modifying the original data
        df = self.data.copy()

        # Initialize a list to keep track of indices where changes are made
        modified_indices = []

        # Iterate through each row to find missing values
        for index, row in df.iterrows():
            if row[question_columns].isnull().any():
                # Calculate the mean of the available (non-missing) values
                mean_value = row[question_columns].mean()
                # Replace NaN values with the calculated mean
                df.loc[index, question_columns] = row[question_columns].fillna(mean_value)
                # Record the index of the modified row
                modified_indices.append(index)

        # Convert the list of modified indices to a numpy array
        modified_indices = np.array(modified_indices)

        return df, modified_indices

# Main script
if __name__ == "__main__":
    # Load the data from the CSV file
    df_test = pd.read_csv('q3_fillna.csv')

    # Load the expected result (indices) from the .npy file
    expected_indices = np.load('q3_fillna.npy')

    # Create an instance of the QuestionnaireAnalysis with the test data
    analysis = QuestionnaireAnalysis(df_test)

    # Apply the fill_na_with_mean method
    corrected_df, modified_indices = analysis.fill_na_with_mean()

    # Display the corrected DataFrame and compare the indices
    print("Corrected DataFrame:")
    print(corrected_df)
    print("\nModified Indices:", modified_indices)
    print("\nDo the modified indices match the expected ones?", np.array_equal(modified_indices, expected_indices))
