import json
import datetime
import numpy as np
from pyspark.sql import SQLContext
from pyspark.sql import Row
from pyspark import SparkContext

#Get ASIN from user
def get_item():
	id = input("Recently viewed product code: ")
	return id

#Find item in dataframe from ASIN
def find_item(df, id):
	item_data = df.where(df.ASIN == id).limit(1).collect()
	item_dict = item_data[0].asDict()
	return item_dict

#Make dictionary of "Similar" items by ASIN code
def amazon_similar(item):
	amazon_weight = 5
	similar_items = {}
	for ASIN in item["similar"]:
		similar_items[ASIN] = amazon_weight
	return similar_items

#Return set of categories belonging to an item
def	get_categories(item):
	category_set = set()
	for row in item["categories"]:
		for category in row:
			category_set.add(category["ID"])
	return list(category_set)

#Return number of similar categories with provided set
def calc_similarity(item, cat_set):
	new_set = get_categories(item)
	return len(set(new_set) & set(cat_set))

#Add sufficiently similar items to the similar items dictionary
def category_similar(rdd, cat_set, items, group):
	min_similar = 6
	similar_rdd = rdd.filter(lambda x: x[2] > min_similar)
	all_similar = similar_rdd.map(lambda x: (x[0], x[2])).collect()
	for product in all_similar:
		new_id = product[0]
		similar = items.get(new_id, 0)
		new_similar = product[1]
		new_similar += similar
		items[new_id] = new_similar
	
#Return reccomended items sorted by most "Similar"
def sort_similar(items):
	reccomendations = sorted(items, key = items.get, reverse = True)
	return reccomendations
	
#Print top n most similar items
def print_n_best(reccomendations, n):
	print("Top " + str(n) + " reccomendations:")
	for i in range(n):
		print(reccomendations[i])

#Main function
if __name__ == "__main__":
	print(datetime.datetime.now())
	
	#Set up spark and read json into dataframe
	sc = SparkContext("local", "My App")
	SQLC = SQLContext(sc)
	df = SQLC.read.json("output.json")
	id_df = df.select("ASIN", "group", "categories")
	
	#Get Asin from user
	print("Input recent product ASIN")
	item_ASIN = get_item()
	#item_ASIN = "827229534"
	
	#Find item with given ASIN
	item = find_item(df, item_ASIN)
	
	#begin similar items list with Amazon's reccomended items
	similar_items = amazon_similar(item)
	
	#Compute categorical similarity
	category_set = get_categories(item)
	group = item["group"]
	group_df = id_df.where(df.group == group)
	similarity_rdd = group_df.rdd.map(lambda row: (row.ASIN, row.group, calc_similarity(row.asDict(), category_set)))
	category_similar(similarity_rdd, category_set, similar_items, group)
	
	#Organize and print top n results
	n = 10
	if(item_ASIN in similar_items): 
		similar_items.pop(item_ASIN)
	reccomendations = sort_similar(similar_items)
	print_n_best(reccomendations, n)
	
	print(datetime.datetime.now())