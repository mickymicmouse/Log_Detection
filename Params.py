# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 16:26:54 2021

@author: seoun
"""

class Hyperparameters:
    """ Hyperparameters for DeepLog """

    seed = 711

    gpus = 1
    epoch = 200
    batch_size = 2048
    lr = 0.001

    input_size = 1
    num_classes = 42611
    num_layers = 2
    hidden_size = 64
    window_size = 10

    # for prediction
    num_candidates = 9