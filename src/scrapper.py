import requests
from bs4 import BeautifulSoup


class TISScrapper:
    def __init__(self):
        self.url = 'https://www.gov.br/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude' \
                   '-suplementar-2013-tiss'

    def getPdfUrl(self):
        latest_tiss_url = self.getTissUrl()

        html_text = requests.get(latest_tiss_url, 'lxml').text

        soup = BeautifulSoup(html_text, 'lxml')
        tiss_pdf_candidates = soup.find_all('a', class_='btn')

        for candidate in tiss_pdf_candidates:
            if candidate.find_next('span').text == " documento referente ao Componente Organizacional.":
                tiss_pdf_url = candidate['href']
                break

        return tiss_pdf_url

    def getPdf(self):
        pdf_url = self.getPdfUrl()
        self.downloadPdf(pdf_url)

    def downloadPdf(self, pdf_url):
        r = requests.get(pdf_url, stream=True)

        with open("../data/latest_tiss.pdf", "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                '''
                writing one chunk at a time to pdf file
                '''
                if chunk:
                    pdf.write(chunk)

    def getTissUrl(self):
        html_text = requests.get(self.url).text
        soup = BeautifulSoup(html_text, 'lxml')
        latest_tiss_url = soup.find('a', class_="alert-link internal-link").get('href')

        return latest_tiss_url
