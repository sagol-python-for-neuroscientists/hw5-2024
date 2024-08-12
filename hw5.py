import pathlib
from typing import Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class QuestionnaireAnalysis:

    def __init__(self, data_fname: Union[pathlib.Path, str]):
        try:
            self.data_fname = pathlib.Path(data_fname).resolve()
        except TypeError:
            raise TypeError("ERROR: not a string or a pathlib.Path instance.")
        
        if not self.data_fname.exists():
            raise ValueError(f"File {str(self.data_fname)} does not exist.")

    def read_data(self):
        
        self.data = pd.read_json(self.data_fname)

    """1. Plot the distribution of ages of the participants. 
    The bins for the histogram should be [0, 10), [10, 20), [20, 30), ..., [90, 100]. 
    The function should return the result."""
    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        
        age_bins = np.linspace(0, 100, 11)
        fig, ax = plt.subplots()
        age_hist, bin_edges, _ = ax.hist(self.data["age"], bins=age_bins)


        ax.set_xlabel("Age")
        ax.set_ylabel("Counts")
        ax.set_title("Age distribution across all subjects")
        return age_hist, bin_edges


    """ 2. Participants without a valid email are useless since we can't contact them. 
    Remove all of the rows with an invalid address and return the new DataFrame. """
    def remove_rows_without_mail(self) -> pd.DataFrame:
        valid_emails = self.data["email"].apply(
        lambda email: (
            ("@" in email) and 
            ("." in email) and 
            (not email.endswith(".")) and 
            (not email.endswith("@")) and 
            (not email.startswith(".")) and 
            (not email.startswith("@")) and 
            email.isascii() and 
            (email.count("@") == 1) and 
            (email[email.find("@") + 1] != ".")
          )
        )
        return self.data.loc[valid_emails].reset_index(drop=True)

    """3. Some participants haven't answered all of the question. 
    It was decided that the grade for those missing questions will be the average grade of the other question for that subject. 
    Write a method that works on the original DataFrame (in self.data), 
    replaces the missing values with the mean for that subject in the other questions 
    and returns the corrected DataFrame as well as a np.array of the indices of the rows that were corrected."""
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        grades_only = self.data.loc[:, "q1":"q5"]
        rows_with_nulls = grades_only.loc[grades_only.isna().any(axis=1)].index.to_numpy()
    
        means_per_row = grades_only.mean(axis=1)
        mean_filled = pd.DataFrame({col: means_per_row for col in grades_only.columns})
        grades_filled_with_mean = grades_only.where(grades_only.notnull(), mean_filled)
    
        updated_data = self.data.copy()
        updated_data.loc[:, "q1":"q5"] = grades_filled_with_mean
    
        return updated_data, rows_with_nulls

    """4. Each participants should receive an integer score for his or her answers, given in a new "score" column you should add. 
    After some deliberation it was decided that if a subject has no grade in two questions or more, the score of that subject will be NA. 
    Write a method that produces this score by averaging the grades of the not-NaN questions in the relevant rows."""
    def score_subjects(self, max_allowed_nans: int = 1) -> pd.DataFrame:
        
        grade_columns = self.data.loc[:, "q1":"q5"]
        self.data["score"] = grade_columns.mean(axis=1).astype("uint8").astype("UInt8")
        rows_with_excess_nans = grade_columns.isna().sum(axis=1) > max_allowed_nans
        self.data.loc[rows_with_excess_nans, "score"] = pd.NA
        return self.data
    

    """5. BONUS 15 POINTS There's reason to believe that there's a correlation between the subject's gender, age and grades."""
    def correlate_gender_age(self) -> pd.DataFrame:
        non_null_age_data = self.data.dropna(axis=0, subset=["age"]).set_index(["gender", "age"], append=True)
        grouped_data = non_null_age_data.loc[:, "q1":"q5"].groupby([None, lambda x: x > 40], level=[1, 2])
        mean_data = grouped_data.mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        mean_data.plot(kind='bar', ax=ax)
        ax.set_xlabel('Gender and Age Group')
        ax.set_ylabel('Average Score')
        ax.set_title('Average Scores by Gender and Age Group')
        ax.legend(title='Questions')

        plt.tight_layout()
        plt.show()
    
        return mean_data


