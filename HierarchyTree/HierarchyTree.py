from anytree import Node, RenderTree
import ImagenetClassFilter
import NaverGoodsTreeConverter

'''
HierarchyTree
    계층트리 클래스
    기능
        1. 트리 생성
        2. 키워드로 노드 검색 후 연결된 노드들 리턴(부모 노드들, 자신, 자식 노드들)
        3. 트리 전체 출력
'''


# TODO : ImageNet Tree 붙여서 구성하기

class HierarchyTree:
    def __init__(self, hierarchyTree, trainingLabel, wnid2name):
        self.hierarchyTreeFile = hierarchyTree
        self.node_set = []
        self.content = {}
        self.icFilter = ImagenetClassFilter.ImagenetClassFilter(trainingLabel, wnid2name)
        self.ngtConverter = NaverGoodsTreeConverter.NaverGoodsTreeConverter()

    def makeHierarchyTree(self):
        self.icFilter.makeTrainingLabelSet()
        self.icFilter.makeWnid2NameMap()
        f = open(self.hierarchyTreeFile, 'r', encoding='UTF-8')

        self.node_set.append(Node(0, data="root"))
        self.node_set.append(Node(1, data="n00001740", parent=self.node_set[0]))
        self.node_set.append(Node(2, data="상품", parent=self.node_set[0]))

        self.content["root"] = 0
        self.content["n00001740/entity"] = 1
        self.content["상품"] = 2

        while True:
            dat = f.readline()
            if not dat: break
            dat = dat.replace("\n","",1)
            parent = dat.split()[0]
            child = dat.split()[1]

            if not self.checkIfKeyExists((parent, child)):
                continue

            parent = self.getData(parent)
            child = self.getData(child)

            if parent not in self.content.keys():
                self.content[parent] = len(self.node_set)
                self.node_set.append(Node(len(self.node_set), data=parent))
            if child in self.content.keys():
                self.node_set[self.content[child]].parent = self.node_set[self.content[parent]]
                continue
            self.content[child] = len(self.node_set)
            self.node_set.append(Node(len(self.node_set), data=child, parent=self.node_set[self.content[parent]]))

        f.close()

        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            if node.is_leaf:
                if self.is_in_training_dataset(node.data):
                    continue
                else:
                    parent_node = node.parent
                    node.parent = None
                    del node
                    while(len(parent_node.children) == 0):
                        tmp_node = parent_node.parent
                        parent_node.parent = None
                        del parent_node
                        parent_node = tmp_node

    def is_in_training_dataset(self, keyword):
        if keyword[0] != "n" or self.icFilter.is_name_in_trainingLabel(keyword):
            return True
        else:
            return False

    def getData(self, wnid):
        if wnid[0] != "n":
            return wnid
        return wnid + "/" + self.icFilter.getData(wnid)

    def checkIfKeyExists(self, key):
        if key[0][0] != "n":
            return True
        if self.icFilter.check_wnid_in_wnid2key(key[0]) and self.icFilter.check_wnid_in_wnid2key(key[1]):
            return True
        else:
            return False

    def searchKeyword(self, keyword):
        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            if keyword in node.data:
                return self.getRelatedNodes(node)

    def getRelatedNodes(self, node):
        result = []
        result.append(self.getParents(node))
        result.append(self.getChildren(node))
        return result

    def getChildren(self, node):
        children = []
        for row in RenderTree(node):
            pre, fill, node = row
            children.append(node.data)
        return children

    def getParents(self, node):
        parents = []
        while True:
            if node.parent:
                parents.append(node.parent.data)
                node = node.parent
            else:
                break
        return parents

    def showTree(self):
        print("==" * 20)
        print("==" * 8 + "트리정보" + "==" * 8)
        print("==" * 20)
        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            print(f"{pre}{node.name}, data: {node.data}")
        print("==" * 20)

    def showTreeP2Cformat(self):
        with open("NaverGoodsTreeP2C.txt", "w", encoding="UTF-8") as f:
           for row in RenderTree(self.node_set[0]):
               pre, fill, node = row
               if node.data == "상품":
                   continue
               f.write(f"{node.parent.data} {node.data}\n")

if __name__ == "__main__":
    ht = HierarchyTree("HierarchyTree.dat", "Imagenet.txt", "wnid2name.txt")
    ht.makeHierarchyTree()
    print(f'keyword : 옷의류 result : {ht.searchKeyword("패션의류")}')
    print(f'keyword : 러닝 result : {ht.searchKeyword("러닝")}')
    print(f'keyword : 신발 result : {ht.searchKeyword("신발")}')
    ht.showTree()
