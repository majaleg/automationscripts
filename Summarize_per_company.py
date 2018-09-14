# Lego
#
# QUICKFIX
#
# This script takes in .csv files with ";"(semicolon) as delimiter, which is standard in excel.
# Row 1 is company/customer, and row 2 is class,
# and returns the number of different servers and clients for each customer. 
# 
# Note that this can be changed further down, see comments.
#
# PS: If index out of range error is received, check the delimiters of the .csv in a text editor.
#

import csv

#Removes duplicate customers in a given list "values" and returns them in a list "output"
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

#get all unique customers and returns them in a list
def get_customers(csv_file):
    all_customers = []
    for row in csv_file:
        all_customers.append(row[1])
    customers = remove_duplicates(all_customers)
    return customers

#Finds the number of a given type of item for the given customer and returns the number
def get_customer_item_num(customer, item_type, csv_file_name):
    #get csv (must be done several times to not exhaust the reader)
    csv_file = get_csv(csv_file_name)
    num_of_items = 0
    for row in csv_file:
        row_customer = row[1]
        row_type = row[2].lower()
        if item_type in row_type:
            if row_customer == customer:
                num_of_items += 1
    return num_of_items

#Find the number of servers for each customer and returns them in a dictionary
#structure: {customer:number of item}
def get_all_customer_item_num(customer_list, item_type, csv_file_name):
    #get csv (must be done several times to not exhaust the reader)
    csv_file = get_csv(csv_file_name)
    customer_item_dict = {}
    for customer in customer_list:
        item_num = get_customer_item_num(customer, item_type, csv_file_name)
        customer_item_dict.update({customer:item_num})
    return customer_item_dict

#imports the needed csv based on user input
def get_csv(csv_file_name):
    f = open(csv_file_name)
    csv_file = csv.reader(f, delimiter = ";")
    return csv_file

#Merges two dictionaries given as input and returns one dictionary
#Format:    dict1 = {"company":number1}
#           dict2 = {"company":number2}
#           merged_dict = {"company":(number1, number2)}
def merge_dictionaries(dict1, dict2):
    both_dict = [dict1, dict2]
    merged_dict = {}
    for key in dict1.iterkeys():
        merged_dict[key] = tuple(merged_dict[key] for merged_dict in both_dict)
    return merged_dict

#lazy conversion
def dict_to_csv(dictionary):
    headers = "Company, Servers, Computers \n"
    #here comes the lazy part
    dict_string = headers
    dict_string += str(dictionary)
    dict_string = dict_string.replace("{", "")
    dict_string = dict_string.replace("}", "")
    dict_string = dict_string.replace(":", ";")
    dict_string = dict_string.replace(",", ";")
    dict_string = dict_string.replace("(", "")
    dict_string = dict_string.replace(")", "\n")
    dict_string = dict_string.replace("'", "")
    dict_string = dict_string.replace("\n, ","\n")
    dict_string = dict_string.split("\n")
    return dict_string

#save string in csv file
def save_as_csv(csv_strings):
    output_file = raw_input("Name output file: (Note that this script will NOT overwrite excisting files for security reasons):")
    output_file += ".csv"
    output = open(output_file, "wb")
    writer = csv.writer(output, dialect = "excel")
    for string in csv_strings:
        writer.writerow([string])
    print ("File " + output_file + " successfulle created.")




def __INIT():
    #import file
    csv_file_name = raw_input("csv file:")
    #csv_file_name = "ALL_computer_RAW.csv" #debug
    csv_file = get_csv(csv_file_name)
                       
    #get non-duped customer list
    customer_list = get_customers(csv_file)

    #get servers
    customer_server_dict = get_all_customer_item_num(customer_list, "server", csv_file_name)

    #get computers
    customer_client_dict = get_all_customer_item_num(customer_list, "computer", csv_file_name)

    #merge servers and computers
    merged_dict = merge_dictionaries(customer_server_dict, customer_client_dict)

    #convert dict to csv
    csv_string = dict_to_csv(merged_dict)
    
    #save results
    save_as_csv(csv_string)
    
    


__INIT()


