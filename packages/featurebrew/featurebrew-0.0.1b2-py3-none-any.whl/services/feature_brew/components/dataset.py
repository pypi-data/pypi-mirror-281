import random
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class FeatureBrewDataset:
    def __init__(self, dataset, data_source, shot=4, seed=0):
        self.dataset_name = dataset
        self.data_source = data_source
        self.shot = shot
        self.seed = seed

        self._set_seed(self.seed)
        self.df, self.X_train, self.X_test, self.y_train, self.y_test, self.target_attr, self.label_list, self.is_cat = self._get_dataset(dataset, shot, seed)
        self.X_all = self.df.drop(self.target_attr, axis=1)

    def _set_seed(self, seed):
        random.seed(seed)
        np.random.seed(seed)

    def _get_dataset(self, data_name, shot, seed):
        file_name = f"{self.data_source}/{data_name}/{data_name}-processed.csv"
        df = pd.read_csv(file_name)
        default_target_attribute = df.columns[-1]

        categorical_indicator = [True if (dt == np.dtype('O') or pd.api.types.is_string_dtype(dt)) else False for dt in
                                 df.dtypes.tolist()][:-1]
        attribute_names = df.columns[:-1].tolist()

        X = df.convert_dtypes()
        y = df[default_target_attribute].to_numpy()
        label_list = np.unique(y).tolist()
        X_train, X_test, y_train, y_test = train_test_split(
            X.drop(default_target_attribute, axis=1),
            y,
            test_size=0.2,
            random_state=seed,
            stratify=y
        )

        assert (shot <= 128)  # We only consider the low-shot regimes here
        X_new_train = X_train.copy()
        X_new_train[default_target_attribute] = y_train
        sampled_list = []
        total_shot_count = 0
        remainder = shot % len(np.unique(y_train))
        for _, grouped in X_new_train.groupby(default_target_attribute):
            sample_num = shot // len(np.unique(y_train))
            if remainder > 0:
                sample_num += 1
                remainder -= 1
            grouped = grouped.sample(sample_num, random_state=seed)
            sampled_list.append(grouped)
        X_balanced = pd.concat(sampled_list)
        X_train = X_balanced.drop([default_target_attribute], axis=1)
        y_train = X_balanced[default_target_attribute].to_numpy()

        return df, X_train, X_test, y_train, y_test, default_target_attribute, label_list, categorical_indicator

