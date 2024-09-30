import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "AIzaSyCXM50Jhl3hk7FjRaJR8VX_YsjgxoY4wXY"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel(model_name='gemini-1.5-pro', tools='code_execution')

def read_input():
   link = {"1":["BookToScrape","https://books.toscrape.com/"]}
   
   for i in range(1,3):
       url = link[str(i)][1]
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'html.parser')
       data = soup.text
       links = soup.find_all('a', href=True)
       urls = ""
       for a in links:
           urls = urls +"\n"+ a['href'][1:]

       query = data + "Jumbled links about book categories:"+urls+"\n Create a table with the following columns: Book category and Category link\n And append this url without space for every books category links: 'https://books.toscrape.com/'"
       main_response = model.generate_content(query)
       print(main_response.text)
       
    #    query = data + "Jumbled links about book categories:"+urls+"\n Create a table with the following columns: Book category and Category link\n And append this url without space for every books category links: 'https://books.toscrape.com/'\n And after this process ends, I need the output in csv file without index. So you need to write the python code and save the code in a python script and run that python file with this command in your terminal/code executor: python {script_file.py}"
    #    main_response = model.generate_content(query)
    #    print(main_response.text)
       
read_input()