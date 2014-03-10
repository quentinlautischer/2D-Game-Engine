#HeapSort
# Priority Queue
"""
Priority queue implemented with a binary heap.

Supports operations:
pop_min: removes and returns the element with the smallest Priority
insert: adds an element with a Priority
update: change an element's priority to a LOWER value

>>> q = PriorityQueue()
>>> q.update("A", 65)
>>> q.update("null", 0)
>>> q.update("B", 66)
>>> q.pop_min()
['null', 0]
>>> q.pop_min()[0]
'A'

>>> q.update("Mike", 52)
>>> q.update("Leah", 12)
>>> q.update("Walter", 84)
>>> q.update("Walter", 7)
>>> q.pop_min()
['Walter', 7]


>>> len(q)
3

>>> q.update("Mike", 128)

>>> while q:
...    print(q.pop_min())
["Leah", 12]
["Mike", 52]
['B', 66]
>>> len(q)
0

>>> q.update("Mike", 12)
>>> len(q)
1
>>> "Mike" in q
True
"""

class PriorityQueue:
    def __init__(self):
        self._items = []
        self._locations = {}

    def __len__(self):
        return len(self._items)

    def __contains__(self):
        return x 

    def _lchild(self, i):
        if len(self._items) <= 2*i+1: return None
        return 2*i+1

    def _rchild(self, i):
        if len(self._items) <= 2*i+2: return None
        return 2*i+2

    def _parent(self, i):
        if i ==0: return None
        return (i-1)//2

    def _swap(self, i, j):
        self._items[i], self._items[j] = self._items[j], self._items[i]
        self._locations[self._items[i][0]] = i
        self._locations[self._items[j][0]] = j


    def _fix_heap_up(self, i):
        """
        Fixes heap violations, where index i may have smaller
        priority than its parent
        """
        parent = self._parent(i)
        if parent != None and self._items[i][1] < self._items[parent][1]:
            self._swap(i, parent)
            self._fix_heap_up(parent)

        while (self._parent != None and 
                self._items[i][1] < self._items[self._parent(i)][1]):
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _fix_heap_down(self, i):
        lchild = self._lchild(i)
        rchild = self._rchild(i)

        if rchild != None:
            if self._items[lchild][1] < self._items[rchild][1]:
                minchild = lchild
            else: 
                minchild = rchild
        elif lchild != None:
            minchild = lchild
        else:
            return
        if self._items[i][1] > self._items[minchild][1]:
            self._swap(i, minchild)
            self._fix_heap_down(minchild)

    def pop_min(self):
        """
        Dont call
        """
        rv = self._items[0] 
        if len(self._items) > 1:
            self._items[0] = self._items.pop()
            self._fix_heap_down(0)
        else:
            self._items.pop()
        self._locations.pop(rv[0])
        return rv

    def update(self, element, priority):
        """
        Don't call this on elements not in the priority queue.
        """
        if element not in self._locations:
            self._items.append([element, priority])
            self._locations[element] = len(self._items)-1
            self._fix_heap_up(len(self._items)-1)            

        else:
            # Find where the element is in the pqueue
            index = self._locations[element]

            # Update its priority (Maybe)
            if self._items[index][1] > priority:
                self._items[index][1] = priority
                # Fix heap up
                self._fix_heap_up(index)
