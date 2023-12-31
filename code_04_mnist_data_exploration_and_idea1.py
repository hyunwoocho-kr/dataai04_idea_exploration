# -*- coding: utf-8 -*-
"""code 04_mnist_Data_exploration_and_Idea1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GXZET8lqyXlUesXJrWF_Km5GNQ4ErZhx
"""

#hide
!pip install -Uqq fastbook
#import fastbook
#fastbook.setup_book()

#hide
from fastai.vision.all import *
from fastbook import *

matplotlib.rc('image', cmap='gist_gray')

URLs.MNIST_SAMPLE

path = untar_data(URLs.MNIST_SAMPLE)

URLs.MNIST_SAMPLE

path

!ls -a /root/.fastai/data/mnist_sample/train

!ls -a /root/.fastai/data/mnist_sample/train/3

!cp -r /root/.fastai/data/mnist_sample/train/3 ./sample_data/3

"""# Data Exploration"""

path.ls() # We can see what's in this directory by using "ls." It also displays the count of items.
# The MNIST dataset follows a common layout for machine learning datasets: separate folders for the training set and the validation set.

(path/'train').ls()
# You can use "/" and a directory name (e.g., "/train") after a path object to access a subdirectory.
# There are a folder of 3s and a folder of 7s in the train folder.
# The directory names will be used as labels.

(path/'train'/'3').ls()

!ls /root/.fastai/data/mnist_sample

!ls /root/.fastai/data/mnist_sample/train/3

(path/'train'/'3').ls()

threes = (path/'train'/'3').ls().sorted() # we want to sort it to make sure we have a same order everytime we create this object.

threes

sevens = (path/'train'/'7').ls().sorted()

type(threes)

threes[0]

sevens

im3_path = threes[1] # Let's take a look at one of the threes.
im3 = Image.open(im3_path) # Image class from the Python Imaging Library (PIL), which is the most widely used Python package for opening, manipulating, and viewing images.
im3

im3_path

# In a computer, everything is represented as a number.
# To view the numbers that make up this image, we have to convert it to a NumPy array or a PyTorch tensor.
tensor(im3) # PyTorch tensor

tensor(im3)[4:10,4:10]
# The 4:10 indicates we requested the rows from index 4 (included) to 10 (not included) and the same for the columns.
# PyTorch indexes from top to bottom and left to right, so this section is located in the top-left corner of the image.

"""# List comprehension
https://www.w3schools.com/python/python_lists_comprehension.asp

https://shoark7.github.io/programming/python/about-list-comprehension-python
"""

alist = [0, 1, 2, 3, 4]

type(alist)

range(5) # returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before 5.

list_compre = [x**2 for x in range(5)]
list_compre

"""## Idea 1: Calculating Pixel Similarity"""

Image.open(threes[1])

tensor(Image.open(threes[1]))

threes

#path = untar_data(URLs.MNIST_SAMPLE)
#threes = (path/'train'/'3').ls().sorted()
three_tensors = [tensor(Image.open(o)) for o in threes]

type(three_tensors)

len(three_tensors)

three_tensors[2]

seven_tensors = [tensor(Image.open(o)) for o in sevens] # List comprehensions: e.g., new_list = [f(o) for o in a_list if o>0].
#three_tensors = [tensor(Image.open(o)) for o in threes] # taking an element from sevens as o and passing it to tensor(Image.open(o))
len(three_tensors),len(seven_tensors)

three_tensors[1]

three_tensors[6130]

show_image(three_tensors[1]); # We'll also check that one of the images looks okay.
# we need to use fastai's `show_image` function to display it, because it is a tensor (not a PIL image)

three_tensors

stacked_sevens = torch.stack(seven_tensors).float()/255 # stack up individual tensors in a collection into a single tensor.
stacked_threes = torch.stack(three_tensors).float()/255 # Generally when images are floats, the pixel values are expected to be between 0 and 1

type(three_tensors)

type(stacked_sevens)

stacked_threes.shape # 6,131 images, each of size 28×28 pixels.
# The first axis is the number of images, the second is the height, and the third is the width

len(stacked_threes.shape), stacked_threes.ndim #two ways to check the length of each axis
# rank is the number of axes or dimensions in a tensor; shape is the size of each axis of a tensor.

mean3 = stacked_threes.mean(0)
# the ideal 3; the mean of all the image tensors by taking the mean along dimension 0 of the stacked, rank-3 tensor
mean3.shape

show_image(mean3)

mean3

show_image(mean3)

mean7 = stacked_sevens.mean(0)
show_image(mean7);

a_3 = stacked_threes[10]
show_image(a_3);

type(a_3)

# Two different ways of measuring the distance between the a_3 and the ideal 3
dist_3_abs = (a_3 - mean3).abs().mean() # the mean absolute difference or L1 norm
dist_3_abs

dist_7_abs = (a_3 - mean7).abs().mean()
dist_7_abs

dist_3_sqr = ((a_3 - mean3)**2).mean().sqrt() # the root mean squared error (RMSE) or L2 norm.
dist_3_sqr

dist_7_sqr = ((a_3 - mean7)**2).mean().sqrt()
dist_7_sqr

# PyTorch provides both of these as loss functions in torch.nn.functional (imported as F by default under that name in fastai)
F.l1_loss(a_3.float(),mean7), F.mse_loss(a_3,mean7).sqrt()
# Here `mse` stands for mean squared error, and `l1` refers to mean absolute value
# the difference between L1 norm and mean squared error (MSE) is that the latter will penalize bigger mistakes more heavily than the former
# and be more lenient with small mistakes.

"""## Computing Metrics Using Broadcasting

https://numpy.org/doc/stable/user/basics.broadcasting.html

"""

len((path/'valid'/'3').ls())

len((path/'valid'/'7').ls())

# Let's calculate acurracy for validation set
valid_3_tens = torch.stack([tensor(Image.open(o)) for o in (path/'valid'/'3').ls()])
valid_3_tens = valid_3_tens.float()/255
valid_7_tens = torch.stack([tensor(Image.open(o)) for o in (path/'valid'/'7').ls()])
valid_7_tens = valid_7_tens.float()/255

valid_3_tens.shape

valid_7_tens.shape # 1,010 3s and 1,028 7s

def mnist_distance(a,b): return (a-b).abs().mean((-1,-2))
# We can write a simple function that calculates the mean absolute error using an expression very similar to the previous one
# Our function calls mean((-1,-2)). The tuple (-1,-2) represents a range of axes.
# In Python, -1 refers to the last element, and -2 refers to the second-to-last.
# So in this case, this tells PyTorch that we want to take the mean ranging over the values indexed by the last two axes of the tensor.
# The last two axes are the horizontal and vertical dimensions of the images.
# After taking the mean over the last two axes, we are left with just the first tensor axis, which indexes over our images

mnist_distance(a_3, mean3)

mnist_distance(valid_3_tens, mean3)
# in order to calculate a metric for overall accuracy, we will need to calculate the distance to the ideal 3 for every image in the validation set.
# PyTorch, when it tries to perform a simple subtraction operation between two tensors of different ranks, will use broadcasting.
# That is, it will automatically expand the tensor with the smaller rank to have the same size as the one with the larger rank.
# Broadcasting makes tensor code much easier to write.

valid_3_tens.shape

mean3.shape

valid_3_dist = mnist_distance(valid_3_tens, mean3)
valid_3_dist.shape
#It returned the distance for every single image as a vector (i.e., a rank-1 tensor) of length 1,010 (the number of 3s in our validation set).

tensor([1,2,3]) - tensor(1)  # broadcasting

mean3.shape, valid_3_tens.shape

(valid_3_tens-mean3).shape
# PyTorch doesn't actually copy mean3 1,010 times. It pretends it were a tensor of that shape, but doesn't actually allocate any additional memory
# It does the whole calculation in C (or, if you're using a GPU, in CUDA, the equivalent of C on the GPU), tens of thousands of times faster than pure Python (up to millions of times faster on a GPU!).

def is_3(x): return mnist_distance(x,mean3) < mnist_distance(x,mean7)

is_3(a_3), is_3(a_3).float()
#Note that when we convert the Boolean response to a float, we get 1.0 for True and 0.0 for False.

is_3(valid_3_tens) # Thanks to broadcasting, we can also test it on the full validation set of 3s:

~is_3(valid_3_tens)

show_images(valid_3_tens[(~is_3(valid_3_tens)).nonzero(as_tuple=True)[0]])

show_images(valid_7_tens[(is_3(valid_7_tens)).nonzero(as_tuple=True)[0]])

# we can calculate the accuracy for each of the 3s and 7s by taking the average of that function for all 3s and its inverse for all 7s:
is_3(valid_3_tens).float() .mean()

1-is_3(valid_7_tens).float().mean()

accuracy_3s =      is_3(valid_3_tens).float() .mean()

accuracy_7s = (1 - is_3(valid_7_tens).float()).mean()

accuracy_3s,accuracy_7s,(accuracy_3s+accuracy_7s)/2