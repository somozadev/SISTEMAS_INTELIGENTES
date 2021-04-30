import requests
from bs4 import BeautifulSoup


def WebScrap(url, laboratorio):
    # for custom request by the user (laboratory name in this case)
    payload = {
        'lab': laboratorio
    }

    page = requests.get(url, params=payload)

    soup = BeautifulSoup(page.content, 'html.parser')
    # gets the section with id product and looks for the class container inside
    html = soup.find('section', id='product').find('div', class_='container')

    # gets the text
    result = html.get_text()
    # cleans out empty spaces
    result = result.replace(' ', '')
    result = result.replace('\n', '')
    # converts to array and pops out the first element, which is the title of the page and not the programs

    arr = result.split()
    arr.pop(0)
    # joins back the array with \n separation
    output = '\n'.join(arr)

    # saves it in current path for easy comprobation and prints it out in console
    with open('index.html', 'w') as f:
        f.write(output)

    print(output)

class main():
    WebScrap('http://esp.uem.es/digitalAED/laboratorios.php', input("Escriba el laboratorio: "))
