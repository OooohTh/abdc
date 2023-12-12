import itertools
import unittest
from typing import Collection

from airmaps import *


def make_clique(airports: Collection[Airport]) -> AirMap:
    airmap = new_airmap('clique')
    for a, b in itertools.combinations(airports, 2):
        add_airport(airmap, a)
        add_airport(airmap, b)
        assert new_connection(a.iata, b.iata, compute_distance(a, b)) is not None
        assert new_connection(b.iata, a.iata, compute_distance(b, a)) is not None
        add_connection(airmap, a.iata, b.iata)
        add_connection(airmap, b.iata, a.iata)
    return airmap


def make_iberia() -> AirMap:
    spain_portugal_airports = [
        new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136)),
        new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681)),
        new_airport('Alicante', 'Spain', 'ALC', new_coordinates(38.34517, -0.48149)),
        new_airport('Barcelona', 'Spain', 'BCN', new_coordinates(41.38879, 2.15899)),
        new_airport('Bilbao', 'Spain', 'BIO', new_coordinates(43.26271, -2.92528)),
        new_airport('Granada', 'Spain', 'GRX', new_coordinates(37.18817, -3.60667)),
        new_airport('Madrid', 'Spain', 'MAD', new_coordinates(40.4165, -3.70256)),
        new_airport('Malaga', 'Spain', 'AGP', new_coordinates(36.72016, -4.42034)),
        new_airport('Murcia', 'Spain', 'MJV', new_coordinates(37.98704, -1.13004)),
        new_airport('Oviedo', 'Spain', 'OVD', new_coordinates(43.36029, -5.84476)),
    ]

    airmap = make_clique(spain_portugal_airports[2:])  # spain clique
    lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))

    # Lisboa -- Porto
    opo = spain_portugal_airports[1]
    add_airport(airmap, lis)
    add_airport(airmap, opo)
    add_connection(airmap, lis.iata, opo.iata)
    add_connection(airmap, opo.iata, lis.iata)

    # Lisboa -- Madrid
    mad = spain_portugal_airports[6]
    add_airport(airmap, lis)
    add_airport(airmap, mad)
    add_connection(airmap, lis.iata, mad.iata)
    add_connection(airmap, mad.iata, lis.iata)

    # Porto -- Bilbao
    bio = spain_portugal_airports[4]
    add_airport(airmap, bio)
    add_airport(airmap, opo)
    add_connection(airmap, bio.iata, opo.iata)
    add_connection(airmap, opo.iata, bio.iata)

    return airmap


class NewAirmapTests(unittest.TestCase):
    def test_new_airmap1(self):
        airmap = new_airmap('testing')
        self.assertIsNotNone(airmap)
        self.assertIsInstance(airmap, AirMap)

    def test_new_airmap2(self):
        airmap = new_airmap('testing')
        self.assertEqual(airmap.name, 'testing')
        self.assertEqual(airmap.num_airports, 0)
        self.assertEqual(airmap.num_connections, 0)

    def test_new_airmap3(self):
        airmap = new_airmap('testing')
        self.assertIsInstance(airmap.num_airports, int)
        self.assertIsInstance(airmap.num_connections, int)
        self.assertIsInstance(airmap.airports, dict)

    def test_new_airmap4(self):
        airmap = new_airmap('testing')
        self.assertEqual(len(airmap.airports), 0)


class NewCoordinatesTests(unittest.TestCase):
    def test_new_coordinates_ok1(self):
        coo = new_coordinates(-34.8165, -58.5373)
        self.assertIsNotNone(coo)
        self.assertAlmostEqual(coo.lat, -34.8165)
        self.assertAlmostEqual(coo.lon, -58.5373)

    def test_new_coordinates_ok2(self):
        coo = new_coordinates(48.20849, 16.37208)
        self.assertIsNotNone(coo)
        self.assertAlmostEqual(coo.lat, 48.20849)
        self.assertAlmostEqual(coo.lon, 16.37208)

    def test_new_coordinates_fail0(self):
        wrong_coo = new_coordinates(90.37723, -181)
        self.assertIsNone(wrong_coo)

    def test_new_coordinates_fail4(self):
        wrong_coo = new_coordinates(98.37723, 180.457)
        self.assertIsNone(wrong_coo)


class NewAirportTests(unittest.TestCase):
    def test_new_airport_ok0(self):
        coord = new_coordinates(-34.8165, -58.5373)
        eze = new_airport("Buenos Aires", "Argentina", "EZE", coord)
        self.assertIsNotNone(eze)
        self.assertIsInstance(eze, Airport)
        self.assertEqual(eze.name, "Buenos Aires")
        self.assertEqual(eze.country, "Argentina")
        self.assertEqual(eze.iata, "EZE")
        self.assertEqual(eze.coord, coord)

    def test_new_airport_ok1(self):
        coord = new_coordinates(-34.8165, -58.5373)
        assert coord is not None
        eze = new_airport("Buenos Aires", "Argentina", "EZE", coord)
        self.assertIsNotNone(eze)
        self.assertIsInstance(eze, Airport)
        self.assertEqual(len(eze.outgoing), 0)

    def test_new_airport_name_is_empty_string(self):
        coord = new_coordinates(43.70643, -79.39864)
        assert coord is not None
        wrong_ytz = new_airport('', "Canada", "YTZ", coord)
        self.assertIsNone(wrong_ytz)

    def test_new_airport_iata_is_empty_string(self):
        coord = new_coordinates(43.70643, -79.39864)
        assert coord is not None
        wrong_ytz = new_airport('Toronto', "Canada", "", coord)
        self.assertIsNone(wrong_ytz)

    def test_new_airport_iata_is_alpha_string(self):
        coord = new_coordinates(43.70643, -79.39864)
        assert coord is not None
        wrong_ytz = new_airport('Toronto', "Canada", "YT1", coord)
        self.assertIsNone(wrong_ytz)


class AddAirportTests(unittest.TestCase):
    def test_add_airport_ok1(self):
        cbr_coord = new_coordinates(-35.28346, 149.12807)
        cbr = new_airport("Canberra", "Australia", "CBR", cbr_coord)
        airmap = new_airmap("testmap")
        self.assertEqual(add_airport(airmap, cbr), 1)
        self.assertEqual(airmap.num_airports, 1)
        self.assertEqual(airmap.airports, {cbr.iata: cbr})

    def test_add_airport_ok2(self):
        eze_coord = new_coordinates(-34.61315, -58.37723)
        eze = new_airport("Buenos Aires", "Argentina", "EZE", eze_coord)
        ytz_coord = new_coordinates(43.70643, -79.39864)
        ytz = new_airport("Toronto", "Canada", "YTZ", ytz_coord)
        airmap = new_airmap("testmap")
        self.assertEqual(add_airport(airmap, eze), 1)
        self.assertEqual(airmap.num_airports, 1)
        self.assertEqual(airmap.airports, {eze.iata: eze})
        self.assertEqual(add_airport(airmap, ytz), 2)
        self.assertEqual(airmap.num_airports, 2)
        self.assertEqual(airmap.airports, {eze.iata: eze, ytz.iata: ytz})


class NewConnectionTests(unittest.TestCase):
    def test_new_connection_ok(self):
        coord = new_coordinates(-34.61315, -58.37723)
        eze = new_airport("Buenos Aires", "Argentina", "EZE", coord)
        coord = new_coordinates(43.70643, -79.39864)
        ytz = new_airport("Toronto", "Canada", "YTZ", coord)
        eze_ytz = new_connection(eze.iata, ytz.iata, 9000)
        self.assertIsNotNone(eze_ytz)
        self.assertEqual(eze.iata, eze_ytz.iata_origin)
        self.assertEqual(ytz.iata, eze_ytz.iata_destination)
        self.assertEqual(eze_ytz.kms, 9000)

    def test_new_connection_fail(self):
        coord = new_coordinates(41.248, -8.681)
        opo = new_airport("Porto", "Portugal", "OPO", coord)
        coord = new_coordinates(38.781, -9.136)
        lis = new_airport("Lisboa", "Portugal", "LIS", coord)
        lis_opo_weird = new_connection(lis.iata, opo.iata, 10000000)  # go a few times around the earth
        self.assertIsNone(lis_opo_weird)


class ComputeDistanceTests(unittest.TestCase):
    def test_compute_distance_commutative(self):
        coord = new_coordinates(0, 0)
        a = new_airport('1', 'n', 'AAA', coord)
        coord = new_coordinates(0, 5)
        b = new_airport('2', 'n', 'AAB', coord)
        self.assertAlmostEqual(compute_distance(a, b), compute_distance(b, a))

    def test_compute_distance_toy(self):
        coord = new_coordinates(0, 0)
        a = new_airport('1', 'n', 'AAA', coord)
        coord = new_coordinates(0, 5)
        b = new_airport('2', 'n', 'AAB', coord)
        self.assertGreaterEqual(compute_distance(a, b), 545)
        self.assertLessEqual(compute_distance(b, a), 565)

    def test_compute_distance_toy2(self):
        coord = new_coordinates(1, 0)
        c = new_airport('3', 'n', 'AAC', coord)
        coord = new_coordinates(-1, 0)
        d = new_airport('4', 'n', 'AAD', coord)
        self.assertGreaterEqual(compute_distance(c, d), 212)
        self.assertLessEqual(compute_distance(c, d), 232)

    # I check the distances in the tests against https://www.airmilescalculator.com/distance/lis-to-cbr/
    def test_compute_distance_real1(self):
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        d = compute_distance(opo, lis)
        self.assertGreaterEqual(d, 267)
        self.assertLessEqual(d, 287)

    def test_compute_distance_real4(self):
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        cbr = new_airport("Canberra", "Australia", "CBR", new_coordinates(-35.28346, 149.12807))
        d = compute_distance(lis, cbr)
        self.assertGreaterEqual(d, 18048)
        self.assertLessEqual(d, 18068)


class AddConnectionTests(unittest.TestCase):
    def test_add_connection_ok1(self):
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        airmap = new_airmap('testing')
        add_airport(airmap, lis)
        add_airport(airmap, opo)
        self.assertEqual(add_connection(airmap, lis.iata, opo.iata), 1)
        self.assertEqual(airmap.num_connections, 1)

    def test_add_connection_ok2(self):
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        airmap = new_airmap('testing')
        add_airport(airmap, opo)
        add_airport(airmap, lis)
        lis_opo = new_connection(lis.iata, opo.iata, compute_distance(opo, lis))
        self.assertEqual(add_connection(airmap, lis.iata, opo.iata), 1)
        self.assertIn(opo.iata, lis.outgoing.keys())
        self.assertEqual(lis_opo, lis.outgoing[opo.iata])

    def test_add_connection_origin_not_in_airmap(self):
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        airmap = new_airmap('testing')
        assert add_airport(airmap, opo) == 1
        out = add_connection(airmap, lis.iata, opo.iata)
        self.assertIsNone(out)

    def test_add_connection_add_connection_twice(self):
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        airmap = new_airmap('testing')
        assert add_airport(airmap, opo) == 1
        assert add_airport(airmap, lis) == 2
        self.assertEqual(airmap.num_airports, 2)
        self.assertEqual(add_connection(airmap, lis.iata, opo.iata), 1)
        self.assertEqual(airmap.num_connections, 1)
        out = add_connection(airmap, lis.iata, opo.iata)
        self.assertIsNone(out)


class TestNearDistance(unittest.TestCase):

    def test_near_distance_ok_iberia_200(self):
        airmap = make_iberia()
        d_200 = near_distance(airmap, airmap.airports['LIS'], 200)
        self.assertIsNotNone(d_200)
        self.assertIn('LIS', d_200)
        for iata in airmap.airports:
            if iata != 'LIS':
                self.assertNotIn(iata, d_200)

    def test_near_distance_ok_iberia_500(self):
        airmap = make_iberia()
        d_500 = near_distance(airmap, airmap.airports['LIS'], 500)
        self.assertIsNotNone(d_500)
        self.assertIn('LIS', d_500)
        self.assertIn('OPO', d_500)
        self.assertIn('MAD', d_500)
        self.assertIn('AGP', d_500)
        for iata in airmap.airports:
            if iata != 'LIS' and iata != 'OPO' and iata != 'MAD' and iata != 'AGP':
                self.assertNotIn(iata, d_500)

    def test_near_distance_ok_iberia_800(self):
        airmap = make_iberia()
        d_800 = near_distance(airmap, airmap.airports['LIS'], 800)
        self.assertIsNotNone(d_800)
        correct = ['LIS', 'OPO', 'ALC', 'BIO', 'GRX', 'MAD', 'AGP', 'MJV', 'OVD']
        for iata in correct:
            self.assertIn(iata, d_800)
        for iata in airmap.airports:
            if iata not in correct:
                self.assertNotIn(iata, d_800)


class TestRouteDistance(unittest.TestCase):
    def test_valid_route_ok1(self):
        iberia = make_iberia()
        route = route_distance(iberia, ['LIS'])
        self.assertIsNotNone(route)
        self.assertEqual(route, 0)

    def test_valid_route_ok2(self):
        iberia = make_iberia()
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        route = route_distance(iberia, ['LIS', 'OPO'])
        self.assertIsNotNone(route)
        self.assertAlmostEqual(route, compute_distance(lis, opo))

    def test_valid_route_ok3(self):
        iberia = make_iberia()
        opo = new_airport("Porto", "Portugal", "OPO", new_coordinates(41.248, -8.681))
        lis = new_airport("Lisboa", "Portugal", "LIS", new_coordinates(38.781, -9.136))
        bio = new_airport('Bilbao', 'Spain', 'BIO', new_coordinates(43.26271, -2.92528))
        route = route_distance(iberia, ['LIS', 'OPO', 'BIO'])
        self.assertIsNotNone(route)
        self.assertAlmostEqual(route, compute_distance(lis, opo) + compute_distance(bio, opo))

    def test_valid_route_fail_no_airport1(self):
        iberia = make_iberia()
        route = route_distance(iberia, ['LIS', 'CBR'])
        self.assertIsNone(route)

    def test_valid_route_fail_no_connection(self):
        iberia = make_iberia()
        route = route_distance(iberia, ['LIS', 'BCN'])
        self.assertIsNone(route)

    def test_valid_route_fail_cycle2(self):
        iberia = make_iberia()
        route = route_distance(iberia, ['LIS', 'MAD', 'LIS'])
        self.assertIsNone(route)


class TestNearHops(unittest.TestCase):
    def test_near_hops_iberia0(self):
        iberia = make_iberia()
        hops = near_hops(iberia, iberia.airports['LIS'], 0)
        self.assertIsNotNone(hops)
        self.assertEqual(len(hops), 1)
        self.assertIn('LIS', hops)

    def test_near_hops_iberia1(self):
        iberia = make_iberia()
        hops = near_hops(iberia, iberia.airports['LIS'], 1)
        self.assertIsNotNone(hops)
        self.assertEqual(len(hops), 3)
        self.assertIn('LIS', hops)
        self.assertIn('OPO', hops)
        self.assertIn('MAD', hops)

    def test_near_hops_iberia_fail(self):
        iberia = make_iberia()
        hops = near_hops(iberia, iberia.airports['LIS'], -1)
        self.assertIsNone(hops)


if __name__ == '__main__':
    unittest.main(failfast=False)
