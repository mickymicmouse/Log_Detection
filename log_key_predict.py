# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 11:15:16 2021

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
    with open("Data/" + name, "rb") as f:
        file = pickle.load(f)
    for ln in file:
        line = list(map(lambda n: n - 1, ln))
        ln = line + [-1] * (window_size + 1 - len(line))
        hdfs.add(tuple(ln))
        # hdfs.append(tuple(ln))
    print("Number of sessions({}): {}".format(name, len(hdfs)))
    return hdfs
    

def main():
    device = DeepLog.device
    hparams = Hyperparameters()
    # best model path 정의 
    bestmodel = DeepLog.load_from_checkpoint(checkpoint_callback.best_model_path)
    
    print("model_path: {}".format(checkpoint_callback.best_model_path))
    test_normal_loader = generate_pred("uri_valid", hparams.window_size)
    # test_abnormal_loader = generate_pred("hdfs_test_abnormal", hparams.window_size)
    
    TP = 0
    FP = 0
    
    # Test the model
    inputed = []
    labeled = []
    input_pred = []
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
                print(label)
                inputed.append(seq)
                labeled.append(label)
                input_pred.append(predicted)
                if label not in predicted:
                    FP += 1
                    
    elapsed_time = time.time() - start_time
    with open ("/home/itm1/seungjun/log_key/result/inputed", "wb") as file:
        pickle.dump(inputed, file)
    with open ("/home/itm1/seungjun/log_key/result/labeled", "wb") as file:
        pickle.dump(labeled, file)
    with open ("/home/itm1/seungjun/log_key/result/input_pred", "wb") as file:
        pickle.dump(input_pred, file)
        
    print("elapsed_time: {:.3f}s".format(elapsed_time))
    print("FP : %d" %FP)
    # Compute precision, recall and F1-measure
    
    print("Finished Predicting")
    
if __name__=="__main__":
    main()