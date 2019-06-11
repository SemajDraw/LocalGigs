from django.conf import settings
from surprise import Dataset, Reader
import pandas as pd
import json
import os


class PreProcessing:

    def __init__(self, query_dict):
        """Extract user email and artists track count from Http QueryDict"""
        self.user_dict = query_dict.dict()
        self.user_email = list(self.user_dict.keys())[0]
        self.artist_track_count = json.loads(self.user_dict[self.user_email])

    def process_data(self):
        """Class entry point"""
        fav_artists = self.build_favourite_artists(self.artist_track_count)
        user_df = self.create_user_df()

        return self.create_surprise_dataset(user_df), fav_artists

    @staticmethod
    def build_favourite_artists(artist_count):
        """Return list of artists with track count > 3"""
        favourite_artists = []
        for k, v in artist_count.items():
            if v >= 3:
                favourite_artists.append(k)

        return favourite_artists

    def create_user_df(self):
        """Create user DataFrame using email as user and artist_track_count
            dictionary as artist and track_count columns"""
        df = pd.DataFrame(self.artist_track_count.items(), columns=['artist', 'track_count'])
        df['user'] = pd.Series(str(self.user_email), index=df.index)
        df = df[['user', 'artist', 'track_count']]

        return df

    def create_surprise_dataset(self, user_df):
        """Create Surprise Dataset from Pandas DataFrame"""
        dataset_path = os.path.join(settings.BASE_DIR, 'datasets/CleanedDataset.csv')
        df = pd.read_csv(dataset_path, sep=',', names=['user', 'artist', 'track_count'], encoding="utf8")

        # If the user is not in the dataset already add them
        if not user_df.user.values[0] in df.user.values:
            df = pd.concat([df, user_df])
            self.update_dataset(dataset_path, df)

        reader = Reader(rating_scale=(1, 10))

        return Dataset.load_from_df(df[['user', 'artist', 'track_count']], reader)

    @staticmethod
    def update_dataset(dataset_path, df):
        """Updates the stored dataset with the new users data"""
        df.set_index('user', inplace=True)
        df.to_csv(dataset_path, sep=',', header=False)
