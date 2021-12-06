from flask import Flask
from string import Template
app = Flask(__name__)
API_KEY = "AIzaSyB6Lwiy8_Mgt71agC0ClD1RIeFiDvhqrMg"

HTML_TEMPLATE = Template("""
<h1>Hello ${place_name}!</h1>

<img src="https://maps.googleapis.com/maps/api/streetview?size=600x300&location=${place_name}&key=AIzaSyB6Lwiy8_Mgt71agC0ClD1RIeFiDvhqrMg" alt="map of ${place_name}">

<img src="https://maps.googleapis.com/maps/api/streetview?size=600x300&location=${place_name}&key=AIzaSyB6Lwiy8_Mgt71agC0ClD1RIeFiDvhqrMg" alt="street view of ${place_name}">

<p>https://maps.googleapis.com/maps/api/streetview?size=600x300&location=${place_name}&key=AIzaSyB6Lwiy8_Mgt71agC0ClD1RIeFiDvhqrMg</p>""")

@app.route('/')
def homepage():
    return """<h1>Hello world!</h1>
    """

@app.route('/<some_place>')
def some_place_page(some_place):
    return(HTML_TEMPLATE.substitute(place_name=some_place))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)