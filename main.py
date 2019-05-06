import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """
    Gets a random fact from unkow.com
    :return: fact string
    """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    fact = soup.find_all("div", id="content")

    formatted_fact = fact[0].getText()

    return formatted_fact


def get_pig_latin(formatted_fact):
    """
    Function that gets the url of the translated fact
    :return: Translation url page
    """
    request_url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    input_data = {"input_text": formatted_fact}

    translation_url = requests.post(request_url, data=input_data, allow_redirects=False)
    translation_page = translation_url.headers["Location"]

    return translation_page


def get_translation_url(translation_page):
    """
    Gets the translation of the fact
    :param request: URL for translated fact
    :return: new translation URL
    """
    response = requests.get(translation_page)

    soup = BeautifulSoup(response.content, "html.parser")
    translated_fact = soup.find("body").getText().replace("Pig Latin", " ").replace("Esultray", " ")

    return translated_fact


@app.route('/')
def home():
    """
    Landing page for web app
    :return: url to Pig Latin translation of random fact
    """
    fact = get_fact().strip()
    translation_url = get_pig_latin(fact)
    translated_fact = get_translation_url(translation_url)

    return home_page_template().format(translated_fact)


def home_page_template():
    """
    Formatting template for home page
    :return: HTML template
    """
    template = """
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    
        <title>Random Pig Latin Fact</title>
      </head>
      <body>
        <h1>Welcome to the Random Pig Latin Fact Generator!</h1>
        <p>{}</p>
      </body>
    </html>
    """
    return template


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

