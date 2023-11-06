import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
import io
import xml.etree.ElementTree as ET
from tqdm import tqdm
import re

import os

folder_path = '/srv/storage/idmctal@storage1.nancy.grid5000.fr/2023/m2/adrelingyte/data_mining/blogs'

pattern = re.compile(r'(\d+)\.(\w+)\.(\d+)\.(\w+)\.(\w+)')

data = []
unicode_errors_list = []
parsing_errors_list = []

def replace_ampersand(text):
    # Replace & with &amp; if it's not already in the &amp; format
    return re.sub(r'&(?!amp;)', '&amp;', text)

file_list = [file for file in os.listdir(folder_path) if re.match(pattern, file)]

for file_name in tqdm(file_list, desc="Processing XML files"):

  match = re.match(pattern, file_name)

  try:
    number, gender, age, genre, zodiac = match.groups()
    xml_file_path = os.path.join(folder_path, file_name)
    with open(xml_file_path, 'r', encoding='utf-8') as file:
      xml_content = file.read()

    # Replace & with &amp; where necessary
    modified_xml_content = replace_ampersand(xml_content)
    tree = ET.ElementTree(ET.fromstring(modified_xml_content))
    root = tree.getroot()

    dates = [date.text for date in root.findall(".//date")]
    posts = [post.text for post in root.findall(".//post")]


    for date, post in zip(dates, posts):
        data.append({
          "Number": number,
          "Gender": gender,
          "Age": age,
          "Post Genre": genre,
          "Zodiac Sign": zodiac,
          "Date": date,
          "Post": post
        })

  except ET.ParseError:
      parsing_errors_list.append(xml_file_path)
      continue
  except UnicodeDecodeError as decode_error:
      unicode_errors_list.append(xml_file_path)
      continue




df = pd.DataFrame(data)
df


NON_ALPHANUM = re.compile(r'[\W]')
NON_ASCII = re.compile(r'[^a-z0-1\s]')
def normalize_texts(texts):
    normalized_texts = []
    for text in texts:
        lower = text.lower() 
        no_punctuation = NON_ALPHANUM.sub(r' ', lower)
        no_non_ascii = NON_ASCII.sub(r'', no_punctuation)
        normalized_texts.append(no_non_ascii)
    return normalized_texts


# Normalize the "Post" column and maintain the normalized texts as a list
# Apply the text normalization function to each row in the "Text" column

data_texts = normalize_texts(df['Post'])
print(data_texts[0:15])

