import os
import sys
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.optim as optim

from mydatasets import load_seizure_dataset
from utils import train, evaluate
from plots import plot_learning_curves, plot_confusion_matrix
from mymodels import MyMLP, MyCNN, MyRNN

torch.manual_seed(0)
if torch.cuda.is_available():
	torch.cuda.manual_seed(0)

# Set a correct path to the seizure data file you downloaded
PATH_TRAIN_FILE = "../data/seizure/seizure_train.csv"
PATH_VALID_FILE = "../data/seizure/seizure_validation.csv"
PATH_TEST_FILE = "../data/seizure/seizure_test.csv"

# Path for saving model
PATH_OUTPUT = "../output/seizure/"
os.makedirs(PATH_OUTPUT, exist_ok=True)

# Some parameters
MODEL_TYPE = 'MLP'  # TODO: Change this to 'MLP', 'CNN', or 'RNN' according to your task
NUM_EPOCHS = 3
BATCH_SIZE = 32
USE_CUDA = False  # Set 'True' if you want to use GPU
NUM_WORKERS = 0  # Number of threads used by DataLoader. You can adjust this according to your machine spec.

train_dataset = load_seizure_dataset(PATH_TRAIN_FILE, MODEL_TYPE)
valid_dataset = load_seizure_dataset(PATH_VALID_FILE, MODEL_TYPE)
test_dataset = load_seizure_dataset(PATH_TEST_FILE, MODEL_TYPE)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
valid_loader = torch.utils.data.DataLoader(valid_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)


if MODEL_TYPE == 'MLP':
	model = MyMLP()
	save_file = 'MyMLP.pth'
elif MODEL_TYPE == 'CNN':
	model = MyCNN()
	save_file = 'MyCNN.pth'
elif MODEL_TYPE == 'RNN':
	model = MyRNN()
	save_file = 'MyRNN.pth'
else:
	raise AssertionError("Wrong Model Type!")

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion.to(device)

best_val_acc = 0.0
train_losses, train_accuracies = [], []
valid_losses, valid_accuracies = [], []

for epoch in range(NUM_EPOCHS):
	train_loss, train_accuracy = train(model, device, train_loader, criterion, optimizer, epoch)
	valid_loss, valid_accuracy, valid_results = evaluate(model, device, valid_loader, criterion)

	train_losses.append(train_loss)
	valid_losses.append(valid_loss)

	train_accuracies.append(train_accuracy)
	valid_accuracies.append(valid_accuracy)

	is_best = valid_accuracy > best_val_acc  # let's keep the model that has the best accuracy, but you can also use another metric.
	if is_best:
		torch.save(model, os.path.join(PATH_OUTPUT, save_file))

plot_learning_curves(train_losses, valid_losses, train_accuracies, valid_accuracies)

best_model = torch.load(os.path.join(PATH_OUTPUT, save_file))
test_loss, test_accuracy, test_results = evaluate(best_model, device, test_loader, criterion)

class_names = ['Seizure', 'TumorArea', 'HealthyArea', 'EyesClosed', 'EyesOpen']
plot_confusion_matrix(test_results, class_names)
