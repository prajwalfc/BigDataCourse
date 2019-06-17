#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import csv
from countminsketch1 import CountMinSketch


# In[2]: Setup the strean and some variables.


item_set = set()
currentCustomer=''
# CountMinSketch with 20 hashes to try to prevent hash collision so that every product gets unique identity. As many hashes used, the more accurate is the result. So
# maybe for biger data sets we need to increase the second argument of the CountMinSketch.
# two CountMinSketch instances one for item count and one for total revenue
# since productId is hashed and cannot be reverted back we need to store the products in item_set set data structure (doesn't contain duplicates)
# while retrieving the counts and revenue we need to hash the strings stoted in item_set since same string is supposed to output the same hash.
itemCount = CountMinSketch(10,20)
itemRevenue = CountMinSketch(10,20)
def salesRead(filename):
    with open(filename, 'r') as fi:
        reader = csv.DictReader(fi)
        for row in reader:
            yield(row)


# In[3]: Now get the stream of data and process it


input_file = sys.argv[1]
out_file = sys.argv[2]
individual_cart = set()
for hod in salesRead(input_file):  
    product_id = hod['Product ID']
    customer_id = hod['Customer ID']
    item_cost = hod['Item Cost']
    itemRevenue.put(product_id,float(item_cost))
    if(currentCustomer != customer_id):
        individual_cart = set()
    elif (product_id in individual_cart):
        continue
    individual_cart.add(product_id)
    item_set.add(product_id)
    itemCount.put(product_id,1)
    currentCustomer = customer_id
    


# In[4]: Now Write the stream data to file


header = [['Product ID','Customer Count','Total Revenue']]
with open(out_file, 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(header)
    for item in item_set:
        line =[[]]
        line=[[item,itemCount.get(item),round(itemRevenue.get(item),2)]]
        writer.writerows(line)
writeFile.close()


# In[ ]:




























