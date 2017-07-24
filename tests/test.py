import unittest
from flight_path.core import Airport, Graph
#todo import google maps api

class TestAirport(unittest.TestCase):
    def test_can_create_airport(self):
        birmingham = Airport()
        self.assertIsInstance(birmingham, Airport)

    def test_airport_has_members(self):
        seattle = Airport("KSEA", "Seattle-Tacoma International", "P-L")
        self.assertEqual(seattle.name, "Seattle-Tacoma International")
        self.assertEqual(seattle.code, "KSEA")
        self.assertEqual(seattle.type, "P-L")

    def test_airport_has_geoloc(self):
        houston = Airport("KIAH", "George Bush Intercontinental Airport", "P-L")
        self.assertEqual(houston.geoloc, {'lat': 29.9902199, 'lng': -95.3367827})

    def test_can_find_distance_between_airports(self):
        houston = Airport("KIAH", "George Bush Intercontinental Airport", "P-L")
        seattle = Airport("KSEA", "Seattle-Tacoma International", "P-L")
        self.assertAlmostEqual(3013.28, seattle.get_distance_to(houston), places=2)


class TestGraph(unittest.TestCase):
    def test_can_create_graph(self):
        air_map = Graph()
        self.assertIsInstance(air_map, Graph)

    def test_can_add_vertex(self):
        air_map = Graph()
        houston = Airport("KIAH", "George Bush Intercontinental Airport", "P-L")
        air_map.add_vertex(houston)
        self.assertTrue(air_map.has_vertex(houston))

        seattle = Airport("KSEA", "Seattle-Tacoma International", "P-L")
        air_map.add_vertex(seattle)
        self.assertTrue(air_map.has_vertex(seattle))

    def test_can_add_edge(self):
        air_map = Graph()
        houston = Airport("KIAH", "George Bush Intercontinental Airport", "P-L")
        seattle = Airport("KSEA", "Seattle-Tacoma International", "P-L")

        air_map.add_flight_path(seattle, houston)
        self.assertAlmostEqual(air_map.get_flight_path_length(seattle, houston), 3013.28, places=2)

    def test_can_find_a_path(self):
        #load from into the graph
        #load to into the graph
        self.fail('implement the path searching')

    def test_can_find_the_shortest_path(self):
        #load several points
        #assert the path returned fits shortest parameters
        pass

#todo
