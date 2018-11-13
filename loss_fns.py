"""

File to house the loss functions we plan to use.

"""

import numpy as np
import torch.optim as optim
import torch.nn as nn
import torch
import preprocess

from constants import *

def get_loss_fn(model_name):
    return focal_loss

def focal_loss(y_true, y_pred, reduction, loss_weight = False, gamma=2):
    """
    """ 
    y_true = preprocess.reshapeForLoss(y_true)
    num_examples = torch.sum(y_true, dtype=torch.float32).cuda()

    y_pred = preprocess.reshapeForLoss(y_pred)
    y_pred, y_true = preprocess.maskForLoss(y_pred, y_true)
    y_true = y_true.type(torch.LongTensor).cuda()
    
    if loss_weight:
        loss_fn = nn.NLLLoss(weight = LOSS_WEIGHT,reduction="none")
    else:
        loss_fn = nn.NLLLoss(weight = weight,reduction="none")
    # get the predictions for each true class
    nll_loss = loss_fn(y_pred, y_true)
    x = torch.gather(y_pred, dim=1, index=y_true.view(-1, 1))
    # tricky line, essentially gathers the predictions for the correct class and takes e^{pred} to undo 
    # log operation 
    # .view(-1) necessary to get correct shape
    focal_loss = (1 - torch.exp(x)) ** gamma
    focal_loss = focal_loss.view(-1)
    y = focal_loss * nll_loss
    loss = torch.sum(focal_loss * nll_loss)
    if reduction == "sum":
        if num_examples == 0:
            return None, 0
        else:
            return loss, num_examples
    else:
        if num_examples == 0:
            return None
        else:
            return loss / num_examples

          
def mask_ce_loss(y_true, y_pred, reduction):
    """
    Args:
        y_true - (npy arr) 

    nn.CrossEntropyLoss expects inputs: y_pred [N x classes] and y_true [N x 1]
    As input, y_pred and y_true have shapes [batch x classes x rows x cols] 

    Finally, to get y_true from [N x classes] to [N x 1], we take the argmax along
      the first dimension to get the largest class values from the one-hot encoding

    """
    y_true = preprocess.reshapeForLoss(y_true)
    num_examples = torch.sum(y_true).item()
    y_pred = preprocess.reshapeForLoss(y_pred)
    y_pred, y_true = preprocess.maskForLoss(y_pred, y_true)
   
    loss_fn = nn.NLLLoss(reduction="sum")
    total_loss = loss_fn(y_pred, y_true.type(torch.LongTensor).cuda())
   
    if reduction == "sum":
        if num_examples == 0:
            return None, 0
        else:
            return total_loss, num_examples
    else:
        if num_examples == 0:
            return None
        else:
            return total_loss / (num_examples)

def get_optimizer(params, optimizer_name, lr, momentum, weight_decay):
    if optimizer_name == "sgd":
        return optim.SGD(params, lr=lr, momentum=momentum, weight_decay=weight_decay)
    elif optimizer_name == "adam":
        return optim.Adam(params, lr=lr, weight_decay=weight_decay)

    raise ValueError(f"Optimizer: {optimizer_name} unsupported")

