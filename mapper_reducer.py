# -*- coding: utf-8 -*-
"""Mapper-Reducer.ipynb

Automatically generated by Colaboratory.

# Mapper-Reducer code for counting frequency of words in a text file.
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/Shared drives/IDS 561: Big Data Analytics/HW1/

"""Reading the text file from drive."""

with open('hw1.txt', "r") as f: 
    for line in f:
        cleanedLine = line.strip()
        if cleanedLine: # is not empty
            print(cleanedLine)
f.close()

"""Reading the file into a dataframe."""

import pandas as pd
df = pd.read_fwf('hw1.txt',header = None)
# print(df[:10])

"""Data Cleaning Function"""

def data_clean(df):
  df["new_column"] = df[0].str.replace('[^\w\s]','')
  df["new_column"] = df["new_column"].str.replace('[\d+]','')
  df.new_column = df.new_column.str.replace('_', ' ')
  df['new_column'] = df['new_column'].str.lower() 
  df.drop(columns=[0],inplace=True)

data_clean(df)

"""Converting dataframe into a list."""

df_list = [i for i in df.values.tolist()]

len(df_list)

"""Data Split Function"""

def data_split(ls):
  return ls[:5000],ls[5000:]

part1 = data_split(df_list)[0]
part2 = data_split(df_list)[1]

"""Mapper function"""

def mapper(cleaned_lines):
  ls=[] 
  for line in cleaned_lines:
    word_list = line[0].split()
    for j in word_list:
      ls.append((j,1))
  return ls

map_part1 = mapper(part1)
map_part2 = mapper(part2)

len(map_part1)

len(map_part2)

"""Sort Function"""

def sort_words(one, two):
  
  return sorted(one+two)

Sorted = sort_words(map_part1, map_part2)

print(Sorted[:10])

len(Sorted)

"""Partition Function"""

def partition(ls,char='m'):
    m_idx = [i for i in range(len(ls)) if  list(ls[i][0])[0]==char]
    return {'partition_1':ls[:max(m_idx)+1],'partition_2':ls[max(m_idx)+1:]}

Part1 = partition(Sorted)['partition_1']
Part2 = partition(Sorted)['partition_2']

print(Part1)
print(Part2)

"""Reducer Function"""

from collections import Counter
def reducer(ls):
    return Counter([word[0] for word in ls])

reduced_1 = reducer(Part1)
reduced_2 = reducer(Part2)

"""Main Function"""

def main(reduced_1,reduced_2):
    reduced_1.update(reduced_2)
    return reduced_1

output = main(reduced_1,reduced_2)

"""Output of reducer stored in CSV format in alphabetical order."""

list_tuples = [(word,freq) for word,freq in output.items()]
pd.DataFrame(list_tuples,columns=['Words','Frequency']).sort_values(by='Words').to_csv('Output.csv')

"""The end."""
