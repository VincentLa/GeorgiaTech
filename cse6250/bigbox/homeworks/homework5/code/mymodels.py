import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class MyMLP(nn.Module):
    """
    Define Multi Layer Perceptron Class

    Note that examples taken from: https://github.com/ast0414/CSE6250BDH-LAB-DL/blob/master/1_FeedforwardNet.ipynb  
    """
    def __init__(self):
        """
        Initialize MLP Class

        As taken from the instructions, we implement a 3-Layer MLP composed by 16 units.
        What does that mean for Layers?: https://piazza.com/class/jjjilbkqk8m1r4?cid=998
        """
        super(MyMLP, self).__init__()
        self.hidden1 = nn.Linear(in_features=179, out_features=16)
        self.out = nn.Linear(in_features=16, out_features=5)

    def forward(self, x):
        """Use Sigmoid Activation Function as denoted in HW"""
        x = torch.sigmoid(self.hidden1(x))
        x = self.out(x)
        return x


class MyCNN(nn.Module):
    def __init__(self):
        super(MyCNN, self).__init__()

    def forward(self, x):
        return x


class MyRNN(nn.Module):
    def __init__(self):
        super(MyRNN, self).__init__()

    def forward(self, x):
        return x


class MyVariableRNN(nn.Module):
    def __init__(self, dim_input):
        super(MyVariableRNN, self).__init__()
        # You may use the input argument 'dim_input', which is basically the number of features

    def forward(self, input_tuple):
        # HINT: Following two methods might be useful
        # 'pack_padded_sequence' and 'pad_packed_sequence' from torch.nn.utils.rnn

        seqs, lengths = input_tuple

        return seqs
