import requests
from bs4 import BeautifulSoup
import bibtexparser


#def get_reference_link(id: str):
#    url = "https://complexityzoo.net/Complexity_Zoo_References"
#    id = id.replace("[", "").replace("]","").lower()
#
#    response = requests.get(url)
#
#    if (response.status_code != 200):
#        return ["Failed to fetch information, Status:" + str(response.status_code)]
#    
#
#    soup = BeautifulSoup(response.text, 'html.parser')
#
#    reference_information = soup.find('span', {'id': id})
#
#    print(reference_information.findParent())


#get_reference_link("[Aar02]")

#def get_class_info(class_name: str):
#
#    #Example url for NP: https://complexityzoo.net/Complexity_Zoo:N
#
#    #Get the webpage for all classes beginning with this letter
#    first_letter = class_name[0].upper()
#    url = f"https://complexityzoo.net/Complexity_Zoo:{first_letter}"
#
#    response = requests.get(url)
#
#    if (response.status_code != 200):
#        return ["Failed to fetch information, Status:" + str(response.status_code)]
#
#    soup = BeautifulSoup(response.text, 'html.parser')
#    
#
#    #Find the span element with the id of the name
#    #All the next paragraph elements will be information about this class. The next class' information is delimited by an h5 element
#    information_span = soup.find('span', {'id': f"{class_name.lower()}"})
#
#    output_list = []
#
#    #Get all paragraph elements until you read an h5, which is the next class
#
#    #for element in information_span.find_all_next():
#    #    if element.name == "p":
#    #        output_list.append(element.text)
#    #    elif element.name == "h5":
#    #        break
#    #    else:
#    #        #Todo: parse hyperlink a element
#    #        pass
#
#
#    for element in information_span.find_all_next():
#        if element.name == "h5":
#            break
#        else:
#            print(element.name)
#
#    return output_list



#def get_all_references():
#    url = "https://complexityzoo.net/Complexity_Zoo_References"
#    response = requests.get(url)
#
#    if (response.status_code != 200):
#        return ["Failed to fetch information, Status:" + str(response.status_code)]
#    
#
#    soup = BeautifulSoup(response.text, 'html.parser')
#
#    reference_information = soup.find('div', {'id': "mw-parser-output"})

    
#bibtex_str = """
#@comment{
#    Example Comment
#}
#@ARTICLE{Cesar2013,
#    author = {Jean Cesar},
#    title = {An amazing title},
#    year = {2013},
#    volume = {12},
#    pages = {12--23},
#    journal = {Nice Journal}
#}
#"""

#library = bibtexparser.parse_string(bibtex_str)
#print(library.comments[0].comment) #The comment
#first_entry = library.entries[0]
#print(first_entry.fields_dict)

#url = f"http://dx.doi.org/10.4086/toc.2005.v001a001"

try:
    headers = {"accept":"application/x-bibtex"}
    response = requests.get("http://dx.doi.org/10.1145/800157.805047", headers=headers)
    print(response.text)
except:
    print("error")

