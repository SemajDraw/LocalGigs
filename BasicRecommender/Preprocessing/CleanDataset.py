"""
@author James Ward C12404762

created 21/12/2018

"""
import pandas as pd
from sklearn.model_selection import train_test_split

# Set larger console display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)

# Read the aggregated dataset and label columns
column_names = ['user', 'artist', 'track_count']
df = pd.read_csv('../Dataset/AggregatedDataset.csv', sep=',', names=column_names, encoding="utf8", index_col='user')
df.drop('id', axis=1)

# Remove all backslash occurrences in artists name
df['artist'].replace(regex=True, inplace=True, to_replace=r'\\', value=r'')

# Remove all forward slash occurrences in artists name
df['artist'].replace(regex=True, inplace=True, to_replace=r'/', value=r'')

# Remove all commas in artists names
df['artist'].replace(regex=True, inplace=True, to_replace=r',', value=r' &')

# Remove all single quotes in artists names
df['artist'].replace(regex=True, inplace=True, to_replace=r"'", value=r'')

# Remove all quotation mark occurrences in artists name
df['artist'] = df['artist'].map(lambda x: x.replace('"', ''))
df['artist'] = df['artist'].map(lambda x: x.lstrip('"').rstrip('"'))

# If the user has more than 10 songs for an artist limit it to 10
over_ten_index = df['track_count'] >= 10
df.loc[over_ten_index, 'track_count'] = 10

users = df['user'].value_counts()
artists = df['artist'].value_counts()
most_pop = artists.index[0]

quantiles = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.96, 0.97, 0.98, 0.99, 1]
print('Users\n', users.quantile(quantiles))
print('Artists\n', artists.quantile(quantiles))
print('Most popular artist\n', most_pop)

users = users[users >= 5]
artists = artists[artists >= 10]
reduced_df = df.merge(pd.DataFrame({'artist': artists.index})).merge(pd.DataFrame({'user': users.index}))

reduced_df.set_index('user', inplace=True)

# train, test = train_test_split(df, test_size=0.1)

# # 1 million dataset
# million_df = df.head(1000015)
#
# # Half million dataset
# halfmil_df = df.head(500108)
#
# # 100k dataset
# hundredk_df = df.head(100378)

reduced_df.to_csv('../Dataset/CleanedDataset.csv', sep=',', header=False)

# train.to_csv('../Dataset/TrainDataset.csv', sep=',', header=False)

# test.to_csv('../Dataset/TestDataset.csv', sep=',', header=False)

# million_df.to_csv('../Dataset/MillionDataset.csv', sep=',', header=False)
#
# halfmil_df.to_csv('../Dataset/HalfMilDataset.csv', sep=',', header=False)
#
# hundredk_df.to_csv('../Dataset/100kDataset.csv', sep=',', header=False)
