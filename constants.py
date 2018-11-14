import numpy as np
import torch.nn as nn
import torch

LOSS_WEIGHT = np.array([5.57, 1.67, 5.88, 8.20, 25.57])
LOSS_WEIGHT = torch.tensor(LOSS_WEIGHT)
LOSS_WEIGHT = (1 - 1 / LOSS_WEIGHT.type(torch.FloatTensor).cuda())

DATA_FILE_PATH = "/home/data"
CROP_LABELS = ['maize','groundnut', 'rice', 'soya bean', 'sorghum', 'yam', 'sesame', 'beans', 'sunflower', 'chick peas', 'wheat', 'other']
SPLITS = ['train', 'val', 'test']
NON_DL_MODELS = ['logreg', 'random_forest']
DL_MODELS = ['bidir_clstm','fcn', 'unet', 'fcn_crnn']
S1_NUM_BANDS = 2
S2_NUM_BANDS = 10
GRID_SIZE = 64
MIN_TIMESTAMPS = 16

LABEL_DIR = "raster_64x64_npy"
S1_DIR = "s1_npy"
S2_DIR = "s2_64x64_npy"
NROW = 10

INT_POWER_EXP = ["hidden_dims", 'weight_scale']
REAL_POWER_EXP = ["weight_decay", "lr"]
INT_HP = ['batch_size', 'crnn_num_layers', 'gamma']
FLOAT_HP = ['momentum']
STRING_HP = ['optimizer']

S1_BAND_MEANS = np.array([-11.411486013023465, -17.94899228790914])

S1_BAND_STDS = np.array([3.738300142932384, 5.034191069133747])

S2_BAND_MEANS = np.array([2626.4081074042033, 2520.2485066503864, 2615.7752958508927, 2720.921209161932, 3204.026112633294, 3536.487707240784, 3331.169189873876, 3757.642916408606, 2819.208490729178, 2032.4985852255897])

S2_BAND_STDS = np.array([2232.5334052935987, 2147.2823093704483, 2244.5187602951046, 2153.469486034919, 2129.289151884002, 2190.9747736567133, 2059.9788191903117, 2174.898225617082, 1237.3449495354944, 937.4064744674777])

CM_CLASSES = ['groundnut', 'maize', 'rice', 'soyabean', 'yam']
CM_LABELS = [0, 1, 2, 3, 4]
