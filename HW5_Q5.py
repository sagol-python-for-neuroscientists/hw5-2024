import pandas as pd
import numpy as np
import pandas as pd
import os

# Print the current working directory to understand where the script is being executed
print("Current Working Directory:", os.getcwd())

# List all files in the current directory to verify that the script is looking in the right place
print("Files in Current Directory:", os.listdir())

# Load the CSV file using the correct path. The path must be verified to ensure the file is present.
# Here, we're using an absolute path to avoid issues with relative paths and to ensure the file is found.
df_test = pd.read_csv(r'C:/Users/saeed/Desktop/hw5-2024/tests_data/q5_corr.csv')  # The path in my computer..This could be changed acoording to the specific path in different computers

class QuestionnaireAnalysis:
    def __init__(self, data: pd.DataFrame):
        self.data = data
 
    def correlate_gender_age(self) -> pd.DataFrame:
        """Looks for a correlation between the gender of the subject, their age
        and the score for all five questions.

        Returns
        -------
        pd.DataFrame
            A DataFrame with a MultiIndex containing the gender and whether the subject is above
            40 years of age, and the average score in each of the five questions.
        """
        # Step 1: Create a new column 'Age_above_40' to indicate if age > 40
        self.data['Age_above_40'] = self.data['age'] > 40

        # Step 2: Set MultiIndex with ordinal index, gender, and age
        self.data.set_index([self.data.index, 'gender', 'age'], inplace=True)

        # Step 3: Group by gender and whether age is above 40
        grouped = self.data.groupby(['gender', 'Age_above_40'])

        # Step 4: Calculate the mean for each group across the questions
        result = grouped[['q1', 'q2', 'q3', 'q4', 'q5']].mean()

        # Stwp 5: Return the resulting DataFrame
        return result
    
# Main Script execution
if __name__ == "__main__":

    # Create an instance of the QuestionnaireAnalysis with the test data
    analysis = QuestionnaireAnalysis(df_test)

    # Apply the correlate_gender_age method
    result_df = analysis.correlate_gender_age()

    # Display the resulting DataFrame (print the resulting DataFrame to display the correlation results)
    print("Correlation between gender, age, and grades:")
    print(result_df)

         


                                    










