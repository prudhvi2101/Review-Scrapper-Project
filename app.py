from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

application = Flask(__name__)
app = application

@app.route("/home", methods = ['GET'])
@cross_origin()
def hello_world():
    return render_template('home.html')

@app.route("/submit-product", methods = ['POST'])
@cross_origin()
def show():
    if (request.method == 'POST'):
        try:
            searchstring = request.form['content'].replace(" ","")
            domain = 'https://www.amazon.in'
            web_url = f'https://www.amazon.in/s?k={searchstring}'
            headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
            page = requests.get(url=web_url, headers=headers)
            amazon_html = bs(page.content, 'html.parser')
            print(amazon_html.show_status)
            bigboxes = amazon_html.find_all('div', {'class': 'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16'})
            box1 = bigboxes[2]
            product1 = domain+box1.div.div.div.div.div.div.div.span.a['href']
            product1_html = bs(uReq(product1).read(), 'html.parser')
            reviews = product1_html.find_all("div", {'class':'a-section review aok-relative'})


            Product_Ratings=[]
            for i in reviews:
                try:
                    Rating = i.div.div.find_all('div', {'class':'a-row a-spacing-small review-data'})[0].div.div.span.text
                except:
                    Rating = 'No Rating'

                try:
                     Comment = i.div.div.find_all('div', {'class': 'a-row'})[1].a['title']
                except:
                    Comment = 'No Comment'
            
                mydict = {"Product": searchstring, "Rating": Rating, "Comment": Comment}
                Product_Ratings.append(mydict)

            return render_template('result.html', Product_Ratings=Product_Ratings)
        except:
            return 'something is wrong'


    else:
        return render_template('home.html')


if __name__== "__main__":
    app.run(host='0.0.0.0', port = 8000 )
