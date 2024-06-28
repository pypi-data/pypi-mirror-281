import numpy as np

from splito import MaxDissimilaritySplit


def test_splits_max_dissimilar_default_feats(test_dataset_smiles):
    splitter = MaxDissimilaritySplit(n_splits=2)

    for train_ind, test_ind in splitter.split(test_dataset_smiles):
        assert len(train_ind) + len(test_ind) == len(test_dataset_smiles)
        assert len(set(train_ind).intersection(set(test_ind))) == 0
        assert len(train_ind) > 0 and len(test_ind) > 0


def test_splits_max_dissimilar():
    X = np.random.random((100, 100))
    splitter = MaxDissimilaritySplit(n_splits=2, metric="euclidean")

    for train_ind, test_ind in splitter.split(X):
        assert len(train_ind) + len(test_ind) == len(X)
        assert len(set(train_ind).intersection(set(test_ind))) == 0
        assert len(train_ind) > 0 and len(test_ind) > 0
