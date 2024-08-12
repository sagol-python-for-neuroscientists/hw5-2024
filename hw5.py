import pathlib
from typing import Union, Tuple
import numpy as np
import pandas as pd
import re

class QuestionnaireAnalysis:


    def __init__(self, data_fname: Union[pathlib.Path, str]):
        self.data_fname=pathlib.Path(data_fname) if isinstance(data_fname, str) else data_fname
        if not self.data_fname.is_file():
            raise ValueError("The file does not exist.")
        self.data=None

    def read_data(self):

        try:
            self.data = pd.read_json(self.data_fname)
        except ValueError as e:
            raise ValueError(f"Failed to read JSON file: {e}")

    def show_age_distrib(self) -> Tuple[np.ndarray, np.ndarray]:
        age_df=self.data['age'].dropna()
        hist, bins=np.histogram(age_df, bins=np.arange(0,101,10))
        
        return hist, bins

    def remove_rows_without_mail(self) -> pd.DataFrame:
        email_pattern=re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        valid_emails_df=self.data[self.data['email'].apply(lambda x: isinstance(x,str) and email_pattern.match(x) is not None)]
        valid_emails_df.reset_index(drop=True,inplace=True)
        return valid_emails_df
    
    def fill_na_with_mean(self) -> Tuple[pd.DataFrame, np.ndarray]:
        original_df = self.data.copy()
        questions = ['q1','q2','q3','q4','q5']
        
        def fill_mean(row):
            nan_indices=row[questions].isna()
            if nan_indices.any():
                mean_value=row[questions].mean()
                row[questions]=row[questions].fillna(mean_value)
            return row
        
        nan_rows=original_df[original_df[questions].isna().any(axis=1)]
        filled_df=original_df.apply(fill_mean, axis=1)
        corrected_indices=nan_rows.index.to_numpy()
        
        return filled_df,corrected_indices

    def score_subjects(self, maximal_nans_per_sub: int = 1) -> pd.DataFrame:

        original_df=self.data.copy()
        questions=['q1','q2','q3','q4','q5']

        def calculate_score(row):
            nan_count=row[questions].isna().sum()
            if nan_count> maximal_nans_per_sub:
                return np.nan
            else:
                return np.floor(row[questions].mean())

        original_df['score'] = original_df.apply(calculate_score, axis=1).clip(0, 255).astype(pd.UInt8Dtype())
        
        return original_df
