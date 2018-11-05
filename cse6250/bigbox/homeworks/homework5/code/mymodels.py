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

        #### Adding more Hidden Layers for 1.2.e, to restore defaults comment out this section
        self.hidden2 = nn.Linear(in_features=16, out_features=16)
        ####

        self.out = nn.Linear(in_features=16, out_features=5)

    def forward(self, x):
        """Use Sigmoid Activation Function as denoted in HW"""
        x = torch.sigmoid(self.hidden1(x))

        #### Adding more Hidden Layers for 1.2.e, to restore defaults comment out this section
        x = torch.sigmoid(self.hidden2(x))
        ####

        x = self.out(x)
        return x


class MyCNN(nn.Module):
    """
    Define Convoluted Neural Network Class

    Note that examples taken from: http://www.sunlab.org/teaching/cse6250/fall2018/dl/dl-cnn.html#convolution
    https://github.com/ast0414/CSE6250BDH-LAB-DL/blob/master/2_CNN.ipynb

    If Getting RuntimeError: Expected 3-dimensional input for 3-dimensional weight, see: https://piazza.com/class/jjjilbkqk8m1r4?cid=974
    """
    def __init__(self):
        super(MyCNN, self).__init__()
        ## Part 1: Default what HW Asks for
        # self.conv1 = nn.Conv1d(in_channels=1, out_channels=6, kernel_size=5)
        # self.pool = nn.MaxPool1d(kernel_size=2)
        # self.conv2 = nn.Conv1d(in_channels=6, out_channels=16, kernel_size=5)
        # self.fc1 = nn.Linear(16 * 41, 128)
        # self.fc2 = nn.Linear(128, 5)

        ## 1.3.d (1) Improving CNN
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=6, kernel_size=5)
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.conv2 = nn.Conv1d(in_channels=6, out_channels=16, kernel_size=5)
        self.fc1 = nn.Linear(in_features=16 * 41, out_features=128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 5)

        ## 1.3.d (2) Improving CNN
        # self.conv1 = nn.Conv1d(in_channels=1, out_channels=6, kernel_size=5)
        # self.pool = nn.MaxPool1d(kernel_size=2)
        # self.conv2 = nn.Conv1d(in_channels=6, out_channels=16, kernel_size=5)
        # self.conv3 = nn.Conv1d(in_channels=16, out_channels=16, kernel_size=5)
        # self.fc1 = nn.Linear(in_features=16 * 41, out_features=128)
        # self.fc2 = nn.Linear(128, 64)
        # self.fc3 = nn.Linear(64, 5)

    def forward(self, x):
        ## Part 1: Default what HW Asks for
        # x = self.pool(nn.functional.relu(self.conv1(x)))
        # x = self.pool(nn.functional.relu(self.conv2(x)))
        # x = x.view(-1, 16 * 41)
        # x = nn.functional.relu(self.fc1(x))
        # x = self.fc2(x)

        ## 1.3.d (1) Improving CNN
        x = self.pool(nn.functional.relu(self.conv1(x)))
        x = self.pool(nn.functional.relu(self.conv2(x)))
        x = x.view(-1, 16 * 41)
        x = nn.functional.relu(self.fc1(x))
        x = nn.functional.relu(self.fc2(x))
        x = self.fc3(x)

        ## 1.3.d (2) Improving CNN
        # x = self.pool(nn.functional.relu(self.conv1(x)))
        # x = self.pool(nn.functional.relu(self.conv2(x)))
        # x = self.pool(nn.functional.relu(self.conv3(x)))
        # x = x.view(-1, 9216)
        # x = nn.functional.relu(self.fc1(x))
        # x = nn.functional.relu(self.fc2(x))
        # x = self.fc3(x)
        return x


class MyRNN(nn.Module):
    """
    Define Recurrent Neural Networks

    Note that a lot of code is taken from examples here: https://github.com/ast0414/CSE6250BDH-LAB-DL/blob/master/3_RNN.ipynb
    """
    def __init__(self):
        super(MyRNN, self).__init__()
        # self.rnn = nn.GRU(input_size=1, hidden_size=16, num_layers=1, batch_first=True, dropout=0.5)
        
        # 1.4.d (1)
        self.rnn = nn.GRU(input_size=1, hidden_size=16, num_layers=5, batch_first=True, dropout=0.5)
        self.fc = nn.Linear(in_features=16, out_features=5)

    def forward(self, x):
        x, _ = self.rnn(x)
        # https://piazza.com/class/jjjilbkqk8m1r4?cid=963
        x = torch.tanh(x[:, -1, :])
        # x = x[:, -1, :]
        x = self.fc(x)
        return x


class MyVariableRNN(nn.Module):
    """
    Define Own Recurrent Neural Networks

    Note that a lot of code is taken from examples here: https://github.com/ast0414/CSE6250BDH-LAB-DL/blob/master/3_RNN.ipynb
    """
    def __init__(self, dim_input):
        super(MyVariableRNN, self).__init__()
        # You may use the input argument 'dim_input', which is basically the number of features
        # self.fc1 = nn.Linear(in_features=dim_input, out_features=32)
        # self.rnn = nn.GRU(input_size=32, hidden_size=16, num_layers=5, batch_first=True, dropout=0.5)
        self.rnn = nn.GRU(input_size=dim_input, hidden_size=16, num_layers=5, batch_first=True, dropout=0.5)
        self.fc2 = nn.Linear(in_features=16, out_features=2)

    def forward(self, input_tuple):
        # HINT: Following two methods might be useful
        # 'pack_padded_sequence' and 'pad_packed_sequence' from torch.nn.utils.rnn

        # pack
        packed_input = pack_padded_sequence(input_tuple[0], input_tuple[1], batch_first=True)
        # print('printing packed input')
        # print(packed_input)

        # print('trying to run rnn')
        x, _ = self.rnn(packed_input)
        x, unpacked_len = pad_packed_sequence(x, batch_first=True)
        x = x[:, -1, :]
        x = self.fc2(x)
        # print('printing x at the end')
        # print(x.shape)
        return x

        # seqs, lengths = input_tuple

        # return seqs

        ## TESTING ONLY
        # x, _ = self.rnn(input_tuple)
        # x = torch.tanh(x[:, -1, :])
        # x = self.fc(x)
        # return x
