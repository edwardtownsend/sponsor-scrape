import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

with open("cued_choice.html", "r", encoding="utf-8") as html_file:
    london_html = html_file.read()

def company_parser(html_content, plain_texts):
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

        plain_texts.append([company_name, person_name_tag, email_address, phone_number])

def remove_strings_with_same_start(lst_of_lsts):
    processed_words = set()
    result = []

    for lst in lst_of_lsts:
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

sponsor_list = []
company_parser(london_html, sponsor_list)
df = pd.read_excel('old_sponsor_list.xlsx', header=None)
rows_list = df.where(pd.notna(df), None).values.tolist()
sponsor_list = sponsor_list + rows_list
sponsor_list = remove_strings_with_same_start(sponsor_list)
print(len(sponsor_list))

company_name_email = []
company_email = []
company = []

for lst in sponsor_list:
    if lst[2] != None:
        if lst[1] != "":
            company_name_email.append(lst)
        else:
            company_email.append(lst)
    else:
        company.append(lst)

dir_path = os.getcwd()

xlsx_path_1 = os.path.join(dir_path, "companies.xlsx")
df1 = pd.DataFrame(company)
df1.to_excel(xlsx_path_1, index=False, header=False)

xlsx_path_2 = os.path.join(dir_path, "companies_emails.xlsx")
df2 = pd.DataFrame(company_email)
df2.to_excel(xlsx_path_2, index=False, header=False)

xlsx_path_3 = os.path.join(dir_path, "companies_names_emails.xlsx")
df3 = pd.DataFrame(company_name_email)
df3.to_excel(xlsx_path_3, index=False, header=False)

print(len(company))
print(len(company_email))
print(len(company_name_email))