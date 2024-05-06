import unittest
from Algorithms.ShortestPath import ShortestPath


class Test_shortestpath(unittest.TestCase):

    def test_dijkstra(self):
        arr1 = [[0,2,0,5,0],
                [2,0,3,0,7],
                [0,3,0,1,0],
                [5,0,1,0,4],
                [0,7,0,4,0]]
        arr2 = [[0,2,0,5,0],
                [2,0,1,0,7],
                [0,1,0,1,0],
                [5,0,1,0,4],
                [0,7,0,4,0]]
        sp = ShortestPath()

        r1 = sp.dijkstra(arr1,0,4)
        r2 = sp.dijkstra(arr2,0,4)
        self.assertEqual(r1,([0,1,4],9))
        self.assertEqual(r2,([0,1,2,3,4],8))