

def loadDataSet():
    dataSet = [['bread','milk'],
            ['bread','diaper','beer','eggs'],
            ['milk','diaper','beer','coke'],
            ['bread','milk','diaper','beer'],
            ['bread','milk','diaper','coke']]
    return dataSet

def transfer2FrozenDataSet(dataSet):
    frozenDataSet = {}
    for elem in dataSet:
        frozenDataSet[frozenset(elem)] = 1
    return frozenDataSet

class TreeNode:
    def __init__(self, nodeName, count, nodeParent):
        self.nodeName = nodeName
        self.count = count
        self.nodeParent = nodeParent
        self.nextSimilarItem = None
        self.children = {}

    def increaseC(self, count):
        self.count += count

def createFPTree(frozenDataSet, minSupport):
    headPointTable = {}
    for items in frozenDataSet:
        for item in items:
            headPointTable[item] = headPointTable.get(item, 0) + frozenDataSet[items]
    headPointTable = {k:v for k,v in headPointTable.items() if v >= minSupport}
    frequentItems = set(headPointTable.keys())
    if len(frequentItems) == 0: return None, None

    for k in headPointTable:
        headPointTable[k] = [headPointTable[k], None]
    fptree = TreeNode("null", 1, None)
    for items,count in frozenDataSet.items():
        frequentItemsInRecord = {}
        for item in items:
            if item in frequentItems:
                frequentItemsInRecord[item] = headPointTable[item][0]
        if len(frequentItemsInRecord) > 0:
            orderedFrequentItems = [v[0] for v in sorted(frequentItemsInRecord.items(), key=lambda v:v[1], reverse = True)]
            updateFPTree(fptree, orderedFrequentItems, headPointTable, count)

    return fptree, headPointTable

def updateFPTree(fptree, orderedFrequentItems, headPointTable, count):
    if orderedFrequentItems[0] in fptree.children:
        fptree.children[orderedFrequentItems[0]].increaseC(count)
    else:
        fptree.children[orderedFrequentItems[0]] = TreeNode(orderedFrequentItems[0], count, fptree)

        if headPointTable[orderedFrequentItems[0]][1] == None:
            headPointTable[orderedFrequentItems[0]][1] = fptree.children[orderedFrequentItems[0]]
        else:
            updateHeadPointTable(headPointTable[orderedFrequentItems[0]][1], fptree.children[orderedFrequentItems[0]])
    if len(orderedFrequentItems) > 1:
        updateFPTree(fptree.children[orderedFrequentItems[0]], orderedFrequentItems[1::], headPointTable, count)

def updateHeadPointTable(headPointBeginNode, targetNode):
    while headPointBeginNode.nextSimilarItem is not None:
        headPointBeginNode = headPointBeginNode.nextSimilarItem
    headPointBeginNode.nextSimilarItem = targetNode

def mineFPTree(headPointTable, prefix, frequentPatterns, minSupport):
    headPointItems = [v[0] for v in sorted(headPointTable.items(), key = lambda v:v[1][0])]
    if len(headPointItems) == 0: return

    for headPointItem in headPointItems:
        newPrefix = prefix.copy()
        newPrefix.add(headPointItem)
        support = headPointTable[headPointItem][0]
        frequentPatterns[frozenset(newPrefix)] = support

        prefixPath = getPrefixPath(headPointTable, headPointItem)
        if prefixPath != {}:
            conditionalFPtree, conditionalHeadPointTable = createFPTree(prefixPath, minSupport)
            if conditionalHeadPointTable is not None:
                mineFPTree(conditionalHeadPointTable, newPrefix, frequentPatterns, minSupport)

def getPrefixPath(headPointTable, headPointItem):
    prefixPath = {}
    beginNode = headPointTable[headPointItem][1]
    prefixs = ascendTree(beginNode)
    if prefixs:
        prefixPath[frozenset(prefixs)] = beginNode.count

    while beginNode.nextSimilarItem is not None:
        beginNode = beginNode.nextSimilarItem
        prefixs = ascendTree(beginNode)
        if prefixs:
            prefixPath[frozenset(prefixs)] = beginNode.count
    return prefixPath

def ascendTree(treeNode):
    prefixs = []
    while (treeNode.nodeParent is not None) and (treeNode.nodeParent.nodeName != 'null'):
        treeNode = treeNode.nodeParent
        prefixs.append(treeNode.nodeName)
    return prefixs

def rulesGenerator(frequentPatterns, minConf, rules):
    for frequentset in frequentPatterns:
        if len(frequentset) > 1:
            getRules(frequentset,frequentset, rules, frequentPatterns, minConf)

def removeStr(set, str):
    tempSet = []
    for elem in set:
        if elem != str:
            tempSet.append(elem)
    tempFrozenSet = frozenset(tempSet)
    return tempFrozenSet


def getRules(frequentset,currentset, rules, frequentPatterns, minConf):
    for frequentElem in currentset:
        subSet = removeStr(currentset, frequentElem)
        confidence = frequentPatterns[frequentset] / frequentPatterns[subSet]
        if confidence >= minConf:
            flag = False
            for rule in rules:
                if rule[0] == subSet and rule[1] == frequentset - subSet:
                    flag = True
            if not flag:
                rules.append((subSet, frequentset - subSet, confidence))

            if len(subSet) >= 2:
                getRules(frequentset, subSet, rules, frequentPatterns, minConf)

if __name__=='__main__':
    print("fptree:")
    dataSet = loadDataSet()
    frozenDataSet = transfer2FrozenDataSet(dataSet)
    minSupport = 2
    fptree, headPointTable = createFPTree(frozenDataSet, minSupport)
    # fptree.disp()
    frequentPatterns = {}
    prefix = set([])
    mineFPTree(headPointTable, prefix, frequentPatterns, minSupport)
    print("frequent patterns:")
    print(frequentPatterns)
    minConf = 0.6
    rules = []
    rulesGenerator(frequentPatterns, minConf, rules)
    print("association rules:")
    print(rules)