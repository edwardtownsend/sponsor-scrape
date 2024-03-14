import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

with open("cued_choice.html", "r", encoding="utf-8") as html_file:
    cued_html = html_file.read()

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
        if not string.isspace() and len(string.split()) > 0:
            first_word = string.split()[0]
            if first_word not in processed_words:
                processed_words.add(first_word)
                result.append(lst)

    return result

def read_from_excel(file_name):
    return pd.read_excel(file_name, header=None).fillna('').values.tolist()

sponsor_list = []
company_parser(cued_html, sponsor_list)
sponsor_list += read_from_excel("2021_company_list.xlsx")
sponsor_list += read_from_excel("old_sponsor_list.xlsx")

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


def save_to_excel(data, file_name, dir_path):
    xlsx_path = os.path.join(dir_path, file_name)
    df = pd.DataFrame(data)
    df.to_excel(xlsx_path, index=False, header=False)

dir_path = os.getcwd()
save_to_excel(company_email, "companies_emails.xlsx", dir_path)
save_to_excel(company_name_email, "companies_names_emails.xlsx", dir_path)

print(len(f"Number of companies with neither contact name or email: {company}"))
print(len(f"Number of companies with only email: {company_email}"))
print(len(f"Number of companies with contact name and email: {company_name_email}"))