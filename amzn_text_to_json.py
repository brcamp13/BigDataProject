import json


def process_amzn_text_to_json():
    review_data = []
    with open("amazon-meta.txt") as f:
        for i in xrange(7):
            next(f)

        for line in f: 
            product_record = dict()
            line_content = line.split()
            
            if len(len_content) == 0:
                review_data.append(product_record)
                continue
            elif line_content[0] == "id:":
                # Process id
            elif line_content[0] == "ASIN:":
                # Process asin
            elif line_content[0] == "title:":
                # Process title
            elif line_content[0] == "group:":
                # Process group
            elif line_content[0] == "salesrank:":
                # Process salesrank
            elif line_content[0] == "similar:":
                # Process similar
            elif line_content[0] == "categories:":
                # Process categories
            elif line_content[0] == "reviews:":
                # Process reviews


    review_data = {"review_data": review_data}
    return json.dumps(review_data)



if __name__ == "__main__":
    process_amzn_text_to_json()
