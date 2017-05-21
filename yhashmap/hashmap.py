"""
A hashmap with with amortized O(1) for search, insertion, and deletion
"""

from yhashmap.dlinkedlist import DLinkedList


class Hashmap(object):
    """
    A hash-map optimized for small to moderate sized storage (< 30,000 objects)
    """
    def __init__(self, size=17, loadfactor=0.75):
        """
        :param size: Initial capacity of the hashmap
        :param loadfactor: A ratio which represents; number of elements : size
        """
        self.size = size
        self.loadfactor = loadfactor
        self.table = [None] * self.size
        self.obj_count = 0
        self.primes = [2] #  cache primes so they aren't recalculated per resize
        self.not_prime = set() #  cache composites " " " " " "

    def __str__(self):
        map_as_str = []

        for i in range(len(self.table)):
            bucket = self.table[i]
            map_as_str.append('[X]: 'if bucket is None else '[' + str(i) + ']: ' + str(bucket))
            map_as_str.append('\n')

        return ''.join(map_as_str)

    def insert(self, key, obj):
        """
        :param key: A string to access the corresponding object
        :param object: An object to store in the hash map
        """
        #  Stop users from using keys which are absurdly large,
        #  This has the side effect of making hash_code O(k) -> O(1)
        if len(key) > 36:
            return
        elif self.obj_count / self.size > self.loadfactor:
            self.resize()

        if self.table[self.hash_code(key)] is None:
            self.table[self.hash_code(key)] = DLinkedList()

        self.table[self.hash_code(key)].append_node((key, obj))
        self.obj_count += 1

    def search(self, key):
        """
        :param key: A string to access the corresponding object
        :return: The object if it exists, or Nil
        """
        if self.table[self.hash_code(key)] is not None:
            return self.table[self.hash_code(key)].find_node(key)

        return None

    def delete(self, key, obj):
        """
        :param key: A string to access the corresponding object
        :param object: An object to store in the hash map
        :return: True if the object exists, False otherwise
        """
        if self.table[self.hash_code(key)] is not None:
            return self.table[self.hash_code(key)].remove_node(obj)

        return False

    def hash_code(self, key):
        """
        :param key: A string uniquely identifying an object
        :return: a hash value
        """
        return (sum([ord(ch) * 128 for ch in key])) % self.size

    def resize(self):
        """
        Resize the hash map if the threshold is met
        """
        self.size = self.sieve_of_eratosthenes(self.size * 2)
        new_map = [None] * self.size

        for i in range(len(self.table)):
            if self.table[i] is not None:
                curr_key = self.table[i].get_head().val[0]
                new_map[self.hash_code(curr_key)] = self.table[i]

        self.table = new_map

    def sieve_of_eratosthenes(self, limit):
        """
        :param limit: An integer
        :return: The largest prime number <= limit
        """
        limitn = limit+1

        for i in range(self.primes[len(self.primes) - 1], limitn):
            if i in self.not_prime:
                continue

            for num in range(i*2, limitn, i):
                self.not_prime.add(num)

            self.primes.append(i)

        return self.primes[len(self.primes) - 1]
