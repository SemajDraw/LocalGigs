import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import scipy.sparse as sp
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from math import sqrt

# Set graph details
plt.rcParams['figure.figsize'] = [15, 5]
plt.rcParams['font.family'] = 'sans-serif'
plt.style.use('seaborn-darkgrid')

# Set larger console display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)

# Read dataset and label columns
df = pd.read_csv('data/NPLC_Matrix.csv', sep=',', header=0)

query_index = np.random.choice(df.shape[0])
print(query_index)

train_dataset_matrix = csr_matrix(df.values)

model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
model_knn.fit(train_dataset_matrix)


distance, indices = model_knn.kneighbors(df.iloc[query_index, :].reshape(1, -1), n_neighbors=6)

for i in range(0, len(distance.flatten())):
    if i == 0:
        print('Recommendations for {0}' .format(df.index[query_index]))
    else:
        print('{0}: {1}, with disctance of {2}:' .format(i, df.index[indices.flatten()[i]], distance.flatten()))

