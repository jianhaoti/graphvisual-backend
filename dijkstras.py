import heapq

def dijkstras(theNeighbors, edgeWeights, source, isOriented):
    prioQueue = [(0, source)]
    processing = None

    edgeStatus = {}
    nodeStatus = {node: "unvisited" for node in theNeighbors}
    nodeStatus[source] = "queued"

    currentShortest = {node: float('infinity') for node in theNeighbors}
    currentShortest[source] = 0

    while prioQueue:
        # pop out next shortest guy from source
        currentDistance, processing = heapq.heappop(prioQueue)
        nodeStatus[processing] = "processing"

        #! CAPTURE SNATPSHOT #

        # this assumes currentDistance is the shortest distance
        # update neighbor's shortest 
        for neighbor in theNeighbors[processing]:
            currentEdge = f"{processing}-{neighbor}" if isOriented else f"{min(processing, neighbor)}-{max(processing, neighbor)}"
            if nodeStatus[neighbor] in ["visited", "queued"]:
                edgeStatus[currentEdge] = "useless"
            else:
                competition = currentDistance + edgeWeights[currentEdge]
                edgeStatus[currentEdge] = "processing"
                if competition < currentShortest[neighbor]:
                    currentShortest[neighbor] = competition
                    heapq.heappush(prioQueue, (competition, neighbor))
                    nodeStatus[neighbor] = "queued"

        
        #! CAPTURE SNATPSHOT #

        # add processing to visited and reset
        nodeStatus[processing] = "visited"
        processing = ""
        
        #! CAPTURE SNATPSHOT #

    return currentShortest, edgeStatus, nodeStatus




