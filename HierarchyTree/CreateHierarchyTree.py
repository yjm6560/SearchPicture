from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from HierarchyTree.FilePath import filePathGetter

class HierarchyTree:
    def __init__(self):
        self.file_name = filePathGetter.getFilePath()
        self.node_set = []
        self.content = []

    def makeContent(self):
        f = open(self.file_name, 'r', encoding='UTF8')
        while True:
            line = f.readline()
            if not line : break
            self.content.append((line.count("\t") ,line.replace("\n","").replace("\t","", len(line))))
        f.close()

    def makeTree(self):
        self.makeContent()
        print("Not implemented")

    def searchKeyword(self, keyword):
        print("Not implemented")

    def getRelatedNodes(self, node):
        print("Not implemented")

    def getChildren(self, node):
        print("Not implemented")

    def getParents(self, node):
        print("Not implemented")

    def showTree(self):
        print("==" * 20)
        for row in RenderTree(self.node_set[0]):
            pre, fill, node = row
            print(f"{pre}{node.name}, data: {node.data}")
        print("==" * 20)

if __name__ == "__main__":
    ht = HierarchyTree()
    ht.makeTree()
    print(ht.content)
