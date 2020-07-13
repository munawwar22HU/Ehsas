import copy


class TreeNode:
    def __init__(self):
        # Node Pointer. If it is a leaf Node it will be None. If it is a Non-Leaf node it will point to a another Node
        self.Pointer = [None] * 2
        self.N = 0  # Number of Node
        self.IsOverflow = False

    def add(self, E):
        if self.N < 2:
            self.Pointer[self.N] = E
        else:
            self.Pointer.append(E)
        self.N += 1

        return self.N

    def __str__(self):
        return str(self.Pointer)


class RTree:
    def __init__(self):

        self.M = 2  # The maximum entries  a Node can contain.
        self.Root = None

    def insert(self, I):
        if not self.Root:
            self.Root = TreeNode()
            self.Root.add([I, None])
        else:
            self._insert(I)

    def _insert(self, value):
        self.IsRootSplit = False
        LeafNode = self.ChooseLeaf(value)
        self.addRecord(LeafNode, value)

    def IsLeaf(self, N):
        Flag = True

        for i in N.Pointer:
            if i == None:
                Flag = Flag and True
            else:
                temp = (i[1] == None)
                Flag = Flag and temp
        return Flag

    def splitNodes(self, Node, value=None):
        self.IsRootSplit = Node is self.Root
        Entry_List = Node.Pointer

        min_x = min(Entry_List, key=lambda x: x[0][0][0])
        max_x = max(Entry_List, key=lambda x: x[0][0][1])
        min_y = min(Entry_List, key=lambda x: x[0][1][0])
        max_y = min(Entry_List, key=lambda x: x[0][1][1])
        w_x = abs(max_x[0][0][1]-min_x[0][0][0])
        w_y = abs(max_y[0][1][1]-min_y[0][1][0])

        m1 = abs(Entry_List[0][0][1][1]-Entry_List[1][0][1][0])/w_y
        m2 = abs(Entry_List[2][0][1][1]-Entry_List[1][0][1][0])/w_y
        m3 = abs(Entry_List[0][0][1][1]-Entry_List[2][0][1][0])/w_y
        m4 = abs(Entry_List[0][0][0][1]-Entry_List[1][0][0][0])/w_x
        m5 = abs(Entry_List[2][0][0][1]-Entry_List[1][0][0][0])/w_x
        m6 = abs(Entry_List[0][0][0][1]-Entry_List[2][0][0][0])/w_x

        lst = [m1, m2, m3, m4, m5, m6]

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

        for e_i in Entry_List:
            if e_i != e_1 and e_i != e_2:

                Area_1 = self.MinEnlarge(L1, e_i[0])
                Area_2 = self.MinEnlarge(L2, e_i[0])
                Enlarge_L1 = (Area_1[7]-Area_1[6]) * (Area_1[5]-Area_1[4]) - \
                    (Area_1[3]-Area_1[2]) * (Area_1[1]-Area_1[0])
                Enlarge_L2 = (Area_2[7]-Area_2[6]) * (Area_2[5]-Area_2[4]) - \
                    (Area_2[3]-Area_2[2]) * (Area_2[1]-Area_2[0])
                if Enlarge_L1 < Enlarge_L2:
                    L1.add(e_i)
                elif Enlarge_L2 < Enlarge_L1:
                    L2.add(e_i)
                elif L1.N < L2.N:
                    L1.add(e_i)
                else:
                    L2.add(e_i)

        for i in L1.Pointer:
            if i != None:
                if i[0] == value:
                    Node.Pointer = L2.Pointer
                    Node.N = len(Node.Pointer)
                    L1.N = len(L1.Pointer)
                    return Node, L1

        Node.Pointer = L1.Pointer
        Node.N = len(Node.Pointer)
        L2.N = len(L2.Pointer)

        return Node, L2

    def MinEnlarge(self, Li, e_i):

        max_x = Li.Pointer[0][0][0][1]
        for i in Li.Pointer:
            if i != None:
                max_x = max(max_x, i[0][0][1])

        min_x = Li.Pointer[0][0][0][0]
        for i in Li.Pointer:
            if i != None:
                min_x = min(min_x, i[0][0][1])
        max_y = Li.Pointer[0][0][1][1]
        for i in Li.Pointer:
            if i != None:
                max_y = max(max_y, i[0][1][1])

        min_y = Li.Pointer[0][0][1][0]
        for i in Li.Pointer:
            if i != None:
                min_y = min(min_y, i[0][1][0])

        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0

        # 1 < 3 < 6  & 1 < 4 < 6 Containment
        if (min_x <= e_i[0][0] <= max_x) and (min_x <= e_i[0][1] <= max_x):
            c1 = min_x
            c2 = max_x

        # 2 < 3 & 3 < 4 < 6  Right Overlap
        if (e_i[0][0] < min_x) and (min_x <= e_i[0][1] <= max_x):

            c2 = max_x
            c1 = e_i[0][0]

        # 1 < 3 < 6 & 7>6     Left Overlap
        if (min_x <= e_i[0][0] <= max_x) and (max_x < e_i[0][1]):

            c1 = min_x

            c2 = e_i[0][1]

        if (e_i[0][0] < min_x) and (max_x < e_i[0][1]):                 # 1 < 3 & 7 >6

            c2 = e_i[0][1]
            c1 = e_i[0][0]

        if (e_i[0][1] < min_x):                               # 1 < 3 < 4 < 6
            c1 = e_i[0][0]
            c2 = max_x

        if (e_i[0][0] > max_x):
            c1 = min_x
            c2 = e_i[0][1]

        if (min_y <= e_i[1][0] <= max_y) and (min_y <= e_i[1][1] <= max_y):
            c3 = min_y
            c4 = max_y

        if (e_i[1][0] < min_y) and (min_y <= e_i[1][1] <= max_y):

            c4 = max_y
            c3 = e_i[1][0]

        if (min_y <= e_i[1][0] <= max_y) and (max_y < e_i[1][1]):
            c3 = min_y
            # c2 = max_x + e_lx
            c4 = e_i[1][1]

        if (e_i[1][0] < min_y) and (max_y < e_i[1][1]):
            c4 = e_i[1][1]
            c3 = e_i[1][0]

        if (e_i[1][1] < min_y):
            c3 = e_i[1][0]
            c4 = max_y

        if (e_i[1][0] > max_y):
            c3 = min_y
            c4 = e_i[1][1]

        return list((max_x, min_x, max_y, min_y, c2, c1, c4, c3))

    def addRecord(self, L, value):

        x = L.add([value, None])

        X = None
        if x > 2:
            L, X = self.splitNodes(L, value)
        L, X = self.adjustTree(L, X)

        if self.IsRootSplit:
            self.RootAdjust(L, X)

    def RootAdjust(self, N, NN):

        tempNode = copy.deepcopy(N)

        max_x = N.Pointer[0][0][0][1]
        for i in N.Pointer:
            if i != None:
                max_x = max(max_x, i[0][0][1])

        min_x = N.Pointer[0][0][0][0]
        for i in N.Pointer:
            if i != None:
                min_x = min(min_x, i[0][0][0])

        max_y = N.Pointer[0][0][1][1]

        for i in N.Pointer:
            if i != None:
                max_y = max(max_y, i[0][1][1])

        min_y = N.Pointer[0][0][1][0]
        for i in N.Pointer:
            if i != None:
                min_y = min(min_y, i[0][1][0])

        New_Entry = [([min_x, max_x], [min_y, max_y]), tempNode]
        self.Root.Pointer[0] = New_Entry

        max_x = NN.Pointer[0][0][0][1]
        for i in NN.Pointer:
            if i != None:
                max_x = max(max_x, i[0][0][1])

        min_x = NN.Pointer[0][0][0][0]
        for i in NN.Pointer:
            if i != None:
                min_x = min(min_x, i[0][0][0])

        max_y = NN.Pointer[0][0][1][1]

        for i in NN.Pointer:
            if i != None:
                max_y = max(max_y, i[0][1][1])

        min_y = NN.Pointer[0][0][1][0]
        for i in NN.Pointer:
            if i != None:
                min_y = min(min_y, i[0][1][0])

        New_Entry = [([min_x, max_x], [min_y, max_y]), NN]
        self.Root.Pointer[1] = New_Entry

    def ChooseLeaf(self, value):
        N = self.Root
        self.Stack = list()
        self.Stack.append(N)
        while self.IsLeaf(N) != True:
            if N.Pointer[0]!=None and N.Pointer[1]!=None:
                Area_1 = self.NewMinEnlarge(N.Pointer[0][0], value)
                Area_2 = self.NewMinEnlarge(N.Pointer[1][0], value)
                Enlarge_L1 = (Area_1[7]-Area_1[6]) * (Area_1[5]-Area_1[4]) - \
                    (Area_1[3]-Area_1[2]) * (Area_1[1]-Area_1[0])
                Enlarge_L2 = (Area_2[7]-Area_2[6]) * (Area_2[5]-Area_2[4]) - \
                    (Area_2[3]-Area_2[2]) * (Area_2[1]-Area_2[0])

                if Enlarge_L1 < Enlarge_L2:
                    N = N.Pointer[0][1]
                elif Enlarge_L1 > Enlarge_L2:
                    N = N.Pointer[1][1]
            else:
                print(N.Pointer[1]==None)
            
                if N.Pointer[0]==None:
                    
                    N = N.Pointer[1][1]
                elif N.Pointer[1]==None:
                    print("iDHER")
                    N = N.Pointer[0][1]
                    print(N)
            self.Stack.append(N)
        self.Stack.pop(-1)
        return N

    def adjustTree(self, N, NN):

        while N is not self.Root:

            P = self.Stack.pop(-1)

            for index in range(len(P.Pointer)):
                if P.Pointer[index] is not None:
                    if P.Pointer[index][1] is N:
                        max_x = N.Pointer[0][0][0][1]  # Max x-value
                        for i in N.Pointer:
                            if i != None:
                                max_x = max(max_x, i[0][0][1])

                        min_x = N.Pointer[0][0][0][0]  # Min x-value
                        for i in N.Pointer:
                            if i != None:
                                min_x = min(min_x, i[0][0][0])

                        max_y = N.Pointer[0][0][1][1]    # Max y-value
                        for i in N.Pointer:
                            if i != None:
                                max_y = max(max_y, i[0][1][1])

                        min_y = N.Pointer[0][0][1][0]   # Min y-value
                        for i in N.Pointer:
                            if i != None:
                                min_y = min(min_y, i[0][1][0])

                        value = ([min_x, max_x], [min_y, max_y])

                        Area = self.NewMinEnlarge(P.Pointer[index][0], value)

                        P.Pointer[index] = [
                            ([Area[5], Area[4]], [Area[7], Area[6]]), N]

                        break

            if NN is not None:
                max_x = NN.Pointer[0][0][0][1]  # Max x-value
                for i in NN.Pointer:
                    if i != None:
                        max_x = max(max_x, i[0][0][1])

                min_x = NN.Pointer[0][0][0][0]  # Min x-value
                for i in NN.Pointer:
                    if i != None:
                        min_x = min(min_x, i[0][0][0])

                max_y = NN.Pointer[0][0][1][1]    # Max y-value
                for i in NN.Pointer:
                    if i != None:
                        max_y = max(max_y, i[0][1][1])

                min_y = NN.Pointer[0][0][1][0]   # Min y-value
                for i in NN.Pointer:
                    if i != None:
                        min_y = min(min_y, i[0][1][0])

                value = ([min_x, max_x], [min_y, max_y])
                flag = P.add([value, NN])
                if flag > 2:
                    N, NN = self.splitNodes(P)

            elif NN is None:
                N = P

        return N, NN

    def NewMinEnlarge(self, Li, e_i):

        max_x = Li[0][1]
        min_x = Li[0][0]
        max_y = Li[1][1]
        min_y = Li[1][0]

        e_lx = 0
        e_ly = 0
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0

        if (min_x <= e_i[0][0] <= max_x) and (min_x <= e_i[0][1] <= max_x):
            c1 = min_x
            c2 = max_x

        if (e_i[0][0] < min_x) and (min_x <= e_i[0][1] <= max_x):
            e_lx = min_x-e_i[0][0]
            c2 = max_x
            c1 = min_x - e_lx

        if (min_x <= e_i[0][0] <= max_x) and (max_x < e_i[0][1]):

            e_lx = e_i[0][1] - max_x
            c1 = min_x
            c2 = max_x + e_lx

        if (e_i[0][0] < min_x) and (max_x < e_i[0][1]):

            e_lx = e_i[0][0] - max_x
            c2 = max_x + e_lx

            e_lx = min_x-e_i[0][1]
            c1 = min_x - e_lx

        if (e_i[0][1] < min_x):
            c1 = e_i[0][0]
            c2 = max_x

        if (e_i[0][0] > max_x):
            c1 = min_x
            c2 = e_i[0][1]

        if (min_y <= e_i[1][0] <= max_y) and (min_y <= e_i[1][1] <= max_y):
            c3 = min_y
            c4 = max_y

        if (e_i[1][0] < min_y) and (min_y <= e_i[1][1] <= max_y):
            e_ly = min_y-e_i[1][0]
            c4 = max_y
            c3 = min_y - e_ly

        if (min_y <= e_i[1][0] <= max_y) and (max_y < e_i[1][1]):
            e_ly = e_i[1][1] - max_y

            c3 = min_y
            c4 = max_y + e_ly

        if (e_i[1][0] < min_y) and (max_y < e_i[1][1]):
            e_ly = e_i[1][0] - max_y
            c4 = max_y + e_ly

            e_ly = min_y-e_i[1][1]
            c3 = min_y - e_ly

        if (e_i[1][1] < min_y):
            c3 = e_i[1][0]
            c4 = max_y

        if (e_i[1][0] > max_y):
            c3 = min_y
            c4 = e_i[1][1]

        return list((max_x, min_x, max_y, min_y, c2, c1, c4, c3))

    def Overlap(self, boxA, boxB):
        if (boxA[0][0][0] <= boxB[0][0] and boxB[0][1] <= boxA[0][0][1]) or (boxB[0][0] >= boxA[0][0][0] and boxB[0][0] <= boxA[0][0][1] and boxB[0][1] >= boxA[0][0][1]) or (boxB[0][0] <= boxA[0][0][0] and boxB[0][0] <= boxA[0][0][1] and boxB[0][1] >= boxA[0][0][1]):
            # if (boxA[0][0][0] <= boxB[0][0] and boxB[1][0] <= boxA[0][1][0]) or (boxB[0][0] >= boxA[0][0][0] and boxB[0][0] <= boxA[0][1][0] and boxB[1][0] >= boxA[0][1][0]) or (boxB[0][0] <= boxA[0][0][0] and boxB[0][0] <= boxA[0][1][0] and boxB[1][0] >= boxA[0][1][0]):
            #print(boxA[0][0][0], boxB[0][0] ,boxB[1][0], boxA[0][1][0] ,"h",boxB[0][0] , boxA[0][0][0] ,boxB[0][0], boxA[0][1][0] ,boxB[1][0],boxA[0][1][0],boxB[0][0],boxA[0][0][0], boxB[0][0], boxA[0][1][0],boxB[1][0], boxA[0][1][0])
            overlapx = 1
        else:
            overlapx = 0
        #print(boxA, boxB, boxA[0][0][1], boxB[0][1], boxB[1][1], boxA[0][1][1],"H", boxB[1][1], boxA[0][0][1], boxB[1][1], boxA[0][1][1], boxB[1][1],"h", boxA[0][1][1], boxB[0][1], boxA[0][0][1], boxB[0][1], boxA[0][1][1], boxB[1][1], boxA[0][1][1])
        # if (boxA[0][0][1] <= boxB[0][1] and boxB[1][1] <= boxA[0][1][1]) or (boxB[1][1] >= boxA[0][0][1] and boxB[1][1] <= boxA[0][1][1] and boxB[1][1] >= boxA[0][1][1]) or (boxB[1][0] <= boxA[0][0][1] and boxB[0][1] <= boxA[0][1][1] and boxB[1][1] >= boxA[0][1][1]):
        if (boxA[0][1][0] <= boxB[1][0] and boxB[1][1] <= boxA[0][1][1]) or (boxB[1][0] >= boxA[0][1][0] and boxB[1][0] <= boxA[0][1][1] and boxB[1][1] >= boxA[0][1][1]) or (boxB[1][0] <= boxA[0][1][0] and boxB[1][0] <= boxA[0][1][1] and boxB[1][1] >= boxA[0][1][1]):
            overlapy = 1
        else:
            overlapy = 0
        if overlapx == 1 and overlapy == 1:
            return boxA

    def Search(self, root, TypeRegion, lst=None):
        if root.Pointer[1] != None:
            if not self.IsLeaf(root):  # if not leaf
                for i in root.Pointer:
                    a = self.Overlap(i, TypeRegion)
                    if lst == None:
                        lst = []
                    if a == None:
                        continue
                    else:
                        if i[1].Pointer[0][1] == None and i[0][0][0] >= TypeRegion[0][0] and i[0][0][1] <= TypeRegion[0][1] and i[0][1][0] >= TypeRegion[1][0] and i[0][1][1] <= TypeRegion[1][1]:
                            lst.append(i[1].Pointer[0][0])

                            #print(self.IsLeaf(i[1]), i[1])
                        # elif self.IsLeaf(a[1].Pointer[0][1]) == True and i[0][0][0] >= TypeRegion[0][0] and i[0][0][1] <= TypeRegion[0][1] and i[0][1][0] >= TypeRegion[1][0] and i[0][1][1] <= TypeRegion[1][1]:
                        #     lst.append(a[1].Pointer[0][1].Pointer[0][0])
                        #     print(self.IsLeaf(
                        #         a[1]), a[1].Pointer[1], self.IsLeaf(a[1].Pointer[0][1]))
                            # a[1].Pointer[0][1].Pointer[0][1] == None
                        elif a[1].Pointer[1] == None and i[0][0][0] >= TypeRegion[0][0] and i[0][0][1] <= TypeRegion[0][1] and i[0][1][0] >= TypeRegion[1][0] and i[0][1][1] <= TypeRegion[1][1]:
                            lst.append(a[1].Pointer[0][1].Pointer[0][0])
                            # print(self.IsLeaf(a[1]), self.IsLeaf(a[1].Pointer[0][1]), a[1].Pointer[0][1])
                        self.Search(a[1], TypeRegion, lst)
            else:  # if leaf
                for i in root.Pointer:
                    if i[0] not in lst and i[0][0][0] >= TypeRegion[0][0] and i[0][0][1] <= TypeRegion[0][1] and i[0][1][0] >= TypeRegion[1][0] and i[0][1][1] <= TypeRegion[1][1]:
                        lst.append(i[0])
        return lst


tree = RTree()

tree.insert(([1, 7], [4, 5]))
tree.insert(([8, 14], [1, 5]))
tree.insert(([5, 10], [2, 4]))
tree.insert(([12, 13], [2, 3]))
tree.insert((([1, 10], [6, 8])))
print("Root")
print(tree.Root.Pointer)
print(tree.Root.Pointer[0][1].Pointer)
print(tree.Root.Pointer[1][1].Pointer)
print(tree.Root.Pointer[0][1].Pointer[0][1].Pointer)
print(tree.Root.Pointer[1][1].Pointer[0][1].Pointer)
print(tree.Root.Pointer[1][1].Pointer[1][1].Pointer)
print(tree.Search(tree.Root, ([1, 14], [1, 6])))
