import json
import datetime

def process_amzn_text_to_json():
    review_data = [[()]]
    product_record = dict()
    
    # Erase contents of output file
    open("output.json", "w").close()
    
    with open("amazon-meta.txt", encoding="utf8") as f:
        for i in range(7):
            next(f)

        for line in f: 
            #print(line)
            line_content = line.split()
            
            if len(line_content) == 0:
                review_data.append(product_record)
                product_record.clear()
                continue
            elif line_content[0] == "id:":
                product_record["id"] = line_content[1]
            elif line_content[0] == "ASIN:":
                product_record["ASIN"] = line_content[1]
            elif line_content[0] == "title:":
                title = " ".join([line_content[i] for i in range(1, len(line_content))])
                product_record["title"] = title
            elif line_content[0] == "group:":
                #print(line_content)
                product_record["group"] = line_content[1]
            elif line_content[0] == "salesrank:":
                product_record["salesrank"] = int(line_content[1])
            elif line_content[0] == "similar:":
                similar = []
                for i in range(2, len(line_content)):
                    similar.append(line_content[i])
                product_record["similar"] = similar
            elif line_content[0] == "categories:":
                categories = []
                for i in range(int(line_content[1])):
                    #print(line_content)
                    debug_cat = next(f)
                    # print(debug_cat)
                    category_content = debug_cat.split("|")
                    category_content.pop(0)
                    descriptions = []
                    for d in category_content:
                        description_content = d.split("[")
                        description = dict()
                        description["Name"] = description_content[0]
                        description["ID"] = description_content[1].split("]")[0]
                        descriptions.append(description)
                    categories.append(descriptions)
                product_record["categories"] = categories
            elif line_content[0] == "reviews:":
                #print(line_content)
                reviews = dict()
                reviews["total"] = line_content[2]
                reviews["downloaded"] = line_content[4]
                reviews["avg rating"] = line_content[7]
                review_list = []
                for i in range(int(line_content[4])):
                    review_content = next(f).split()
                    #print(review_content)
                    review = dict()
                    review["date"] = review_content[0]
                    review["customer"] = review_content[2]
                    review["rating"] = review_content[4]
                    review["votes"] = review_content[6]
                    review["helpful"] = review_content[8]
                    review_list.append(review)
                reviews["review_list"] = review_list
                product_record["reviews"] = reviews
                with open("output.json", "a") as outfile:
                    json.dump(product_record, outfile)
                    outfile.write("\n")



if __name__ == "__main__":
    print(datetime.datetime.now())
    process_amzn_text_to_json()
    print(datetime.datetime.now())
