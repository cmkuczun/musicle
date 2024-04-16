import pandas as pd

# load the data
data = pd.read_csv('/Users/claudia/advanced-db/songuess/data/csv/albums.csv')

# iterate through date attribute in each row, ensuring it is in format YYYY-MM-DD
for i in range(len(data)):
    date = data['date'][i]
    if len(date) == 4:
        data['date'][i] = date + '-01-01'
    elif len(date) == 7:
        data['date'][i] = date + '-01'
    elif len(date) == 10:
        data['date'][i] = date
    else:
        data['date'][i] = '0000-00-00'


# save the data
data.to_csv('/Users/claudia/advanced-db/songuess/data/csv/albums.csv', index=False)