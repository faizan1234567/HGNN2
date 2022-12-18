# import all the necceary packages to work with dataset split and division
import pandas as pd             # library to read and manipulate dataset
import numpy as np              # libarary for scientific computing
import matplotlib.pyplot as plt # library to visualize data, plots
import os                       # operating system library
import argparse
from sklearn.utils import shuffle

def read_args():
    '''read command line args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_csv', type =str, help=" data csv file path")
    parser.add_argument('--time_stamp', type = int, help= "to divide data into time stamp")
    return parser.parse_args()

def divide(df, indices):
  '''divide the dataset into various parts
  args:
  df: a randomly shuffled dataframe
  indices: a list of indices, add one to indices for correct calculations
  return dataframes
  '''
  my_dfs = {}
  for i in range(len(indices) -1):
    var_name = "df%d" % i
    my_dfs[var_name] = df[indices[i]: indices[i+1]]
  return my_dfs


def divide_data(df, time_stamp):
  '''take input dataframe, and divide it into specified number of parts
  and include dropped data into the last batch, then return divided
  Args:
  df: dataframe, mainly nodes edges 
  time_stamp: divide the data into number of time stamp
  Return
  return number of time stamp dataframes of data formed in batches'''
  #randomly shuffle dataset frame
  shuffled_df = shuffle(df)
  count_rows = shuffled_df.shape[0] # number of rows
  count_cols = shuffled_df.shape[1] # number of columns
  split_size = int(count_rows/time_stamp) 
  dropped_data = count_rows - split_size * time_stamp
  index = 0
  indices = []
  indices.append(index)
  while index <= count_rows:
    index+= split_size
    if index < count_rows and count_rows - index != dropped_data:
      indices.append(index)
    elif index + dropped_data == count_rows:
      indices.append(index + dropped_data)
      break
    else:
      break
  divided_dfs = divide(shuffled_df, indices)
  print(f'length of indices: {len(indices)}')
  print(f'indices list: {indices}')
  return divided_dfs

def main():
    '''all the funs goes here'''
    args = read_args()
    if args.data_csv:
        edges = pd.read_csv(args.data_csv)
    if args.data_csv and args.time_stamp:
        divided_data = divide_data(edges, args.time_stamp)
    return divided_data

if __name__ == '__main__':
    splitted_data = main()
    print(f'first element of the data: {splitted_data["df0"]}')
    print('divided dataset!!!')
    print('Finished!!!')
    