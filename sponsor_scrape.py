import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

filename_23 = "data/2023/cued_choice_2023.html"
filename_24 = "data/2024/cued_choice_2024.html"

with open(filename_23, "r", encoding="utf-8") as file:
    raw_html_23 = file.read()
with open(filename_24, "r", encoding="utf-8") as file:
    raw_html_24 = file.read()

def html_parser(html_content):
    company_info_list = []
    soup = BeautifulSoup(html_content, 'html.parser')
    target_attrs = {
        "target": "_blank"
    } 
    phone_pattern = re.compile(r'Tel:\s*([\d\s\-]+)')

    for row in soup.find_all('tr'):
        company_name = ""
        company_name_tag = row.find('a', attrs=target_attrs)
        if company_name_tag:
            company_name = company_name_tag.text.strip()

        email_address_tag = row.find('a', href=lambda href: href and href.startswith('mailto:'))
        email_address = email_address_tag['href'][7:] if email_address_tag else None


        person_name_tag = None
        if email_address_tag:
            parent_tr_tag = email_address_tag.find_parent('tr')
            if parent_tr_tag:
                td_tags = parent_tr_tag.find_all('td', recursive=False)
                if td_tags:
                    person_name_tag = td_tags[-3].text.strip()

        phone_number = None
        address_tag = row.find('address')
        if address_tag:
            text = address_tag.get_text() 
            phone_number_list = phone_pattern.findall(text)
            phone_number = phone_number_list[0]
            if len(phone_number) < 4:
                phone_number = None

        company_info_list.append([company_name, person_name_tag, email_address, phone_number])

    return company_info_list

def remove_duplicate_companies(lst_of_lsts):
    processed_words = set()
    result = []

    for lst in lst_of_lsts:
        string = lst[0]
        if not string.isspace() and len(string.split()) > 0:
            first_word = string.split()[0]
            if first_word not in processed_words:
                processed_words.add(first_word)
                result.append(lst)

    return result

# Read other databases that are excel files into list of lists
def read_from_excel(file_name):
    return pd.read_excel(file_name, header=None).fillna('').values.tolist()

def save_to_excel(data, file_name, dir_path):
    xlsx_path = os.path.join(dir_path, file_name)
    df = pd.DataFrame(data)
    df.to_excel(xlsx_path, index=False, header=False)

# Create global list of company information
company_info_list = html_parser(raw_html_23)
company_info_list = html_parser(raw_html_24)
company_info_list += read_from_excel("data/other_databases/2021_company_list.xlsx")
company_info_list += read_from_excel("data/other_databases/old_sponsor_team_list.xlsx")
company_info_list += read_from_excel("data/other_databases/events_team_list.xlsx")

# Remove companies with no email address
edited_company_info_list = []

for lst in company_info_list:
    # If email is present and not empty
    if lst[2] is not None and lst[2] != "":
        edited_company_info_list.append(lst)

# Remove duplicate companies
final_company_info_list = remove_duplicate_companies(edited_company_info_list)

dir_path = os.getcwd()
save_to_excel(final_company_info_list, "company_info_database_2024.xlsx", dir_path)
print(f"Number of companies found: {len(final_company_info_list)}")