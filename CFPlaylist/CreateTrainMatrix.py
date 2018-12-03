import pandas as pd
from sklearn.model_selection import train_test_split


# Set larger console display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)

# Read dataset and label columns
df = pd.read_csv('data/NowPlayingListenCount.csv', sep=',', header=0)

# Splits dataset into 2 blocks 40% for testing 60% for training
train_data, test_data = train_test_split(df, test_size=0.4, shuffle=False)

# Create a sparse matrix from the test_data dataframe
test_data_pivot = test_data.pivot(index='USER', columns='ARTIST', values='LISTENCOUNT').fillna(0)
test_data_pivot.to_csv('data/NPLC_Matrix.csv', sep=',')

