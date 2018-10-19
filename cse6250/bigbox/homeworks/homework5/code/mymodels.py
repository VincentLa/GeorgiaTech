import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


class MyMLP(nn.Module):
	def __init__(self):
		super(MyMLP, self).__init__()

	def forward(self, x):
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