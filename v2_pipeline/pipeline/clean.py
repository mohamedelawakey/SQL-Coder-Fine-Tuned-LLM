import pandas as pd

# drop duplicates
def clean_data(data):
    print("Before:", data.shape)
    data = data.drop_duplicates()
    print("After:", data.shape)

    return data
