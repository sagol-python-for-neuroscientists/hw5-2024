import pandas as pd

class QuestionnaireAnalysis:
    # Other methods including __init__ and read_data go here...

    def remove_rows_without_mail(self) -> pd.DataFrame:
        """Checks self.data for rows with invalid emails, and removes them.

        Returns
        -------
        df : pd.DataFrame
          A corrected DataFrame, i.e. the same table but with the erroneous rows removed and
          the (ordinal) index after a reset.
        """
        def is_valid_email(email: str) -> bool:
            # Check basic structure
            if not isinstance(email, str):
                return False
            if "@" not in email or "." not in email:
                return False
            
            # Check that there is exactly one '@'
            if email.count("@") != 1:
                return False
            
            local_part, domain_part = email.split("@")
            
            # Ensure the '@' is not at the start or end, and '.' is not at the start or end
            if local_part == "" or domain_part == "":
                return False
            if email.startswith("@") or email.endswith("@"):
                return False
            if email.startswith(".") or email.endswith("."):
                return False
            
            # Ensure the domain part is valid (no '.' immediately after '@')
            if domain_part.startswith("."):
                return False
            
            # Add any other checks as needed (e.g., valid characters, length, etc.)
            return True

        # Convert self.data to a DataFrame if it's not already
        df = pd.DataFrame(self.data)
        
        # Filter out rows with invalid emails
        valid_email_mask = df['email'].apply(is_valid_email)
        df_valid = df[valid_email_mask].reset_index(drop=True)
        
        return df_valid
