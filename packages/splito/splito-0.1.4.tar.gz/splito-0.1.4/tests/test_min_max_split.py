from splito import MolecularMinMaxSplit


def test_splits_min_max(test_dataset_smiles):
    splitter = MolecularMinMaxSplit(n_splits=2)

    for train_ind, test_ind in splitter.split(test_dataset_smiles):
        assert len(train_ind) + len(test_ind) == len(test_dataset_smiles)
        assert len(set(train_ind).intersection(set(test_ind))) == 0
        assert len(train_ind) > 0 and len(test_ind) > 0
