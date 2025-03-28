"""
Main script which runs the website
"""

# Imports
from flask import Flask, render_template, request, jsonify, session
from script.load_classes import list_all_classes, create_class_network
from script.search import search_classes
from script.load_classes import create_class_network
from script.complexity_network import complexity_network
import git
import hashlib
import hmac

"""
Key variables
"""
MAX_SEARCH_OUTPUT = 100
# CLASS_LIST, class_dict = list_all_classes('./proc_classes.json')
class_json_loc = './classes.json'
theorem_json_loc = './theorems.json'
NETWORK = create_class_network(class_json_loc, theorem_json_loc)

app = Flask(__name__)

app.secret_key = b'_5#y3l"Fp7z\n\xec]/'

def update_network_information():
   network: complexity_network = NETWORK
   session['selected_classes'] = network.get_trimmed_network()
   # network.print_trimmed_network()
   return

@app.before_request
def before_req():
   # if 'network' not in session:
   #    session['network'] = create_class_network(class_json_loc, theorem_json_loc)
   if 'all_classes' not in session:
      session['all_classes'] = NETWORK.get_all_class_identifiers()
      NETWORK.new_trimmed_network(session['all_classes'])
   # Keeping track of classes from last session
   if 'selected_classes' not in session:
      session['selected_classes'] = NETWORK.get_trimmed_network()
   
   return

@app.route('/', methods=["GET"])
def index():
   return render_template('index.html')

@app.route('/references', methods=["GET"])
def references():
   return render_template('references.html')

@app.route('/searchresults', methods=['GET', "POST"])
def add_remove_class():
   if request.method == 'POST':
      var_name = request.form["name"]
      checked = bool(int(request.form["checked"]))
      print(f'{var_name} - {checked}')
      network: complexity_network = NETWORK
      if checked:
         print('Adding')
         network.add_class_to_trimmed_network(var_name)
      else:
         print('Removing')
         network.remove_class_from_trimmed_network(var_name)
      
      update_network_information()
      return var_name

@app.route('/search_complexity_classes', methods=['GET'])
def search():
   query = request.args.get('query')
   network: complexity_network = NETWORK
   results = search_classes(query, network)
   if len(results) > MAX_SEARCH_OUTPUT:
      results = results[:MAX_SEARCH_OUTPUT]
   return jsonify(results)

@app.route('/get_class_description', methods=['GET'])
def get_class_description():
   class_name = request.args.get('class_name').lower()
   network: complexity_network = NETWORK
   description = network.get_class(class_name).get_description()
   information = network.get_class(class_name).get_information()
   try:
      # title = class_dict[class_name]['title']
      # Going to add a proper title later - we should decide how to format this page
      title = network.get_class(class_name).get_latex_name()
   except:
      title = "No title available"
   return jsonify({'description': description, 'title': title, 'information':information})

@app.route('/get_complexity_network')
def get_complexity_network():
   network: complexity_network = NETWORK
   return jsonify(network.get_trimmed_network_json())

@app.route('/get_complexity_sunburst')
def get_complexity_sunburst():
   network: complexity_network = NETWORK
   return jsonify(network.get_trimmed_sunburst_json())

"""
Selecting all/no classes in the visualization
 - If 'select', then we show all classes, otherwise we unselect all
"""
@app.route('/all_class_request', methods=['GET'])
def all_class_request():
    select = request.args.get('select') == 'true'
    network: complexity_network = NETWORK
    if select:
        network.new_trimmed_network(network.get_all_class_identifiers())
    else:
        network.new_trimmed_network([])
    
   #  # Update the check_classes_dict
   #  cc_dict = session['check_classes_dict']
   #  for class_name in CLASS_LIST:
   #      cc_dict[class_name]['value'] = select
   #  session['check_classes_dict'] = cc_dict
    
    return jsonify({'success': True})

@app.route('/update_server', methods=['POST'])
def webhook():
   try:
      repo = git.Repo('/home/chrispsimadas/website')
      origin = repo.remotes.origin
      origin.pull()
      return 'Updated PythonAnywhere successfully', 200
   except Exception as e:
      print("Error during git pull"), e
      return 'Failed to update server', 500

"""
Expand item - either an edge or a node
   - expanding an edge: Find all the classes which are between the source and target classes and add those
   - expanding a node: Find all the classes which are connected to the node and add those
"""
@app.route('/expand_item', methods=['GET'])
def expand_item():
   network: complexity_network = NETWORK
   expand_edge = request.args.get('expand_edge') == 'true'
   if expand_edge:
      source_class = request.args.get('source_class')
      target_class = request.args.get('target_class')
      expand_success, new_classes = network.expand_edge(source_class, target_class)
   else:
      class_name = request.args.get('source_class')
      expand_success, new_classes = network.expand_node(class_name)
   if expand_success:
      update_network_information()
   return jsonify({'success': expand_success, 'new_classes': new_classes})

@app.route('/expand_node', methods=['GET'])
def expand_node():
   class_name = request.args.get('class_name')
   network: complexity_network = NETWORK
   expand_success, new_classes = network.expand_node(class_name)
   if expand_success:
      update_network_information()
   return jsonify({'success': expand_success, 'new_classes': new_classes})

@app.route('/delete_class', methods=['GET'])
def delete_class():
   class_name = request.args.get('class_name')
   network: complexity_network = NETWORK
   network.remove_class_from_trimmed_network(class_name)
   update_network_information()
   return jsonify({'success': True})

@app.route('/check_indirect_paths', methods=['GET'])
def check_indirect_paths():
   class_name = request.args.get('class_name')
   network: complexity_network = NETWORK
   direct_paths = network.get_direct_paths(class_name)
   return jsonify({'success': True, 'direct_paths': direct_paths})

if __name__ == '__main__':
    app.run(debug=True)
