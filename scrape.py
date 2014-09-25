import os
from flask import Flask
from urllib import urlopen
import lxml.html
from lxml.html import fromstring
from flask import render_template, Markup

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

@app.route('/autofare/<format>')
@app.route('/autofare/')
def autofare(format=None):
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
	table = Markup(lxml.html.tostring(fare_table[0]))
	min_fare = int(html_object.cssselect("#MC_lblMinimumFare")[0].text_content()[2:4])
	per_unit = int(html_object.cssselect("#MC_lblFarePerUnitDistance")[0].text_content()[2:4])
	if format == 'json':
		return flask.jsonify(min_fare=min_fare, per_unit = per_unit)
	return render_template('autofare.html', table = table, min_fare=min_fare, per_unit = per_unit)
	
def get_source(url):
	html = urlopen(url).read()
	dom = fromstring(html)
	dom.make_links_absolute(url)
	return dom

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)