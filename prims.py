import heapq
import sys, json


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
    runningCost = 0

    steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "runningCost": int(runningCost)})

    while nextStep:
        cost, processing, prevNode = heapq.heappop(nextStep)
        
        if nodeStatus[processing] == "visited":
            continue

        nodeStatus[processing] = "processing"

        if prevNode is not None:  # If it's not the first node
            edgeStatus[f"{processing}-{prevNode}"] = "visited"
            runningCost += cost
            steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "runningCost": int(runningCost)})

        
        for neighbor in graphAdjacencyList[processing]:
            if nodeStatus[neighbor] != "visited":
                heapq.heappush(nextStep, (edgeWeights[(processing, neighbor)], neighbor, processing))
                nodeStatus[neighbor] = "queued"
                
                edgeStatus[f"{processing}-{neighbor}"] = "queued"

        steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "runningCost": int(runningCost)})
     
        nodeStatus[processing] = "visited"
        steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "runningCost": int(runningCost)})

        prevNode = processing
        
        
    return steps

def main():
    # Reading JSON input from standard input
    input_json = sys.stdin.read()
    data = json.loads(input_json)
    
    # Extracting data for the algorithm
    graph = data['graphAdjacencyList']
    edgeWeights = {tuple(k.split('-')): v for k, v in data['edgeWeights']}
    source = data['source']
    
    # Running Prim's algorithm
    steps = prims(graph, edgeWeights, source)
    
    # Output the result as a JSON
    print(json.dumps(steps, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
