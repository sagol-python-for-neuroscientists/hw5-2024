import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plot

class QuestionnaireAnalysis:
   def __init__(self, data_fname): #worked
        
      if isinstance(data_fname, str):
            
            self.data_fname = Path(data_fname)
      elif isinstance(data_fname, Path):
            
            self.data_fname = data_fname
      else:
            raise TypeError()
        
      if not self.data_fname.exists():
            raise ValueError()
        

      self.data = None
   
   def read_data(self): #worked
      self.data = pd.read_json(self.data_fname)
      return self.data      
   
   def show_age_distrib(self): #worked
      data = self.read_data()
      bins = np.arange(0,110,10)
      by_age = np.histogram(data.age,bins=bins)
      plot.hist(data.age,bins=bins)
      plot.show()
      return by_age


   def remove_rows_without_mail(self): #worked
      data = self.read_data() 
      substring1 = data['email'].str.contains(r'[^@]*@[^@]*$') # contains exactly one @
      substring2 = ~data['email'].str.contains(r'@\.') # does not contain the @.
      substring3 = ~data['email'].str.contains(r'\.$') # not . at the end
      substring4 = ~data['email'].str.contains(r'^\.') # not . at the start
      substring5 = data['email'].str.contains(r'\.')
      correct_emails =data[substring1 & substring2 & substring3 & substring4 & substring5]
      correct_emails.reset_index(drop=True, inplace=True)  
      return  correct_emails



   def fill_na_with_mean(self): 
      data =  self.read_data()
      rows = []
      for index, row in data[['q1','q2','q3','q4','q5']].iterrows():
        row_mean = row.mean()
        data.loc[index,['q1','q2','q3','q4','q5']] = row.replace(np.nan, row_mean)
        if row.isnull().any():
         rows.append(index)
      return data,rows

 
   def score_subjects(self, maximal_nans_per_sub = 1): #works
      data =  self.read_data() 
      score = []
      for idx,row in data[['q1','q2','q3','q4','q5']].iterrows():
       sumNAN = data.loc[idx,['q1','q2','q3','q4','q5']].isnull().sum()
       if sumNAN > maximal_nans_per_sub:
        score.append(np.nan)
       else:
        score.append(np.floor(row.mean()))
      data['score'] = score
      data['score'] = data['score'].astype('UInt8')
      return data

   def correlate_gender_age(self):
     data =  self.read_data() 
     data = data.dropna(subset='age')
     data.loc[:, 'age'] = data['age'] > 40
     data.set_index(['gender','age'],inplace=True)
     grouped = data.groupby(['gender','age'])[['q1','q2','q3','q4','q5']].mean()
     return grouped


    