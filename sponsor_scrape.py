import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

with open("london.html", "r", encoding="utf-8") as html_file:
    london_html = html_file.read()
with open("bedfordshire.html", "r", encoding="utf-8") as html_file:
    bedfordshire_html = html_file.read()
with open("berkshire.html", "r", encoding="utf-8") as html_file:
    berkshire_html = html_file.read()
with open("cambridgeshire.html", "r", encoding="utf-8") as html_file:
    cambirdgeshire_html = html_file.read()
with open("derbyshire.html", "r", encoding="utf-8") as html_file:
    derbyshire_html = html_file.read()
with open("gloucs.html", "r", encoding="utf-8") as html_file:
    gloucs_html = html_file.read()
with open("hampshire.html", "r", encoding="utf-8") as html_file:
    hampshire_html = html_file.read()
with open("kent.html", "r", encoding="utf-8") as html_file:
    kent_html = html_file.read()
with open("lancs.html", "r", encoding="utf-8") as html_file:
    lancs_html = html_file.read()
with open("northumberland.html", "r", encoding="utf-8") as html_file:
    northumberland_html = html_file.read()
with open("uk_orgs.html", "r", encoding="utf-8") as html_file:
    uk_orgs_html = html_file.read()

def company_parser(html_content, plain_texts):
    soup = BeautifulSoup(html_content, 'html.parser')
    target_attrs = {
        "target": "_blank",
        "target": "_new"
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

sponsor_list = []
company_parser(london_html, sponsor_list)
company_parser(bedfordshire_html, sponsor_list)
company_parser(berkshire_html, sponsor_list)
company_parser(cambirdgeshire_html, sponsor_list)
company_parser(derbyshire_html, sponsor_list)
company_parser(gloucs_html, sponsor_list)
company_parser(hampshire_html, sponsor_list)
company_parser(kent_html, sponsor_list)
company_parser(lancs_html, sponsor_list)
company_parser(northumberland_html, sponsor_list)
company_parser(uk_orgs_html, sponsor_list)

sponsor_list = remove_strings_with_same_start(sponsor_list)

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