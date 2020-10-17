import json


def process_amzn_text_to_json():
    review_data = [[()]]
    product_record = dict()

    with open("amazon-meta.txt") as f:
        for i in range(7):
            next(f)

        for line in f: 
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
                product_record["group"] = line_content[1]
            elif line_content[0] == "salesrank:":
                product_record["salesrank"] = int(line_content[1])
            elif line_content[0] == "similar:":
                similar = []
                for i in range(2, len(line_content)):
                    similar.append(line_content[i])
                product_record["similar"] = similar
            elif line_content[0] == "categories:":
                categories = [[]]
                for i in range(int(line_content[1])):
                    category_content = next(f).split("|")
                    category_content.pop(0)
                    descriptions = []
                    for d in category_content:
                        description_content = d.split("[")
                        description = dict()
                        description["Name"] = description_content[0]
                        description["ID"] = description_content[1]
                        descriptions.append(description)
                    categories.append(descriptions)
                product_record["categories"] = categories
                # product_json = json.dumps(product_record) #Dictionary to JSON
                # print(product_json) #Print JSON
            elif line_content[0] == "reviews:":
                # Process reviews
                
    #review_data = {"review_data": review_data}
    #return json.dumps(review_data)



if __name__ == "__main__":
    process_amzn_text_to_json()
