from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

def getHtml(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def homepageHandler(yy, sem):
    url = f"https://www.jntufastupdates.com/jntuk-{yy}-{sem}-question-papers/"
    sp = getHtml(url)
    div = sp.find("figure", class_="wp-block-table")
    a_tag_links = div.find_all("a", attrs={"data-wpel-link" : "internal"})
#     print(a_tag_links)
    links = [{"text" : a_tag.text, "id" : a_tag["href"].split("/")[-2]} for a_tag in a_tag_links]
    return links



@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/sem', methods=['POST'])
def lister():
    year = request.form['year']
    sem = request.form['sem']
    data = homepageHandler(year, sem)
    return render_template('reg_year_lister.html', data = data)


@app.route('/show/<ID>', methods=['GET'])
def show(ID):
    print(ID)
    return render_template('shower.html')




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)
