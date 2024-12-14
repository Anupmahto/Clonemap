# Project: Google Maps Clone for Bengaluru

## Backend Code (Flask + OSMnx)

from flask import Flask, request, jsonify
import osmnx as ox
import networkx as nx
import json

# Initialize Flask app
app = Flask(__name__)

# Preload graph data for Bengaluru
def load_graph():
    print("Loading graph data for Bengaluru...")
    G = ox.graph_from_place("Bengaluru, India", network_type="drive")
    return G

G = load_graph()

@app.route("/shortest-path", methods=["POST"])
def shortest_path():
    try:
        data = request.get_json()
        origin = (data['origin']['lat'], data['origin']['lng'])
        destination = (data['destination']['lat'], data['destination']['lng'])
        
        orig_node = ox.nearest_nodes(G, origin[1], origin[0])
        dest_node = ox.nearest_nodes(G, destination[1], destination[0])
        
        shortest_path = nx.shortest_path(G, orig_node, dest_node, weight="length")
        
        path_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]

        return jsonify({"path": path_coordinates}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
