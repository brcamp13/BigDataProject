import json


def process_amzn_text_to_json():
    review_data = []
    with open("amazon-meta.txt") as f:
        # Start at line with first ID: 
        # Once you've found this line, next line is ASIN
        # Next line is title
        # Group
        # Salesrank
        # Similar
        # Categories. If > 0, each following line will have some information
        # Reviews. If > 0, each following line will have some information
        # Newline
        # Start of new entry
        # Repeat everything above
        for line in f:
            # Do all of the pseudocode above
            print("Putting stuff here to remove error below.")
            print(line)

    review_data = {"review_data": review_data}
    return json.dumps(review_data)


if __name__ == "__main__":
    process_amzn_text_to_json()
