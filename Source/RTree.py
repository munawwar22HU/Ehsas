import copy
# Helper Functions


def get(Entry, key1, key2):
    return(Entry.MBR[key1][key2])


class TreeEntry:
    def __init__(self, value=None, f=""):
        self.MBR = value
        self.Pointer = None
        self.Name = f
        self.Address = ""
        self.City = ""
        self.Province = ""
        self.Area = ""
        self.Cell = ""
        self.Landline = ""
        self.Latitude = float()
        self.Longitude = float()
        self.StoreType = list()

    def setPointer(self, Pointer):
        self.Pointer = Pointer

    def getPointer(self):
        return self.Pointer

    def __str__(self):
        return "MBR : " + str(self.MBR) + " Pointer " + str(self.Pointer)+" :  "+str(self.Name)+' : '+str(self.Area)+' : '

    def setData(self, Name, Address, Province, Area, Cell, Landline, Latitude, Longitude, StoreList):
        self.Name = Name
        self.Address = Address
        self.Province = Province
        self.Area = Area
        self.Cell = Cell
        self.Landline = Landline
        self.Latitude = float(Latitude)
        self.Longitude = float(Longitude)
        self.StoreType = StoreList

    def getData(self):
       return str(self.Name)

class TreeNode:
    """ A node in R-Tree that supports:

    - add : given a entry, returns the number of entries currently in the Node

    """

    def __init__(self):

        # The Node will contain a maximum of 2 Enttries.
        self.EntryList = [None] * 2
        self.N = 0

    def add(self, entry):
        """ Adds entry to the Entry List

        Args:
        - self: the Tree Node in which the entry is being added, mandatory object refrence
        - entry: the entry which is being added to the Tree Node

        Returns:
        an integer N which is the number of entries in the node
        """

        if self.N < 2:  # The Maximum of entries a Root Node can contain is N , which in this case is 2.
            self.EntryList[self.N] = entry
            # print(self.EntryList)
        else:
            self.EntryList.append(entry)
        self.N += 1

        return self.N


class RTree:
    """ A R-Tree that supports:

    - insert : given a value, it inserts an entry in the R-Tree. Returns nothing

    - search : given a bounded region, it returns a list of all entries that are
      contained within the region.

    - delete : given a particular entry, it deletes the entry if present. Returns
      nothing.
    """

    def __init__(self):

        self.Root = None  # The Root Node

    def insert(self, value):
        """ Finds a Leaf Node to the enter the value.

        It starts from the Root until it finds a leaf Node. If Root Node is the leaf Node,
        it inserts the entry in the leaf Node. If the Leaf Node overflows, it is split. Then
        the tree is traversed upwards, from the Leaf Node to the Root, adjusting the tree on
        during the process.

        Args:
        - self: the Tree in which the entry is being added, mandatory object refrence
        - value : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.

        Returns:
        Nothing.
        """

        if not self.Root:  # The R-Tree is empty, insert the value in the Root Node
            self.Root = TreeNode()
            self.Root.add(value)
        else:
            self._insert(value)

    def _insert(self, value):

        # A Flag Variable to check if the Root Node has been split.
        self.IsRootSplit = False
        # Finding the Leaf Node, to enter the value.
        LeafNode = self.ChooseLeaf(value)
        # Adds the entry in the LeafNode found.
        self.addRecord(LeafNode, value)

    def IsLeaf(self, Node):
        """ Checks if a Node is the Leaf Node

        A Node will be a Leaf Node if it does not point to any Node.

        Args:
        - self: mandatory object refrence
        - N : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.

        Returns:
        Returns a boolean variable that will be True if the Node is a Leaf Node
        """
        Flag = True

        # for entry in Node.EntryList:
        #     if entry == None:
        #         Flag = Flag and True # This means the Node contains less than two entries
        #     else:
        #         temp = (entry.getPointer() == None) # temp will be True, if the entry does not point to other Nodes.
        #         Flag = Flag and temp
        for i in range(2):
            if Node.EntryList[i] == None:
                Flag = Flag and True
            else:
                if Node.EntryList[i].Pointer == None:
                    Flag = Flag and True
                else:
                    Flag = False
        return Flag

    def addRecord(self, LeafNode, value):
        """ Enters the entry in the leaf Node.

        It inserts the entry in the Leaf Node.

        Args:
        - self: mandatory object refrence
        - LeafNode : the Leaf Node in which the entry is to be inserted.
        - value : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.

        Returns:

        Nothing.

        """

        # Inserts the Entry in the LeafNode. The number of the entries present in the LeafNode are Returned.
        N = LeafNode.add(value)

        SplitLeaf = None  #
        if N > 2:  # The Node has overflowed and needs to be split
            # The LeafNode is split into LeafNode and SplitLeaf
            LeafNode, SplitLeaf = self.splitNodes(LeafNode, value)

        # The Tree is then adjusted upwards. If the LeafNode is not split, then SplitLeaf will be None.
        LeafNode, SplitLeaf = self.adjustTree(LeafNode, SplitLeaf)

        # If the Root Node has been split, then the Root Node must be adjusted.
        if self.IsRootSplit:
            self.RootAdjust(LeafNode, SplitLeaf)

    def ChooseLeaf(self, value):
        """ Finds a Leaf Node to insert the entry.

        It starts from the Root Node and continues until it founds a Leaf Node. While the Leaf Node is not
        found, it will select the Node which requires the least amount of enlargement to store the entry.

        Args:
        - self: mandatory object refrence
        - value : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.

        Returns:

        Returns the Leaf Node in which the Entry will be added.

        """
        N = self.Root  # Set N equal to the Root Node
        # The stack will contain the path from the Root Node to the Leaf Node.
        self.Stack = list()
        self.Stack.append(N)
        while self.IsLeaf(N) != True:  # If N is not a Leaf Node Continue

            if N.EntryList[0] != None and N.EntryList[1] != None:
                # The Old Bounds & New Bounds of Entry 1
                Area_1 = self.EntryEnlarge(N.EntryList[0], value.MBR)
                # The Old Bounds & New Bounds of Entry 2
                Area_2 = self.EntryEnlarge(N.EntryList[1], value.MBR)
                Enlarge_L1 = (Area_1[7]-Area_1[6]) * (Area_1[5]-Area_1[4]) - \
                    (Area_1[3]-Area_1[2]) * (Area_1[1]-Area_1[0]
                                             )               # Diffrence in Area for Entry 1
                Enlarge_L2 = (Area_2[7]-Area_2[6]) * (Area_2[5]-Area_2[4]) - \
                    (Area_2[3]-Area_2[2]) * (Area_2[1]-Area_2[0])
                # Diffrence in Area for Entry 2
                if Enlarge_L1 < Enlarge_L2:   # Entry 1 requires a smaller change then Entry 2
                    N = N.EntryList[0].Pointer
                elif Enlarge_L1 > Enlarge_L2:  # Entry 1 requires a smaller change then Entry 2
                    N = N.EntryList[1].Pointer
                elif Enlarge_L1 == Enlarge_L2:
                    if N.EntryList[0].Pointer.N < N.EntryList[1].Pointer.N:
                        N = N.EntryList[0].Pointer
                    else:
                        N = N.EntryList[1].Pointer
            else:
                if N.EntryList[0] == None:
                    N = N.EntryList[1].Pointer
                else:
                    N = N.EntryList[0].Pointer

            self.Stack.append(N)         # Push the entry in the Stack
        self.Stack.pop(-1)
        return N

    def splitNodes(self, Node, value=None):
        """ Splits the Node into two Nodes : L1 & L2

        It inserts the entry in the Leaf Node.

        Args:
        - self: mandatory object refrence.
        - Node : the Node which is to be split.
        - value : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.

        Returns:

        Returns the two Nodes : the Original Node and the other Node that has been created as a result of Node Split.

        """

        # Checks if the Node that is being split is the Root Node
        self.IsRootSplit = Node is self.Root
        Entry_List = Node.EntryList
        min_x = min(Entry_List, key=lambda x: get(x, 0, 0))
        max_x = max(Entry_List, key=lambda x: get(x, 0, 1))
        min_y = min(Entry_List, key=lambda x: get(x, 1, 0))
        max_y = max(Entry_List, key=lambda x: get(x, 1, 1))

        w_x = abs(max_x.MBR[0][1]-min_x.MBR[0][0])  # Width Across the x-axis
        w_y = abs(max_y.MBR[1][1]-min_y.MBR[1][0])  # Width Across the y-axis

        # Seperation (L) per unit Width
        m1 = abs(Entry_List[0].MBR[1][1]-Entry_List[1].MBR[1][0])/w_y
        # Seperation (L) per unit Width
        m2 = abs(Entry_List[2].MBR[1][1]-Entry_List[1].MBR[1][0])/w_y
        # Seperation (L) per unit Width
        m3 = abs(Entry_List[0].MBR[1][1]-Entry_List[2].MBR[1][0])/w_y
        # Seperation (L) per unit Width
        m4 = abs(Entry_List[0].MBR[0][1]-Entry_List[1].MBR[0][0])/w_x
        # Seperation (L) per unit Width
        m5 = abs(Entry_List[2].MBR[0][1]-Entry_List[1].MBR[0][0])/w_x
        # Seperation (L) per unit Width
        m6 = abs(Entry_List[0].MBR[0][1]-Entry_List[2].MBR[0][0])/w_x

        lst = [m1, m2, m3, m4, m5, m6]

        # Picking Seeds (Selecting two Entries)
        # The pair of the entries which has the greatest Seperation (L) per unit width will be chosen

        if max(lst) == m1 or max(lst) == m4:
            e_1 = Entry_List[0]
            e_2 = Entry_List[1]
        elif max(lst) == m2 or max(lst) == m5:
            e_1 = Entry_List[2]
            e_2 = Entry_List[1]
        elif max(lst) == m3 or max(lst) == m6:
            e_1 = Entry_List[2]
            e_2 = Entry_List[0]

        L1 = TreeNode()
        L1.add(e_1)
        L2 = TreeNode()
        L2.add(e_2)
        # Adding the remaining entry to the group which requires the Least Amount of Enlargement.
        for e_i in Entry_List:
            if e_i != e_1 and e_i != e_2:
                # The Old Bounds & New Bounds of Node L1
                Area_1 = self.NodeEnlarge(L1, e_i.MBR)
                # The Old Bounds & New Bounds of Node L2
                Area_2 = self.NodeEnlarge(L2, e_i.MBR)
                Enlarge_L1 = (Area_1[7]-Area_1[6]) * (Area_1[5]-Area_1[4]) - \
                    (Area_1[3]-Area_1[2]) * (Area_1[1]-Area_1[0]
                                             )    # Diffrence in Area for Node L1
                Enlarge_L2 = (Area_2[7]-Area_2[6]) * (Area_2[5]-Area_2[4]) - \
                    (Area_2[3]-Area_2[2]) * (Area_2[1]-Area_2[0]
                                             )    # Diffrence in Area for Node L2
                if Enlarge_L1 < Enlarge_L2:   # Entry 1 requires a smaller change then Entry 2
                    L1.add(e_i)
                elif Enlarge_L2 < Enlarge_L1:  # Entry 1 requires a smaller change then Entry 2
                    L2.add(e_i)
                elif L1.N < L2.N:  # If both require same enlargement, then the entry is added to the node which lesser enteries
                    L1.add(e_i)
                else:
                    L2.add(e_i)
        # Determining wether L1 is the original Node or L2 is the original Node.
        for entry in L1.EntryList:
            if entry != None:
                if entry == value:
                    Node.EntryList = L2.EntryList
                    Node.N = L2.N
                    return Node, L1  # L2 is the original node

        Node.EntryList = L1.EntryList
        Node.N = L1.N
        return Node, L2  # L1 is the original node.

    def EntryEnlarge(self, entry, value):
        """ Calculates by how much does an Entry needs to be enlarged.

        Args:
        - self: mandatory object refrence
        - entry : the entry which needs to be enlarged.
        - value : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.


        Returns:

        Returns a List which contains the old & new bounds of the entry. [max_x, min_x, max_y, min_y,n_max_x, n_min_x, n_max_y, n_min_y]

        """

        max_x = entry.MBR[0][1]  # Maximum x-coordinate of the Entry
        min_x = entry.MBR[0][0]  # Minimum x-coordinate of the Entry
        max_y = entry.MBR[1][1]  # Maximum x-coordinate of the Entry
        min_y = entry.MBR[1][0]  # Minimum y-coordinate of the Entry

        n_max_x = 0  # New Maximum x-coordinate of the Entry
        n_min_x = 0  # New Minimum x-coordinate of the Entry
        n_max_y = 0  # New Maximum y-coordinate of the Entry
        n_min_y = 0  # New Minimum y-coordinate of the Entry
        # No change in the x-bounds (Containment)
        if (min_x <= value[0][0] <= max_x) and (min_x <= value[0][1] <= max_x):
            n_min_x = min_x
            n_max_x = max_x

        # min_x needs to  be lowered. (Partial Overlap)
        elif (value[0][0] < min_x) and (min_x <= value[0][1] <= max_x):
            n_min_x = value[0][0]
            n_max_x = max_x

        # max_x needs to be increased. (Partial Overlap)
        elif (min_x <= value[0][0] <= max_x) and (max_x < value[0][1]):

            n_min_x = min_x
            n_max_x = value[0][1]

        # the min_x needs to be lowered and the max_x needs to be increased.
        elif (value[0][0] < min_x) and (max_x < value[0][1]):
            n_min_x = value[0][0]
            n_max_x = value[0][1]

        # There is no overlap at all. The x max of the value is less than min_x
        elif (value[0][1] < min_x):
            n_min_x = value[0][0]
            n_max_x = max_x  # Old Max

        # There is no overlap at all. The x min of the value is greater than max_x
        elif (value[0][0] > max_x):
            n_min_x = min_x  # Old Min
            n_max_x = value[0][1]

        # No change in the y-bounds (Containment)
        if (min_y <= value[1][0] <= max_y) and (min_y <= value[1][1] <= max_y):
            n_min_y = min_y
            n_max_y = max_y

        # min_y needs to  be lowered. (Partial Overlap)
        elif (value[1][0] < min_y) and (min_y <= value[1][1] <= max_y):
            n_min_y = value[1][0]
            n_max_y = max_y

        # max_y needs to be increased. (Partial Overlap)
        elif (min_y <= value[1][0] <= max_y) and (max_y < value[1][1]):
            n_min_y = min_y
            n_max_y = value[1][1]

        # the min_y needs to be lowered and the max_y needs to be increased.
        if (value[1][0] < min_y) and (max_y < value[1][1]):
            n_min_y = value[1][0]
            n_max_y = value[1][1]

        # There is no overlap at all. The y max of the value is less than min_y
        if (value[1][1] < min_y):
            n_min_y = value[1][0]
            n_max_y = max_y  # Old Max

        # There is no overlap at all. The y min of the value is greater than max_y
        if (value[1][0] > max_y):
            n_min_y = min_y  # Old Min
            n_max_y = value[1][1]

        return list((max_x, min_x, max_y, min_y, n_max_x, n_min_x, n_max_y, n_min_y))

    def NodeEnlarge(self, Node, value):
        """ Calculates by how much does a Node needs to be enlarged.

        Args:
        - self: mandatory object refrence
        - Node : the entry which needs to be enlarged.
        - value : the MBR (Mininimum Bounding Region) of the the entry which is being inserted.


        Returns:

        Returns a List which contains the old & new bounds of the Node. [max_x, min_x, max_y, min_y,n_max_x, n_min_x, n_max_y, n_min_y]

        """

        max_x = Node.EntryList[0].MBR[0][1]  # Maximum x-coordinate of the Node
        for entry in Node.EntryList:
            if entry != None:
                max_x = max(max_x, entry.MBR[0][1])

        min_x = Node.EntryList[0].MBR[0][0]  # Minimum y-coordinate of the Node

        for entry in Node.EntryList:
            if entry != None:
                min_x = min(min_x, entry.MBR[0][0])

        max_y = Node.EntryList[0].MBR[1][1]  # Maximum y-coordinate of the Node

        for entry in Node.EntryList:
            if entry != None:
                max_y = max(max_y, entry.MBR[1][1])

        min_y = Node.EntryList[0].MBR[1][0]  # Minimum y-coordinate of the Node

        for entry in Node.EntryList:
            if entry != None:
                min_y = min(min_y, entry.MBR[1][0])

        n_max_x = 0  # New Maximum x-coordinate of the Node
        n_min_x = 0  # New Minimum x-coordinate of the Node
        n_max_y = 0  # New Maximum y-coordinate of the Node
        n_min_y = 0  # New Minimum y-coordinate of the Node

        # No change in the x-bounds (Containment)
        if (min_x <= value[0][0] <= max_x) and (min_x <= value[0][1] <= max_x):
            n_min_x = min_x
            n_max_x = max_x

        # min_x needs to  be lowered. (Partial Overlap)
        elif (value[0][0] < min_x) and (min_x <= value[0][1] <= max_x):
            n_min_x = value[0][0]
            n_max_x = max_x

        # max_x needs to be increased. (Partial Overlap)
        elif (min_x <= value[0][0] <= max_x) and (max_x < value[0][1]):

            n_min_x = min_x
            n_max_x = value[0][1]

        # the min_x needs to be lowered and the max_x needs to be increased.
        elif (value[0][0] < min_x) and (max_x < value[0][1]):
            n_min_x = value[0][0]
            n_max_x = value[0][1]

        # There is no overlap at all. The x max of the value is less than min_x
        elif (value[0][1] < min_x):
            n_min_x = value[0][0]
            n_max_x = max_x  # Old Max

        # There is no overlap at all. The x min of the value is greater than max_x
        elif (value[0][0] > max_x):
            n_min_x = min_x  # Old Min
            n_max_x = value[0][1]

        # No change in the y-bounds (Containment)
        if (min_y <= value[1][0] <= max_y) and (min_y <= value[1][1] <= max_y):
            n_min_y = min_y
            n_max_y = max_y

        # min_y needs to  be lowered. (Partial Overlap)
        elif (value[1][0] < min_y) and (min_y <= value[1][1] <= max_y):
            n_min_y = value[1][0]
            n_max_y = max_y

        # max_y needs to be increased. (Partial Overlap)
        elif (min_y <= value[1][0] <= max_y) and (max_y < value[1][1]):
            n_min_y = min_y
            n_max_y = value[1][1]

        # the min_y needs to be lowered and the max_y needs to be increased.
        if (value[1][0] < min_y) and (max_y < value[1][1]):
            n_min_y = value[1][0]
            n_max_y = value[1][1]

        # There is no overlap at all. The y max of the value is less than min_y
        if (value[1][1] < min_y):
            n_min_y = value[1][0]
            n_max_y = max_y  # Old Max

        # There is no overlap at all. The y min of the value is greater than max_y
        if (value[1][0] > max_y):
            n_min_y = min_y  # Old Min
            n_max_y = value[1][1]

        return list((max_x, min_x, max_y, min_y, n_max_x, n_min_x, n_max_y, n_min_y))

    def RootAdjust(self, N, NN):
        """ This creates a new Root whose children are the old root which was split and the extra node that was created due to the Root Split

        Args:
        - self: mandatory object refrence
        - N : the original Root which was split
        - NN : the extra Node which was created due to Root Split


        Returns:

        Returns a List which contains the old & new bounds of the Node. [max_x, min_x, max_y, min_y,n_max_x, n_min_x, n_max_y, n_min_y]

        """

        # This was done because N is the original Root
        tempNode = copy.deepcopy(N)

        # First Child of the New Node

        max_x = N.EntryList[0].MBR[0][1]  # Maximum x-coordinate of the Node
        for entry in N.EntryList:
            if entry != None:
                max_x = max(max_x, entry.MBR[0][1])

        min_x = N.EntryList[0].MBR[0][0]  # Minimum y-coordinate of the Node

        for entry in N.EntryList:
            if entry != None:
                min_x = min(min_x, entry.MBR[0][0])

        max_y = N.EntryList[0].MBR[1][1]  # Maximum y-coordinate of the Node

        for entry in N.EntryList:
            if entry != None:
                max_y = max(max_y, entry.MBR[1][1])

        min_y = N.EntryList[0].MBR[1][0]  # Minimum y-coordinate of the Node

        for entry in N.EntryList:
            if entry != None:
                min_y = min(min_y, entry.MBR[1][0])

        New_Entry = TreeEntry(([min_x, max_x], [min_y, max_y]))
        New_Entry.setPointer(tempNode)
        # Second Child of the New Node

        self.Root.EntryList[0] = New_Entry

        max_x = NN.EntryList[0].MBR[0][1]  # Maximum x-coordinate of the Node
        for entry in NN.EntryList:
            if entry != None:
                max_x = max(max_x, entry.MBR[0][1])

        min_x = NN.EntryList[0].MBR[0][0]  # Minimum y-coordinate of the Node

        for entry in NN.EntryList:
            if entry != None:
                min_x = min(min_x, entry.MBR[0][1])

        max_y = NN.EntryList[0].MBR[1][1]  # Maximum y-coordinate of the Node

        for entry in NN.EntryList:
            if entry != None:
                max_y = max(max_y, entry.MBR[1][1])

        min_y = NN.EntryList[0].MBR[1][0]  # Minimum y-coordinate of the Node

        for entry in NN.EntryList:
            if entry != None:
                min_y = min(min_y, entry.MBR[1][0])

        New_Entry1 = TreeEntry(([min_x, max_x], [min_y, max_y]))
        New_Entry1.setPointer(NN)

        self.Root.EntryList[1] = New_Entry1
        self.Root.N = 2

    def adjustTree(self, N, NN):
        """ This starts from the leaf Node and travels upto the Root.
        While Travelling upward, it adjusts the bounding node of the Parent Node. If the child Node was split, the other
        Node is added to the parent Node.

        Args:
        - self: mandatory object refrence
        - N : the original Node which was split
        - NN : the extra Node which was created due to Root Split


        Returns:

        Returns N & NN

        """
        while N is not self.Root:

            P = self.Stack.pop(-1)
            for index in range(len(P.EntryList)):

                if P.EntryList[index] is not None:
                    if P.EntryList[index].Pointer == N:

                        # Maximum x-coordinate of the Node
                        max_x = N.EntryList[0].MBR[0][1]
                        for entry in N.EntryList:
                            if entry != None:

                                max_x = max(max_x,  entry.MBR[0][1])

                        # Minimum y-coordinate of the Node
                        min_x = N.EntryList[0].MBR[0][0]

                        for entry in N.EntryList:
                            if entry != None:
                                min_x = min(min_x, entry.MBR[0][0])

                        # Maximum y-coordinate of the Node
                        max_y = N.EntryList[0].MBR[1][1]

                        for entry in N.EntryList:
                            if entry != None:
                                max_y = max(max_y, entry.MBR[1][1])

                        # Minimum y-coordinate of the Node
                        min_y = N.EntryList[0].MBR[1][0]

                        for entry in N.EntryList:
                            if entry != None:
                                min_y = min(min_y, entry.MBR[1][0])

                        # The Bounds of the Node N
                        value = ([min_x, max_x], [min_y, max_y])

                        # Enlarged Bounds of the Parent Node P
                        Area = self.EntryEnlarge(P.EntryList[index], value)
                        temp = TreeEntry(
                            ([Area[5], Area[4]], [Area[7], Area[6]]))
                        temp.setPointer(N)
                        P.EntryList[index] = temp

            if NN is not None:  # If N was split then add NN to P
                # Maximum x-coordinate of the Node
                max_x = NN.EntryList[0].MBR[0][1]
                for entry in NN.EntryList:
                    if entry != None:
                        max_x = max(max_x, entry.MBR[0][1])

                # Minimum y-coordinate of the Node
                min_x = NN.EntryList[0].MBR[0][0]

                for entry in NN.EntryList:
                    if entry != None:
                        min_x = min(min_x, entry.MBR[0][0])

                # Maximum y-coordinate of the Node
                max_y = NN.EntryList[0].MBR[1][1]

                for entry in NN.EntryList:
                    if entry != None:
                        max_y = max(max_y, entry.MBR[1][1])

                # Minimum y-coordinate of the Node
                min_y = NN.EntryList[0].MBR[1][0]

                for entry in NN.EntryList:
                    if entry != None:
                        min_y = min(min_y, entry.MBR[1][0])

                value = ([min_x, max_x], [min_y, max_y])
                entry = TreeEntry(value)
                entry.setPointer(NN)
                Num = P.add(entry)
                if Num > 2:  # If Adding NN to P causes it to overflow, then split P into P,PP
                    N, NN = self.splitNodes(P)

            elif NN is None:
                N = P

        return N, NN

    def Overlap(self, boxA, boxB):
        # print(boxA[0][0][0], boxB[0][0],boxB[0][1],boxA[0][0][1],boxB[0][0],boxA[0][0][0],boxB[0][0],boxA[0][0][1],boxB[0][1],boxA[0][0][1])
        if (boxA.MBR[0][0] <= boxB[0][0] and boxB[0][1] <= boxA.MBR[0][1]) or (boxB[0][0] >= boxA.MBR[0][0] and boxB[0][0] <= boxA.MBR[0][1] and boxB[0][1] >= boxA.MBR[0][1]) or (boxB[0][0] <= boxA.MBR[0][0] and boxB[0][0] <= boxA.MBR[0][1] and boxB[0][1] >= boxA.MBR[0][1]):
            overlapx = 1
        else:
            overlapx = 0
        # print(boxA[0][1][0] , boxB[1][0] , boxB[1][1],boxA[0][1][1],boxB[1][0],boxA[0][1][0],boxB[1][0],boxA[0][1][1],boxB[1][1],boxA[0][1][1])
        if (boxA.MBR[1][0] <= boxB[1][0] and boxB[1][1] <= boxA.MBR[1][1]) or (boxB[1][0] >= boxA.MBR[1][0] and boxB[1][0] <= boxA.MBR[1][1] and boxB[1][1] >= boxA.MBR[1][1]) or (boxB[1][0] <= boxA.MBR[1][0] and boxB[1][0] <= boxA.MBR[1][1] and boxB[1][1] >= boxA.MBR[1][1]):
            overlapy = 1
        else:
            overlapy = 0
        if overlapx == 1 and overlapy == 1:
            return boxA

    def Search(self, root, value, lst=None):
        if root.EntryList[1] != None or root.EntryList[0].Pointer != None:
            for i in root.EntryList:
                if not self.IsLeaf(root) and i != None:  # if not leaf
                    a = self.Overlap(i, value)
                    if lst == None:
                        lst = []
                    if a == None:
                        continue
                    else:
                        if i.Pointer.EntryList[0].Pointer == None and i.MBR[0][0] >= value[0][0] and i.MBR[0][1] <= value[0][1] and i.MBR[1][0] >= value[1][0] and i.MBR[1][1] <= value[1][1] and i.Pointer.EntryList[0] not in lst:
                            lst.append(i.Pointer.EntryList[0])

                        self.Search(a.Pointer, value, lst)
                else:  # if leaf
                    for i in root.EntryList:
                        if i != None and i.Pointer == None and i not in lst and i.MBR[0][0] >= value[0][0] and i.MBR[0][1] <= value[0][1] and i.MBR[1][0] >= value[1][0] and i.MBR[1][1] <= value[1][1]:
                            lst.append(i)
        else:
            return [root.EntryList[0]]
        return lst


# tree = RTree()

# # a1 = TreeEntry(([338, 131], [460, 227]), "Spar")
# # b1 = TreeEntry(([421, 144], [546, 201]), "Imtiaz")
# # c1 = TreeEntry(([515, 169], [638, 217]), "AL-Jadeed")
# # d1 = TreeEntry(([541, 158], [607, 205]), "Naheed")
# # e1 = TreeEntry(([640, 134], [765, 223]), "Chase UP")
# # f1 = TreeEntry(([2, 5], [7, 8]), "Chase")
# # Insert-BoundingBox{(338.0, 131.0)(460.0, 227.0)}
# # Insert-BoundingBox{(421.0, 144.0)(546.0, 201.0)}
# # Insert-BoundingBox{(515.0, 169.0)(638.0, 217.0)}
# # Insert-BoundingBox{(541.0, 158.0)(607.0, 205.0)}
# # Insert-BoundingBox{(640.0, 134.0)(765.0, 223.0)}
# a1 = TreeEntry(([1, 7], [1, 5]), "Spar")
# b1 = TreeEntry(([8, 14], [1, 5]), "Imtiaz")
# c1 = TreeEntry(([15, 20], [5, 10]), "AL-Jadeed")
# d1 = TreeEntry(([12, 13], [2, 3]), "Naheed")
# e1 = TreeEntry(([1, 10], [6, 8]), "Chase UP")
# f1 = TreeEntry(([2, 5], [7, 8]), "Chase")
# tree.insert(a1)
# tree.insert(b1)
# tree.insert(c1)
# tree.insert(d1)
# tree.insert(e1)
# tree.insert(f1)

# # print(tree.Root.EntryList[0].Pointer.EntryList[0].Pointer.EntryList[0].Pointer.EntryList[0].MBR,tree.Root.EntryList[0].Pointer.EntryList[0].Pointer.EntryList[0].Pointer.EntryList[1])
# # print(tree.Root.EntryList[0].MBR, tree.Root.EntryList[0].Pointer)
# # print(tree.Root.EntryList[1].MBR, tree.Root.EntryList[1].Pointer)
# # print(tree.Root.EntryList[1].Pointer.EntryList[0].MBR)
# # print(tree.Root.EntryList[0].Pointer.EntryList[0].Pointer.EntryList[0].MBR)
# # print(tree.Root.EntryList[1])
# # print(tree.Root.Pointer)
# # print(tree.Root.Pointer[0][1].Pointer)
# # print(tree.Root.Pointer[1][1].Pointer)
# # print(tree.Root.Pointer[0][1].Pointer[0][1].Pointer)
# # print(tree.Root.Pointer[1][1].Pointer[0][1].Pointer)
# # print(tree.Root.Pointer[1][1].Pointer[1][1].Pointer)

# # # lst = (tree.Search(tree.Root, ([640, 134], [765, 223])))
# lst = (tree.Search(tree.Root, ([15, 20], [5,10 ])))
# print(lst)
# for i in lst:
#     # print(i)
#     print(i.Name)
