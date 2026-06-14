import pandas as pd

def load_ballots(sheet_id):

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv"
    )

    df = pd.read_csv(url)

    # Drop second column (index 1)
    df = df.drop(df.columns[1], axis=1)

    return df
