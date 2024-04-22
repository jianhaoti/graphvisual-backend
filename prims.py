import heapq

def connectedComponent(graphAdjacencyList, source): # run dfs to find connected component
    visited = set()
    stacked = [source]
    while stacked:
        processing = stacked.pop()
        visited.add(processing)
        for neighbor in graphAdjacencyList[processing]:
            if neighbor not in visited:
                stacked.append(neighbor)
    return visited

def prims(graphAdjacencyList, edgeWeights, source):
    component = connectedComponent(graphAdjacencyList, source)
    nodeStatus = {node: "unvisited" for node in component} # always populated
    nodeStatus[source] = "processing"
    edgeStatus = {}
    steps = [] 

    nextStep = [(0, source, None)] 

    while nextStep:
        cost, processing, prevNode = heapq.heappop(nextStep)
        
        if nodeStatus[processing] == "visited":
            continue

        edgeStatus[f"{processing}-{prevNode}"] = "visited"
        edgeStatus[f"{prevNode}-{processing}"] = "visited"

        
        for neighbor in graphAdjacencyList[processing]:
            if nodeStatus[neighbor] != "visited":
                heapq.heappush(nextStep, (edgeWeights[(processing, neighbor)], neighbor, processing))
                nodeStatus[neighbor] = "queued"
                
                edgeStatus[f"{processing}-{neighbor}"] = "queued"
                edgeStatus[f"{neighbor}-{processing}"] = "queued"

                
        
        nodeStatus[processing] = "visited"
        prevNode = processing
        
        
    return steps