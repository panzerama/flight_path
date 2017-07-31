import googlemaps
import json
from config.api_key import google_maps_api
import math
from collections import defaultdict
from flight_path import PriorityDict

class Airport:
    def __init__(self, code="", name="", type=""):
        self.code = code
        self.name = name
        self.type = type
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

    def add_flight_path(self, origin, destination):
        if origin not in self.vertices:
            raise ValueError("origin is not in graph")
        self.vertices[origin][destination] = origin.get_distance_to(destination)

    def get_flight_path_length(self, origin, destination):
        return self.vertices[origin][destination]

    def find_route(self, origin, destination, distance_limit):
        #wrapper for dijkstra
        pass

    def dijsktra(self, start, end):
        """Return a list of nodes and distances related to the travel from initial to those nodes
        initial -- an Airport object, the starting point
        end -- limiting node. search ends when end is encountered in graph
        """
        D = {}  # dictionary of final distances
        P = {}  # dictionary of predecessors
        Q = PriorityDict()  # est.dist. of non-final vert.
        Q[start] = 0

        for v in Q:
            D[v] = Q[v]
            if v == end: break

            for w in self.vertices[v]:
                vwLength = D[v] + self.vertices[v][w]
                if w in D:
                    if vwLength < D[w]:
                        raise ValueError("Dijkstra: found better path to already-final vertex")
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v

        return (D, P)

    def shortestPath(self, start, end):
        """
        Find a single shortest path from the given start vertex
        to the given end vertex.
        The input has the same conventions as Dijkstra().
        The output is a list of the vertices in order along
        the shortest path.
        """

        D, P = self.dijkstra(start, end)
        path = []
        while 1:
            path.append(end)
            if end == start: break
            end = P[end]
        path.reverse()
        return path