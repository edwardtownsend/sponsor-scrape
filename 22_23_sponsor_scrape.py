import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import math

def remove_strings_with_same_start(list_of_lists):
    processed_words = set()
    result = []

    for lst in list_of_lists:
        string = lst[0]
        # Check if the string contains more than one word
        if not string.isspace() and len(string.split()) > 0:
            # Get the first word of the string
            first_word = string.split()[0]

            # Check if the first word has already been processed
            if first_word not in processed_words:
                # If not processed, add the first word to the set and include the string in the result
                processed_words.add(first_word)
                result.append(lst)

    return result

dir_path = os.getcwd()
xlsx_path = os.path.join(dir_path, "2022_sponsor_list.xlsx")

df = pd.read_excel(xlsx_path)
column_1 = df.iloc[:,0].to_list()
column_2 = df.iloc[:,1].to_list()
column_3 = df.iloc[:,2].to_list()

sponsor_list_of_lists =[]

for i in range(len(column_3)):
    sponsor_list_of_lists.append([column_1[i], column_2[i], column_3[i]])

clean_sponsor_list_of_lists = remove_strings_with_same_start(sponsor_list_of_lists)

print(clean_sponsor_list_of_lists)
print(323+276+399)

company_name_email = []
company_email = []
company = []
for lst in clean_sponsor_list_of_lists:
    if isinstance(lst[2], str):
        if isinstance(lst[1], str):
            company_name_email.append(lst)
        else:
            company_email.append(lst)
    else:
        company.append(lst)

xlsx_path_1 = os.path.join(dir_path, "companies.xlsx")
xlsx_path_2 = os.path.join(dir_path, "companies_emails.xlsx")
xlsx_path_3 = os.path.join(dir_path, "companies_names_emails.xlsx")
df1 = pd.DataFrame(company)
df1.to_excel(xlsx_path_1, index=False, header=False)
df2 = pd.DataFrame(company_email)
df2.to_excel(xlsx_path_2, index=False, header=False)
df3 = pd.DataFrame(company_name_email)
df3.to_excel(xlsx_path_3, index=False, header=False)

print(len(company))
print(len(company_email))
print(len(company_name_email))
