import pandas as pd
import numpy as np

class QuestionnaireAnalysis:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:
        """Calculates the average score of a subject and adds a new "score" column with it.

        If the subject has more than "maximal_nans_per_sub" NaN in his grades, the
        score should be NA. Otherwise, the score is simply the mean of the other grades.
        The datatype of score is UInt8, and the floating point raw numbers should be
        rounded down.

        Parameters
        ----------
        maximal_nans_per_sub : int, optional
            Number of allowed NaNs per subject before giving a NA score.

        Returns
        -------
        pd.DataFrame
            A new DF with a new column - "score".
        """
        # Columns that represent the questions
        question_columns = ['q1', 'q2', 'q3', 'q4', 'q5']

        # Calculate the number of NaNs in each row for the question columns
        nan_counts = self.data[question_columns].isna().sum(axis=1)

        # Calculate the average score, rounded down
        self.data['score'] = self.data[question_columns].mean(axis=1).apply(np.floor).astype('UInt8')

        # Set the score to NA where the number of NaNs exceeds the allowed maximum
        self.data.loc[nan_counts > maximal_nans_per_sub, 'score'] = pd.NA

        return self.data

# Main script
if __name__ == "__main__":
    # Load the test data from the CSV file
    df_test = pd.read_csv('q4_score.csv')

    # Create an instance of the QuestionnaireAnalysis with the test data
    analysis = QuestionnaireAnalysis(df_test)

    # Apply the score_subjects method
    scored_df = analysis.score_subjects()

    # Display the DataFrame with the new "score" column
    print("DataFrame with Scores:")
    print(scored_df)
