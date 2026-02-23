# importing all the required modules
import pypdf
import os
from os import listdir
from os.path import isfile, join
import re
path = os.path.dirname(os.path.abspath(__file__))+'\\Faturas\\'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)
# creating a pdf reader object
reader = pypdf.PdfReader(path+onlyfiles[0])

# print the number of pages in pdf file
print(len(reader.pages))

# print the text of the first page
print(reader.pages[5].extract_text())
print(re.split('((?:\n)[0-3][0-9] [A-Z]{3}\n)',reader.pages[9].extract_text()))
