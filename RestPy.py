import json
import flask
from flask_cors import CORS
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["data_file"] = "api_data.json"
CORS(app)
# Create some test data for our catalog in the form of a list of dictionaries.


@app.route('/', methods=['GET'])
def home():
	return '''
	Bad and Lazy Rest API, literally no validators or models. Just POST, DELETE, GET anything lol
	'''



# POST
@app.route('/api/v1/<path:data>', methods=['POST', 'GET', 'DELETE'])
def api_id(data):
	jsonFile = open(app.config["data_file"], "r") 
	api_data = json.load(jsonFile)
	jsonFile.close() 

	if request.method == "DELETE":
		sections = data.split("/")
		node = api_data
		for section in sections:
			if node[section] == {}  or sections.index(section) == len(sections) - 1:
				del node[section]
				with open(app.config["data_file"], 'w', encoding='utf-8') as f:
					json.dump(api_data, f, ensure_ascii=False, indent=4)
				return '200'
			node = node[section]

	if request.method == "POST":
		sections = data.split("/")
		node = api_data
		for index in range(len(sections)):
			try:
				node = node[sections[index]]
			except KeyError:
				if index == len(sections) - 1:
					node[sections[index]] = {} # Empty dict, when getting if a dict is empty just return name
				else:
					node[sections[index]] = {sections[index + 1]: {}}
				node = node[sections[index]]
		with open(app.config["data_file"], 'w', encoding='utf-8') as f:
			json.dump(api_data, f, ensure_ascii=False, indent=4)
		return "201"

	if request.method == "GET":
		
		sections = data.split("/")
		node = api_data
		for section in sections:
			if node[section] == {}  or sections.index(section) == len(sections) - 1:
				return jsonify(node[section])
			node = node[section]
		


app.run(host="0.0.0.0", port=8080)