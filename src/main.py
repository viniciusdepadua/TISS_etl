import lxml
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')

    latest_tiss_url = soup.find('a', class_="alert-link internal-link").get('href')
    html_text = requests.get(latest_tiss_url, 'lxml').text

    soup = BeautifulSoup(html_text, 'lxml')
    tiss_pdf_candidates = soup.find_all('a', class_='btn')

    for candidate in tiss_pdf_candidates:
        if candidate.find_next('span').text == " documento referente ao Componente Organizacional.":
            tiss_pdf = candidate['href']
            break

    print(tiss_pdf)
    r = requests.get(tiss_pdf, stream=True)

    with open("../data/latest_tiss.pdf", "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            '''
            writing one chunk at a time to pdf file
            '''
            if chunk:
                pdf.write(chunk)