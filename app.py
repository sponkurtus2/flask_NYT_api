# To add all the packages requirements, you can use 'pip freeze > requirements.txt'
from flask import Flask, render_template, request, redirect, url_for
# To start using this app, you first need to type in the terminal 'pip install requests'
import requests

app = Flask(__name__)

# To use the NYT api, we need a key, so we save it here, and then save the url which we are going to fetch
api_key = 'bDnEbbqzPLaaok4ule1hMl3UdXx8fNZ1'
base_url = 'https://api.nytimes.com/svc/topstories/v2/'

# Flask uses ROUTES, and it's the most important thing in the framework, because it's how we are going to organize our pages
# in this piece of code, we create the main route, the root route, that means that when we create our index html
# The first web which is going to load, is this, the /
# Here we are telling the function that is going to use 2 methods, GET and POST, this is because we are going to be GETTING
# the request, and POST because we are going to be POSTING data about the sections, it means that we'll recieve data.
@app.route('/', methods=['GET', 'POST'])
def get_top_stories():
    #   To make this route work, we'll define a function which is going to handle our calls to the API

    # This is going to handle the select element from the index.html, it will recieve the option
    # And use it hete
    if request.method == 'POST':
        section = request.form['section']
        return redirect(url_for('get_top_stories', section=section))

    # The default option will be home
    section = request.args.get('section', 'home')

    # We define the endpoint (data from the api) with a formated string which will have 2 parameters
    # The base URL that we declared earlier, and the section that we want to recieve the news from.
    # We recieve the data in a json format.
    endpoint = f'{base_url}{section}.json'
    # To acces to the parameters we se our api key
    params = {'api-key': api_key}

    # we create a response variable to save the data that we requested to the NYT APi
    response = requests.get(endpoint, params=params)
    # Then, we transform that response, into a json file
    data = response.json()

    # This is to save the title of the news topic
    section_title = section

    # articles is the variable which is going to save the posts, to make this possible, we do this.
    # data.get -> we GET the info from our DATA variable which has the JSON INFORMATION
    # ('results') -> we want the RESULTS section from the DATA JSON
    # [] -> first creates an empty list, and then saves the ARTICLES from the DATA.GET
    # [:5] -> After saving all the data, we specify that we ONLY want the first 5 articles
    articles = data.get('results', [])[:6]

    #   And all the info es done, now we just return it to our index.html, and we pass the articles, and
    #   the section as parameters, so we can use them in the html file
    return render_template('index.html', articles=articles, section_title=section_title)

# Now, we want a route that can handle the section change, so we create it, and it's only method
# will be POST because we're only going to be POSTING data (the different articles)
@app.route('/update_section', methods=['POST'])
def update_section():
    # This route will only save the section that we pick from the html and will save it here
    section = request.form['section']
    # Then we will redirect our user to the get_top_stories function to render all the data
    # but now with the new section
    return redirect(url_for('get_top_stories', section=section))

# And finally, this is to run the app
if __name__ == '__main__':
    app.run()