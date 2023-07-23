import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    url = 'https://search.folha.uol.com.br/search?q=Seguran%C3%A7a+da+Informa%C3%A7%C3%A3o&periodo=personalizado&sd=01%2F01%2F2018&ed=31%2F12%2F2022&site=todos'
    response = requests.get(url)
    raw_html = response.text

    parsed_html = BeautifulSoup(raw_html, 'html.parser')
    div_principal = parsed_html.select('#view-view')

    caderno_lista = []
    titulo_lista = []
    link_lista = []
    data_lista = []

    if div_principal is not None:
        for div in div_principal:
            caderno = div.select('div.c-headline__head')
            titulo = div.select('div.c-headline__wrapper > div > a > h2')
            link = div.select('div.c-headline__wrapper > div > a')
            data = div.select('div.c-headline__wrapper > div > a > div > time')

            caderno_text = caderno[0].text.strip() if caderno else ''
            titulo_text = titulo[0].text.strip() if titulo else ''
            link_href = link[0]['href'] if link else ''
            data_text = data[0].text.strip() if data else ''

            # Verificar se a frase 'Segurança da Informação' está no corpo do texto
            #corpo_texto = div.select('div.c-headline__wrapper > div > a > p')
            #corpo_texto = corpo_texto[0].text.strip() if corpo_texto else ''
            #if 'Segurança da Informação' in corpo_texto.lower():
            #   caderno_lista.append(caderno_text)
            #   titulo_lista.append(titulo_text)
            #   link_lista.append(link_href)
            #   data_lista.append(data_text)

            caderno_lista.append(caderno_text)
            titulo_lista.append(titulo_text)
            link_lista.append(link_href)
            data_lista.append(data_text)

    dados = {
        'Caderno': caderno_lista,
        'Título': titulo_lista,
        'Link': link_lista,
        'Data': data_lista
    }

    df = pd.DataFrame.from_dict(dados)
    #df['Data'] = pd.to_datetime(df['Data'])  # Converter a coluna 'Data' para Timestamp

    # Filtrar notícias dentro do período desejado (dois anos)
    # start_date = pd.Timestamp('2018-01-01')
    # end_date = pd.Timestamp('2022-12-31')
    # mask = (df['Data'] >= start_date) & (df['Data'] <= end_date)
    # filtered_df = df.loc[mask]

    return render_template('index.html', df=df)

if __name__ == '__main__':
    app.run(debug=False)