# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 17:37:16 2021

@author: seoun
"""


import os
import sys
import time
os.chdir(r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding")
import torch
import torch.nn as nn
import torch.optim as optim
import pytorch_lightning as pl

from tqdm import tqdm
from torch.utils.data import TensorDataset, DataLoader
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger

from Params import Hyperparameters
from log_key_detection_models import DeepLog
from log_key_train import *
import pickle

def generate_pred(name, window_size):
    hdfs = set()
    # hdfs = [] # for using full dataset
    with open("data/" + name, "r") as f:
        for ln in f.readlines():
            ln = list(map(lambda n: n - 1, map(int, ln.strip().split())))
            ln = ln + [-1] * (window_size + 1 - len(ln))
            hdfs.add(tuple(ln))
            # hdfs.append(tuple(ln))
    print("Number of sessions({}): {}".format(name, len(hdfs)))
    return hdfs
    
device = DeepLog.device

bestmodel = DeepLog.load_from_checkpoint(checkpoint_callback.best_model_path)

print("model_path: {}".format(checkpoint_callback.best_model_path))
test_normal_loader = generate_pred("hdfs_test_normal", hparams.window_size)
test_abnormal_loader = generate_pred("hdfs_test_abnormal", hparams.window_size)

TP = 0
FP = 0

# Test the model
start_time = time.time()
with torch.no_grad():
    for line in tqdm(test_normal_loader):
        for i in range(len(line) - hparams.window_size):
            seq = line[i : i + hparams.window_size]
            label = line[i + hparams.window_size]
            seq = (
                torch.tensor(seq, dtype=torch.float).view(
                    -1, hparams.window_size, hparams.input_size
                )
            )
            label = torch.tensor(label).view(-1) 
            output = bestmodel(seq)
            predicted = torch.argsort(output, 1)[0][-hparams.num_candidates :]
            if label not in predicted:
                FP += 1
                break
                
with torch.no_grad():
    for line in tqdm(test_abnormal_loader):
        for i in range(len(line) - hparams.window_size):
            seq = line[i : i + hparams.window_size]
            label = line[i + hparams.window_size]
            seq = (
                torch.tensor(seq, dtype=torch.float).view(
                    -1, hparams.window_size, hparams.input_size
                )
            )
            label = torch.tensor(label).view(-1)
            output = bestmodel(seq)
            predicted = torch.argsort(output, 1)[0][-hparams.num_candidates :]
            if label not in predicted:
                TP += 1
                break
                
elapsed_time = time.time() - start_time
print("elapsed_time: {:.3f}s".format(elapsed_time))

# Compute precision, recall and F1-measure
FN = len(test_abnormal_loader) - TP
P = 100 * TP / (TP + FP)
R = 100 * TP / (TP + FN)
F1 = 2 * P * R / (P + R)
print(
    "false positive (FP): {}, false negative (FN): {}, Precision: {:.3f}%, Recall: {:.3f}%, F1-measure: {:.3f}%".format(
        FP, FN, P, R, F1
    )
)
print("Finished Predicting")