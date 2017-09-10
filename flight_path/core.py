import googlemaps
import json
from config.api_key import google_maps_api
import math
from collections import defaultdict
from collections import deque

class Airport:
    def __init__(self, code="", name=""):
        self.code = code
        self.name = name
        if code != "":
            self.geoloc = self.set_geoloc(code)
        else:
            self.geoloc = {'lat': 0, 'lng':0}

    def __eq__(self, other):
        return self.code == other.code

    def __hash__(self):
        return hash((self.geoloc['lat'], self.geoloc['lng']))

    def set_geoloc(self, code):
        gmaps_client = googlemaps.Client(key=google_maps_api)
        result = gmaps_client.geocode(code)
        return result[0]['geometry']['location']

    def get_distance_to(self, other_airport):
        #http://www.movable-type.co.uk/scripts/latlong.html

        r = 6371e3 # earth's radius in meters
        psi1 = math.radians(self.geoloc['lat'])
        psi2 = math.radians(other_airport.geoloc['lat'])

        delta_psi = math.radians(other_airport.geoloc['lat'] - self.geoloc['lat'])
        delta_gamma = math.radians(other_airport.geoloc['lng'] - self.geoloc['lng'])

        a = math.sin(delta_psi / 2) * math.sin(delta_psi / 2) + math.cos(psi1) * math.cos(psi2) * \
            math.sin(delta_gamma / 2) * math.sin(delta_gamma / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        d = r * c

        return d / 1000


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = {}

    def has_vertex(self, thing):
        return thing in self.vertices

    def get_vertices(self):
        return self.vertices

    def get_adjacency(self, vertex):
        return self.vertices[vertex]

    def add_flight_path(self, origin, destination): #todo make get_edge
        if origin not in self.vertices:
            raise ValueError("origin is not in graph")
        self.vertices[origin][destination] = origin.get_distance_to(destination)

    def get_flight_path_length(self, origin, destination): #todo make get_weight
        return self.vertices[origin][destination]

    def find_route(self, origin, destination, distance_limit):
        distances, predecessor = self.breadth_first_search(origin, distance_limit)
        path = []
        current = destination
        if distances[destination] != math.inf:
            for x in range(distances[destination]):
                path.append(predecessor[current])
                current = predecessor[current]

        return path

    # Breadth first search
    def breadth_first_search(self, starting_vertex, distance_limit):
        # start from point start
        # create q with s in queue
        v_queue = deque(starting_vertex)

        marked = []

        # dictionary of distances from s to each vertex, set to math.inf
        distances = {key: math.inf for key in self.vertices}
        # dictionary of previous vertex on path from s to each vertex, each set to None
        predecessor = {key: None for key in self.vertices}
        distances[starting_vertex] = 0
        predecessor.popitem(starting_vertex)

        #while queue is not empty
        while v_queue:
            # new vertex equals queue.pop
            vertex = v_queue.popleft()

            # explore each of the neighboring vertices
            for adjacent in self.vertices[vertex]:
                # discarding those at a suboptimal distance
                # or that have already been explored
                if self.get_flight_path_length(vertex, adjacent) <= distance_limit or vertex not in marked:
                # for every qualified neighbor
                #     for that neighbor, set distance +1 distance vertex
                    distances[adjacent] = distances[vertex] + 1
                #     for that neighbor, set predecessor to vertex
                    predecessor[adjacent] = vertex

        # add vertex to marked dictionary when finished
            marked.append(vertex)

        # return the two dicts of information
        return distances, predecessor

#todo elements of the graph class are specific to the application. abstract them