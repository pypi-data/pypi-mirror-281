import sys

import langtorch.semantic_algebra

sys.path.append("..")
import langtorch
from langtorch import TextTensor, String, Text,  Activation
from langtorch import Markdown, XML
from langtorch.tt.functional import dropout
from langtorch import Session
import numpy as np
import torch
from langtorch import TextModule
from langtorch import Chat, ChatML

from langtorch import TextTensor, TextModule, OpenAI, TextLoss
import torch

from langtorch import TextOptimizer
import logging
import re

logging.basicConfig(level=logging.DEBUG)
inputs = TextTensor(["1"])
prompt = TextTensor("Is this a number? {}", requires_grad=True)
task = TextModule(prompt, activation=Activation("gpt-3.5-turbo", T=0))

optimizer = TextOptimizer(task.parameters())
loss_fn = TextLoss("Is the provided answer correct?\nAnswer: {}\nCorrect answer: {}", activation=Activation("gpt-3.5-turbo", max_tokens=1, system_message="Answer only Yes or No"))

answers = task(inputs).detach()
loss = loss_fn(answers+TextTensor(["Yes"]))

loss.backward()
print(answers.grad)
quit()
# print(task.prompt.grad)
# optimizer.step()
# optimizer.zero_grad()
print(task.prompt)

# print("grad tt: \n", tt.grad)


quit()

from torch.utils.data import DataLoader, TensorDataset

# Define the dataset
input_data = (User([f"Is {word} positive?" for word in ["love", "chair", "non-negative"]]) * Assistant(
    ["Yes", "No", "Yes"])).requires_grad_()
target_data = TextTensor(['Yes', "No", "No"]).requires_grad_()

# Wrap the data in a TensorDataset and then create a DataLoader
dataset = TensorDataset(input_data, target_data)
dataloader = DataLoader(dataset, batch_size=1)  # Adjust the batch size as needed

# Define your TextModule
text_module = TextModule("{*}")  # Initialize your TextModule here

# Loop over the DataLoader
for i, (inputs, targets) in enumerate(dataloader):
    # Pass the batch through the TextModule
    outputs = text_module(inputs)

    # Compare outputs to targets and save the results
    # Here, you can define your own comparison logic
    # For example, you can save the results in a list or write them to a file
    print(f"Batch {i}:")
    print("Inputs:", inputs)
    print("Predicted:", outputs)
    print("Targets:", targets)
    print("----")
