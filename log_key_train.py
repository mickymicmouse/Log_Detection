# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:25:28 2021

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
import pickle

def generate(name, window_size, num_classes):
    """ Structure

    root/
      └── data/
          ├── hdfs_train
          ├── hdfs_test_abnormal
          └── hdfs_test_normal
      └── your_code.ipynb
    """
    num_sessions = 0
    inputs = []
    outputs = []
    with open("Data/" + name, "rb") as f:
        seq_train = pickle.load(f)
        
    for line in seq_train:
        num_sessions += 1
        # line = tuple(map(lambda n: n - 1, map(int, line.strip().split())))
        for i in range(len(line) - window_size):
            inputs.append(line[i : i + window_size])
            outputs.append(line[i + window_size])
    print("Number of sessions({}): {}".format(name, num_classes))
    print("Number of seqs({}): {}".format(name, len(inputs)))
    dataset = TensorDataset(
        torch.tensor(inputs, dtype=torch.float), torch.tensor(outputs)
    )
    return dataset


def main():
    # Load hyperparameters
    hparams = Hyperparameters()
    
    # Fix seed for reproducibility
    pl.seed_everything(hparams.seed)
    
    # Set dataset and dataloader
    train_dset = generate("uri_train", hparams.window_size, hparams.num_classes)
    train_loader = DataLoader(
        train_dset, batch_size=hparams.batch_size, shuffle=True, pin_memory=True
    )
    
    valid_dset = generate("uri_valid", hparams.window_size, hparams.num_classes)
    valid_loader = DataLoader(
        valid_dset, batch_size=hparams.batch_size, shuffle=False, pin_memory=True
    )
    # Set model
    model = DeepLog(
        input_size=hparams.input_size,
        hidden_size=hparams.hidden_size,
        window_size=hparams.window_size,
        num_layers=hparams.num_layers,
        num_classes=hparams.num_classes,
        lr=hparams.lr,
    )
    
    # Set training config
    early_stopping = EarlyStopping(
        monitor="trn_loss", patience=3, strict=False, verbose=True, mode="min"
    )
    logger = TensorBoardLogger("logs", name="deeplog")
    checkpoint_callback = ModelCheckpoint(
        monitor="trn_loss",
        dirpath="deeplog/",
        filename="checkpoint-{epoch:02d}-{trn_loss:.2f}",
        save_top_k=3,
        mode="min",
    )
    
    # Set trainer
    trainer = pl.Trainer(
        # gpus=hparams.gpus,
        
        deterministic=True,
        logger=logger,
        callbacks=[early_stopping, checkpoint_callback],
        max_epochs=hparams.epoch,
    )
    # Train model
    # trainer.fit(model, train_loader)
    trainer.fit(model, train_loader, valid_loader)
if __name__ == '__main__':
    main()