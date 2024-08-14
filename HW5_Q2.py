import pandas as pd
import pathlib

class QuestionnaireAnalysis:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
          A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
          the (ordinal) index after a reset.
        """
        # Define a function to validate the email
        def is_valid_email(email):
            # Check basic conditions
            if not isinstance(email, str):
                return False
            email = email.strip()

            # Check if there's exactly one "@" and it is not at the start or end
            if email.count('@') != 1 or email.startswith('@') or email.endswith('@'):
                return False
            
            # Check if there is at least one "." and it is not at the start or end
            if email.count('.') < 1 or email.startswith('.') or email.endswith('.'):
                return False
            
            # Check if the character immediatly after "@" is not "."
            at_index = email.index('@')
            if email[at_index + 1] == '.':
                return False

            # Additional Checks: no spaces allowed
            if ' ' in email:
                return False
            
            return True
        
        # Apply the validation function
        valid_email_mask = self.data['email'].apply(is_valid_email)

        # Filter out invalid emails and reset index
        df_valid = self.data[valid_email_mask].reset_index(drop=True)

        return df_valid
    

# Load the test data from 'q2_email.csv'
test_df = pd.read_csv('q2_email.csv')

# Create an instance of the QuestionnaireAnalysis with the test data
analysis = QuestionnaireAnalysis(test_df)

# Apply the email filtering method
cleaned_df = analysis.remove_rows_without_mail()

# Print the cleaned DataFrame
print(cleaned_df)












    


 
 