from anytree import Node, RenderTree
from FilePath import FilePathGetter

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
    def __init__(self):
        self.file_name = FilePathGetter.getNaverGoodsTreeFilePath()
        self.node_set = []
        self.content = {}

    def makeFinalContent(self):
        f = open("finalTree.txt", 'r', encoding='UTF-8')

        self.node_set.append(Node(0, data="root"))
        self.node_set.append(Node(1, data="n00001740", parent=self.node_set[0]))
        self.node_set.append(Node(2, data="상품", parent=self.node_set[0]))

        self.content["root"] = 0
        self.content["n00001740"] = 1
        self.content["상품"] = 2
#        self.content.append({"root":0})
#        self.content.append({"n00001740":1})
#        self.content.append({"상품":2})
#
        while True:
            dat = f.readline()
            if not dat: break
            parent = dat.split()[0]
            child = dat.split()[1]
            if parent not in self.content.keys():
                self.content[parent] = len(self.node_set)
                self.node_set.append(Node(len(self.node_set), data=parent))
            if child in self.content.keys():
                self.node_set[self.content[child]].parent = self.node_set[self.content[parent]]
                continue
            self.content[child] = len(self.node_set)
            self.node_set.append(Node(len(self.node_set), data=child, parent=self.node_set[self.content[parent]]))

        f.close()

    def makeContent(self):
        f = open(self.file_name, 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line: break
            self.content.append((line.count("\t"), line.replace("\n", "").replace("\t", "", len(line))))
        f.close()

    def makeTree(self):
        self.makeContent()
        self.node_set.append(Node(f'node_{0}', data=self.content[0][1]))
        self.makeTree_sub(0)

    def makeTree_sub(self, nodeNum):
        while True:
            if (len(self.content) == len(self.node_set)) or (
                    self.content[nodeNum][0] > self.content[len(self.node_set)][0] - 1):
                return
            elif self.content[nodeNum][0] == self.content[len(self.node_set)][0] - 1:
                self.node_set.append(Node(f'node_{len(self.node_set)}', parent=self.node_set[nodeNum],
                                          data=self.content[len(self.node_set)][1]))
            elif self.content[nodeNum][0] < self.content[len(self.node_set)][0] - 1:
                self.makeTree_sub(len(self.node_set) - 1)

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
        for i in range(29):
            print(f'{i} {self.node_set[i].data}')
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
#            print(f"{node.parent.data} {node.data}")

if __name__ == "__main__":
    ht = HierarchyTree()
    ht.makeFinalContent()
#    print(f'keyword : 패션의류 result : {ht.searchKeyword("패션의류")}')
#    print(f'keyword : 러닝 result : {ht.searchKeyword("러닝")}')
#    print(f'keyword : 신발 result : {ht.searchKeyword("신발")}')
#    ht.showTree()
    ht.showTree()
