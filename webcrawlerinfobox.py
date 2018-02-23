import urllib2
import re
from bs4 import BeautifulSoup
from unidecode import unidecode



def find_info(quote_page,focus_word_list):
    # query the website and return the html to the variable page
    page = urllib2.urlopen(quote_page)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, "html.parser")

    # find the info-box contents
    info_box = soup.find("table", attrs={"class": re.compile("^infobox")})

    # clean the input string
    def clean_string(given_string):
        final_string = re.sub("\n\n*" , ", " , unidecode(given_string.strip()))
        final_string = re.sub('[*/\[0-9]]', '', final_string)
        return final_string
    
    # create a dictionary of the the info contents
    final_list = [{clean_string(tr.find("th").text): clean_string(td.text) for td in tr.findAll("td")} for tr in info_box.findAll('tr') if tr.find("th") is not None]
    output_list = []
    for each_word in focus_word_list:
        for each_dict in final_list:
            if each_word in each_dict.keys():
                output_list.append(each_dict.values())
    if output_list:
        return output_list
    else:
        return quote_page
        
    
        
    

print(find_info("https://en.wikipedia.org/wiki/India",["Capital","Internet TLD"]))




