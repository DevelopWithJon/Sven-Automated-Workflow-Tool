def parse(data):
    parsed_dict = {}
    parsed_dict[state] = data["State"]
    parsed_dict[city] = data["City"]
    parsed_dict[customer_Name] = data["Customer_Name"]
    parsed_dict[company] = data["Company"]
    parsed_dict[product] = data["Product"]["Brand Name"]
    parsed_dict[price] = data["Product"]["Price"]
    parsed_dict[units] = data["Product"]["Price"]
    parsed_dict[latitude] = data["coordinates"][0]
    parsed_dict[langitude] = data["coordinates"][1]
    return parsed_dict
