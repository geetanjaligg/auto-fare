from urllib import urlopen
import lxml.html
from lxml.html import fromstring
from flask import Flask, render_template, Markup
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/autofare/')
def autofare(name=None):
	html_object = get_source("http://www.taxiautofare.com/taxi-fare-card/Bengaluru-Auto-fare")
	fare_table = html_object.cssselect("#MC_RateCardDataList")
	#print lxml.html.tostring(fare_table[0])
	fare_table[0].attrib['bordercolor'] = 'grey'
	fare_table[0].attrib['width'] = '0%'
	html_object.cssselect("#MC_RateCardDataList td")[0].attrib['bgcolor']="grey"
	for i in html_object.cssselect("#MC_RateCardDataList td"):
		i.attrib['align']='center'
	html_object.cssselect("#MC_RateCardDataList td")[::-1][0].drop_tree()
	#print lxml.html.tostring(fare_table[0])
	return render_template('autofare.html', name=name, table = Markup(lxml.html.tostring(fare_table[0])))
	
def get_source(url):
	html = urlopen(url).read()
	dom = fromstring(html)
	dom.make_links_absolute(url)
	return dom

if __name__ == '__main__':
	app.debug = True
	app.run()