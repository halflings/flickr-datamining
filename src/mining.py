#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cross_validation import cross_val_score

import config

# Parsing raw CSV file
db = pd.read_csv(config.db_path)
#print db.columns

et = ExtraTreesClassifier(n_estimators=100, max_depth=None, min_samples_split=1, random_state=0)

columns = ["latitude", "longitude"]

sample = 3000
labels = db["hour_taken"].values[:sample]
features = db[list(columns)].values[:sample]

et_score = cross_val_score(et, features, labels, n_jobs=-1).mean()

print "{0} -> ET: {1})".format(columns, et_score)
