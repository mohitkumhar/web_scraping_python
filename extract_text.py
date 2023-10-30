import requests
import pandas as pd
from bs4 import BeautifulSoup
import os


file_path = 'Input.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)


for id, links in df.iterrows(): 
    url = links['URL']
    url_id = links['URL_ID']


    os.makedirs('extracted_text', exist_ok=True)
    
    path = f"extracted_text/{url_id}.html"

    


    def get_web_content(url, path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            
    get_web_content(url, path)
    
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            all_htmls = f.read()
            

                
        soup = BeautifulSoup(all_htmls, 'html.parser')
            
        title = soup.title.string if soup.title else "Title Not Found"


        print(f"Title of the Article is: {title}")

        content_element = soup.find(class_="td_block_wrap tdb_single_content tdi_130 td-pb-border-top td_block_template_1 td-post-content tagdiv-type")

        if content_element is None:
            content_element = soup.find(class_="td-post-content tagdiv-type")

        if content_element:
            all_content = content_element.get_text()
                
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'The Title of Article is: {title}\n\n\n')
            f.write(all_content)
                




        




