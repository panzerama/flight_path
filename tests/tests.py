import unittest
from flight_path.core import Airport, Graph
#todo import google maps api
import random

class TestAirport(unittest.TestCase):

    def setUp(self):
        file_path = '../data/us-primary-airports.txt'
        airports = open(file_path, 'r', encoding="utf-8")
        air_map = Graph()

        for line in airports:
            airport_line = line.split(u'\t')
            airport = Airport(airport_line[0], airport_line[1])
            air_map.add_vertex(airport)

        airports_list = []
        airports = open(file_path, 'r', encoding="utf-8")

        for line in airports:
            part = line.split(u'\t')
            airports_list.append(Airport(part[0], part[1]))

        for airport in airports_list:
            if air_map.has_vertex(airport):
                air_map.add_flight_path(airport, random.choice(airports_list))

    def test_can_create_airport(self):
        birmingham = Airport()
        self.assertIsInstance(birmingham, Airport)

    def test_airport_has_members(self):
        seattle = Airport("KSEA", "Seattle-Tacoma International")
        self.assertEqual(seattle.name, "Seattle-Tacoma International")
        self.assertEqual(seattle.code, "KSEA")

    def test_airport_has_geoloc(self):
        houston = Airport("KIAH", "George Bush Intercontinental Airport")
        self.assertEqual(houston.geoloc, {'lat': 29.9902199, 'lng': -95.3367827})

    def test_can_find_distance_between_airports(self):
        houston = Airport("KIAH", "George Bush Intercontinental Airport")
        seattle = Airport("KSEA", "Seattle-Tacoma International")
        self.assertAlmostEqual(3013.28, seattle.get_distance_to(houston), places=2)


class TestGraph(unittest.TestCase):
    def test_can_create_graph(self):
        air_map = Graph()
        self.assertIsInstance(air_map, Graph)

    def test_can_add_vertex(self):
        air_map = Graph()
        houston = Airport("KIAH", "George Bush Intercontinental Airport")
        air_map.add_vertex(houston)
        self.assertTrue(air_map.has_vertex(houston))

        seattle = Airport("KSEA", "Seattle-Tacoma International")
        air_map.add_vertex(seattle)
        self.assertTrue(air_map.has_vertex(seattle))

    def test_can_add_edge(self):
        air_map = Graph()
        houston = Airport("KIAH", "George Bush Intercontinental Airport")
        seattle = Airport("KSEA", "Seattle-Tacoma International")
        air_map.add_vertex(seattle)
        air_map.add_vertex(houston)
        air_map.add_flight_path(seattle, houston)
        self.assertAlmostEqual(air_map.get_flight_path_length(seattle, houston), 3013.28, places=2)

    def test_can_find_a_path(self):
        #load airports as vertices from test file into the graph
        #load flight paths from test file to into the graph
        #nominate a start and end
        #detect a path
        #assert that a path is returned
        self.fail('implement the path searching')

    def test_can_find_the_shortest_path(self):
        # load airports as vertices from test file into the graph
        # load flight paths from test file to into the graph
        # nominate a start and end
        # detect a path
        # assert that the path returned is the most efficient
        pass

    # @staticmethod
    # def load_airport_info(file_path):
    #     airports = open(file_path, 'r')
    #     air_map = Graph()
    #
    #     for line in airports:
    #         airport_line = line.split(r'\t')
    #         airport = Airport(airport_line[0], airport_line[1])
    #         air_map.add_vertex(airport)
    #
    # def load_flight_paths(self, air_map, file_path):
    #     airports = open(file_path, 'r')
    #     airports_list = []
    #
    #     for line in airports:
    #         part = line.split(r'\t')
    #         airports_list.append(Airport(part[0], part[1]))
    #
    #     for airport in airports_list:
    #         if air_map.has_vertex(airport):
    #             air_map.add_flight_path(airport, random.choice(airports_list))


#todo pre and post conditions in app, test edge cases
#todo why were helper functions not recognized in setUp?
