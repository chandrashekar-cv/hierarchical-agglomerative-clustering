__author__ = 'Chandu'
import sys,heapq,math,itertools

class hcluster:
    dataPoints = {}
    clusters = {}
    clusterCenters={}
    goldStandardClusters = {}
    heap = []
    k=0
    mergedClusters = []

    def __init__(self,k,fileName):
        self.k = k
        self.readFile(fileName)

    def readFile(self,fileName):
        lines = None
        with open(fileName,"r") as reader:
            lines = reader.readlines()
        clusterCount = 0
        for i in range(0,len(lines)):

            line = lines[i].strip().split(",")
            className = line[len(line)-1]
            point = tuple(map(float,line[:len(line)-1]))
            self.dataPoints[i] = point

            self.clusterCenters.setdefault(clusterCount)
            self.clusterCenters[clusterCount] = point

            self.clusters.setdefault(clusterCount,[])
            self.clusters[clusterCount].append(i)
            clusterCount += 1

            self.goldStandardClusters.setdefault(className,[])
            self.goldStandardClusters[className].append(i)


    def computeDistances(self):

        keys = self.clusterCenters.keys()
        combination = list(itertools.combinations(keys,2))
        for key in combination:
            p1 = self.clusterCenters[key[0]]
            p2 = self.clusterCenters[key[1]]

            dist = self.euclideanDist(p1,p2)
            heapq.heappush(self.heap,tuple([dist,key[0],key[1]]))

    def insertNewDistances(self,center,index):

        for k,v in self.clusterCenters.items():
            dist = self.euclideanDist(center,v)
            heapq.heappush(self.heap, tuple([dist,k,index]))

    def euclideanDist(self,p1,p2):
        p1 = list(p1)
        p2 = list(p2)
        dist = 0.0
        for i in range(0,len(p1)):
            dist+=((p1[i]-p2[i])**2)

        return math.sqrt(dist)


    def clustering(self):
        self.computeDistances()

        while(len(self.clusters.keys())>self.k):
            heapq.heapify(self.heap)
            while True:
                mergingClusters = heapq.heappop(self.heap)
                c1 = mergingClusters[1]
                c2 = mergingClusters[2]
                if(self.mergedClusters.__contains__(c1) or self.mergedClusters.__contains__(c2)):
                    continue
                else:
                    break

            self.mergeClusters(c1,c2)



    def mergeClusters(self,c1,c2):
        cluster1 = list(self.clusters[c1])
        cluster2 = list(self.clusters[c2])

        newCluster = cluster1+cluster2
        center = self.calculateClusterCenter(newCluster)

        index = max(self.clusters.keys())+1

        self.mergedClusters.extend([c1,c2])
        del self.clusters[c1]
        del self.clusters[c2]
        del self.clusterCenters[c1]
        del self.clusterCenters[c2]

        self.insertNewDistances(center,index)

        self.clusterCenters[index] = center
        self.clusters[index]=newCluster

    def calculateClusterCenter(self,newCluster):

        center = [0.0]*len(self.dataPoints[0])
        for index in newCluster:
            point = self.dataPoints[index]
            for i in range(0,len(point)):
                center[i]+=point[i]

        for i in range(0,len(center)):
            center[i] = center[i]/len(newCluster)

        return center

    def calculatePrecissionRecall(self):
        goldSet=[]
        for k,v in self.goldStandardClusters.items():
            goldSet.extend(list(itertools.combinations(sorted(v),2)))

        goldSet = set(goldSet)

        algoSet =[]
        for k,v in self.clusters.items():
            algoSet.extend(list(itertools.combinations(sorted(v),2)))

        algoSet = set(algoSet)

        numerator = len(goldSet.intersection(algoSet))

        precision = float(numerator) / len(algoSet)
        recall = float(numerator) / len(goldSet)
        print(str(precision))
        print(str(recall))
		
    def outputClusters(self):
        for k,v in self.clusters.items():
            print(sorted(v))

        
if __name__=="__main__":
    fileName = sys.argv[2]
    k = int(sys.argv[1])
    clustering = hcluster(k,fileName)
    clustering.clustering()
    clustering.calculatePrecissionRecall()
    clustering.outputClusters()
