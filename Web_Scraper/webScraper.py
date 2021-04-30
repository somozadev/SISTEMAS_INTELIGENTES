from nltk.util import pr
import requests
from bs4 import BeautifulSoup


def WebScrap(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    soupList = list(soup.children)
    # print(soupList)
    html = Html(soupList)
    Title(html)
    Body(html)
    FindPTag(soup)
    


def WebScrapWithClasses(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print("cursivas: " ,CursivaClass(soup))
    print("azul: " ,CursivaClassAzul(soup))
    print("id: ", Id(soup,'parrafo1'))


def CursivaClass(soup):
    cursivas = soup.find_all('p', class_='cursiva')
    return cursivas

def CursivaClassAzul(soup):
    azul = soup.find_all('p', class_='azul')
    return azul
def Id(soup, id):
    parrafo = soup.find_all('p', id=id)
    return parrafo

def Html(soupList):
    html = list(soupList[2])
    print("HTML" + "\n")
    print(html)
    print("\n")
    return html


def Body(html):
    body = list(html[3].children)
    pOne = body[1].get_text()
    pTwo = body[3].get_text()

    print("P1: " + pOne + "\n P2: " + pTwo)


def FindPTag(soup):
    p = soup.find_all('p')
    # con soup.find('p') devolvería la primera

    print("Search by tag: ", p)


def Title(html):
    head = list(html[1].children)
    title = head[1]
    print(title.get_text())
    print("\n")


class main():
    # WebScrap('http://esp.uem.es/ssii/holaMundo.html')
    WebScrapWithClasses('http://esp.uem.es/ssii/holaMundo2.html')
