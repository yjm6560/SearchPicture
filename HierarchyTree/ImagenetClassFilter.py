import sqlite3
import re
from anytree import Node, RenderTree

class ImagenetClassFilter:
    def __init__(self, training_label, wnid2name):
        self.trainingLabelFilePath = training_label
        self.wnid2nameFilePath = wnid2name
        self.trainingLabel = []
        self.wnid2name = {}

    def makeTrainingLabelSet(self):
        self.trainingLabel = []
        with open(self.trainingLabelFilePath, "r") as training_f:
            while True:
                line = training_f.readline()
                if not line:
                    break
                pattern = None
                if line[-3] == "\"":
                    pattern = re.compile(r"\".*\"")
                else:
                    pattern = re.compile(r"\'.*\'")
                m = pattern.search(line.replace("\n",""))

                self.trainingLabel.append(str(m.group()).replace(", ", "/", len(str(m.group)))[1:-1])
    def writeTrainingLabels2File(self):
        with open("training_label.dat","w") as f:
            for wnid, name in self.wnid2name.items():
                if self.changeFormat(name) in self.trainingLabel:
                    f.write(wnid)
                    f.write(" ")
                    f.write(self.changeFormat(name))
                    f.write("\n")

    def makeWnid2NameMap(self):
        with open(self.wnid2nameFilePath, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                self.wnid2name[line[:self.getLenWnid()]] = self.changeFormat(line[self.getLenWnid()+1:])

    def changeFormat(self, name):
        return name.replace(", ", "/", len(name)).replace("\n","")

    def check_wnid_in_wnid2key(self, wnid):
        if wnid[0] != "n" or wnid in self.wnid2name.keys():
            return True
        else:
            return False

    def is_name_in_trainingLabel(self, name):
        if name[0] != "n" or name[self.getLenWnid()+1 : ] in self.trainingLabel:
            return True
        else:
            return False
    def is_wnid_in_trainingLabel(self, wnid):
        if wnid[0] != "n" or wnid[:self.getLenWnid()] in self.trainingLabel:
            return True
        else:
            return False

    def getData(self, wnid):
        if wnid in self.wnid2name.keys():
            return self.wnid2name[wnid]
        else:
            return None
    def getLenWnid(self):
        return len("n00000000")

if __name__ == "__main__":
    icFilter = ImagenetClassFilter("Imagenet.txt", "wnid2name.txt")
    icFilter.makeTrainingLabelSet()
    icFilter.makeWnid2NameMap()
    for val in icFilter.trainingLabel:
        print(val)
#    for key, val in icFilter.wnid2name.items():
#        print(key," ", val)
    print(icFilter.is_name_in_trainingLabel("junco/snowbird"))
    print(icFilter.getData("n02404186"))
    icFilter.writeTrainingLabels2File()
