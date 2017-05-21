"""
This module contains the class for a DLL with
support searching by keys and abstract objects
"""


class DLinkedList(object):
    """
    A doubly linked-list with support for querying by object or
    an object key, where the key is the first index of a tuple.
    """
    def __init__(self):
        self.head = None

    def __str__(self):
        if self.head is None:
            return "Empty"
        else:
            llist = []
            curr = self.head

            while curr is not None:
                llist.append(str(curr))
                curr = curr.next

            return ' <-> '.join(llist)

    def get_head(self):
        """
        :return: First node in DLL
        """
        return self.head

    def append_node(self, node, unique_key=True):
        """
        :param node: The object to be stored
        :param unique_key: If true, assume the object is a tuple and contains @ [0]
        """
        if self.head is None:
            self.head = Node(node)
            return
        else:
            node = Node(node)

        curr = self.head

        while curr.next is not None:
            # special case where keys must be unique in a LL
            if unique_key and curr.val[0] == node.val[0]:
                curr.val = node.val

            curr = curr.next

        curr.next = node
        node.prev = curr

    def remove_node(self, node):
        """
        :param node: Object to be removed
        """
        if self.head and self.head.val == node:
            self.head = self.head.next
            return True

        curr = self.head

        while curr and curr.val != node:
            curr = curr.next

        if curr is None:
            return False
        else:
            curr.prev.next = curr.next
            # tail edgecase
            if curr.next:
                curr.next.prev = curr.prev
            return True

    def find_node(self, node, is_key=True):
        """
        :param node: Object to be retrieved
        :param is_key: If True, the node argument is a key, instead of the object itself
        :return: The object being queried or None
        """
        if self.head is None:
            return None

        curr = self.head

        while curr:
            if is_key and curr.val[0] == node:
                break
            elif curr.val == node:
                break

            curr = curr.next

        return curr.val if curr is not None else None

class Node(object):
    """
    A doubly linked list node
    """
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

    def __str__(self):
        return str(self.val)
