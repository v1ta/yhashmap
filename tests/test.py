# -*- coding: utf-8 -*-
""" Test suite for yhashmap """
import unittest
import os
import sys
import string
import uuid
from random import choices
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from yhashmap.dlinkedlist import DLinkedList
from yhashmap.hashmap import Hashmap


class DLinkedListTestSuite(unittest.TestCase):
    """ Test DLL member functions """
    def test_instantiation(self):
        """ Verify DLL import and type """
        self.assertIsInstance(DLinkedList(), DLinkedList)

    def test_insertion_find(self):
        """
        Verify append_node correctly updates the list and
        find_node returns the element specficed, if it exists.
        """
        llist = DLinkedList()

        node_1 = ('123', 12)
        node_2 = ('12', ['I\' an array with a string'])
        node_3 = ('ahh', ('x', 'y'))

        llist.append_node(node_1)

        self.assertEqual(llist.find_node('123'), node_1)

        llist.append_node(node_2)
        llist.append_node(node_3)

        self.assertEqual(llist.find_node('12'), node_2)
        self.assertEqual(llist.find_node('ahh'), node_3)

    def test_removal_find(self):
        """
        Verify remove_node correctly deletes the object from the
        the list and the object can no longer be queried via find_node
        """
        llist = DLinkedList()

        # simulate insertions with keys
        node_1 = ('12', ['I\' an array with a string'])
        node_2 = ('123', 12)
        node_3 = ('ahh', ('x', 'y'))

        llist.append_node(node_1)
        llist.append_node(node_2)
        llist.append_node(node_3)

        self.assertTrue(llist.remove_node(node_3))
        self.assertIsNone(llist.find_node(node_3))


class HashMapTestSuite(unittest.TestCase):
    """ Test Hashmap member functions """
    def test_instantiation(self):
        """ Verify hashmap import and type """
        self.assertIsInstance(Hashmap(), Hashmap)

    def test_insertion_search(self):
        """
        Verify data can be inserted into the hashmap via
        insert and said data can be retrieved via search
        """
        hmap = Hashmap()

        hmap.insert('3', ['stuff'])
        hmap.insert('43', ['ahh'])
        hmap.insert('345', ['ahh'])

        self.assertEqual(hmap.search('3'), ('3', ['stuff']))
        self.assertEqual(hmap.search('43'), ('43', ['ahh']))
        self.assertEqual(hmap.search('345'), ('345', ['ahh']))

    def test_resize(self):
        """
        Test resizing capcacity, the hashmap size updates in a
        fixed manner of the largest prime < twice the previous size
        """
        hmap = Hashmap()

        for _ in range(100):
            hmap.insert(str(uuid.uuid1()), random_string(10))

        self.assertEqual(hmap.size, 241)

    def test_delete(self):
        """
        Verify that objects inserted into the hashmap can be
        deleted, and afterwards, can't be queried via their key
        """
        hmap = Hashmap()

        objs = [(str(uuid.uuid1()), random_string(10))] * 100

        for obj in objs:
            hmap.insert(obj[0], obj[1])
            self.assertEqual(hmap.search(obj[0]), obj)

        for obj in objs:
            self.assertTrue(hmap.delete(obj[0], obj), True)

    def test_asymtotic_complexity_small(self):
        """
        Stress test the hashmap can handle a moderate amount
        of data (2^14 objects) and resizes in small amount of time
        """
        hmap = Hashmap()
        tick = datetime.now()
        test_data = random_string(10)

        for _ in range(2**14):
            hmap.insert(str(uuid.uuid1()), test_data)

        diff = datetime.now() - tick

        self.assertTrue(float(diff.total_seconds()) < 1.0)

    def test_invalid_keys(self):
        """ Test keys which don't exist or have been removed """
        hmap = Hashmap()

        objs = [(str(uuid.uuid1()), random_string(10))] * 3

        for obj in objs:
            hmap.insert(obj[0], obj[1])

        #  Valid key
        self.assertEqual(hmap.search(objs[0][0]), objs[0])

        #  Invalid key
        self.assertIsNone(hmap.search('bad key'))

def random_string(length):
    """
    :param length: an int representing the length of the random string
    :return: a string of the arguments length consisting of random upper case letters and digits.
    """
    return ''.join(choices(string.ascii_uppercase + string.digits, k=length))

if __name__ == '__main__':
    unittest.main()
