import re
from anytree import Node, RenderTree

'''
    NaverGoodsTreeConverter
    기능
        tab으로 이루어진 트리를 parent child 포맷으로 출력시켜준다.
        makeContent()
        makeTree()
        하면 트리가 만들어진다.
        showTree()
        하면 트리 출력
        showTreeP2Cformat()
        하면 parent child 포맷으로 출력
'''
class NaverGoodsTreeConverter:
    def __init__(self):
        self.naverGoodsPath = "NaverGoodsTree.txt"
        self.targetPath = "NaverGoodsTreeP2C.txt"
        self.node_set = []
        self.content = []

    def makeContent(self):
        f = open(self.naverGoodsPath, 'r', encoding='UTF8')
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

    def showTree(self):
        print("==" * 20)
        print("==" * 8 + "트리정보" + "==" * 8)
        print("==" * 20)
        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            print(f"{pre}{node.name}, data: {node.data}")
        print("==" * 20)

    def showTreeP2Cformat(self):
        with open(self.targetPath, "w", encoding="UTF-8") as f:
           for row in RenderTree(self.node_set[0]):
               pre, fill, node = row
               if node.data == "상품":
                   continue
               f.write(f"{node.parent.data} {node.data}\n")

if __name__ == "__main__":
    ngtc = NaverGoodsTreeConverter()
    ngtc.makeContent()
    ngtc.makeTree()
    ngtc.showTree()
