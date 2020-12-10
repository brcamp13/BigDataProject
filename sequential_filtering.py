import json
import datetime

#Get ASIN from user
def get_item():
	id = input("Product code: ")
	return id

#Find item in json data from given ASIN, return it as dictionary
def find_item(data, id):
	for line in data:
		if(line.strip()):
			line_content = line.split()
			#print((line_content[1].split("\""))[1])
			if(line_content[1].split("\"")[1] == id):
				return json.loads(line)

#Make dictionary of "Similar" items by ASIN code
def amazon_similar(item):
	similar_items = {}
	for ASIN in item["similar"]:
		similar_items[ASIN] = 5
	return similar_items

#Not used, will delete for final version
def find_similar(data, items):
	similar_data = []
	for ASIN in items:
		new_item = find_item(data, ASIN)
		similar_data.append(new_item)
	return similar_data

#Not used, will delete for final version	
def update_value(similar_items, similar_data):
	for product in similar_data:
		print(product)
		new_value = similar_items.get(product["ASIN"], 0.0)
		new_value += float(product["reviews"]["avg rating"])
		similar_items[product["ASIN"]] = new_value

#Not used, will delete for final version
def update_list(similar_items, similar_data):
	for product in similar_data:
		for similar_item in product["similar"]:
			if not similar_items.has_key(similar_item):
				similar_items[similar_item] = 0

#Return set of categories belonging to an item
def	get_categories(item):
	category_set = set()
	for row in item["categories"]:
		for category in row:
			category_set.add(category["ID"])
	return category_set

#Calculate similarity with main item based on shared categories
def category_similar(data, cat_set, items, group):
	min_similar = 6
	for line in data:
		if(line.strip()):
			line_content = line.split("group\": \"")[1]
			if (line_content.split("\"")[0] == group):
				new_set = set()
				product = json.loads(line)
				for row in product["categories"]:
					for category in row:
						new_set.add(category["ID"])
				similar = len(new_set.intersection(cat_set)) 
				if(similar > min_similar):
					#print(new_set.intersection(cat_set))
					new_id = product["ASIN"]
					new_similar = items.get(new_id, 0)
					new_similar += similar
					items[new_id] = new_similar
					#print(items)
				new_set.clear()
				
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
	print("Input recent product ASIN: ")
	item_ASIN = get_item()
	#item_ASIN = "0827229534"
	#item_ASIN = "1559351659"
	print(datetime.datetime.now())
	json_data = open("output.json", "r")
	item = find_item(json_data, item_ASIN)
	similar_items = amazon_similar(item)
	group = item["group"]
	category_set = get_categories(item)
	category_similar(json_data, category_set, similar_items, group)
	if(item_ASIN in similar_items): 
		similar_items.pop(item_ASIN)
	reccomendations = sort_similar(similar_items)
	print_n_best(reccomendations, 10)
	print(datetime.datetime.now())