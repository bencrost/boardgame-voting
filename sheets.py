import pandas as pd

def load_ballots(sheet_id):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv"
    )

    return pd.read_csv(url)
