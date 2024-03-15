import heapq
import json
import sys

# an edge a -> b is now a tuple ('a','b') in python
def dijkstras(theNeighbors, edgeWeights, source, isOriented):
    prioQueue = [(0, source)]
    processing = None

    edgeStatus = {}
    nodeStatus = {node: "unvisited" for node in theNeighbors} # always populated
    nodeStatus[source] = "queued"

    currentShortest = {node: float('inf') for node in theNeighbors}
    currentShortest[source] = 0

    steps = []  

    while prioQueue:
        # pop out next shortest guy from source
        currentDistance, processing = heapq.heappop(prioQueue)
        nodeStatus[processing] = "processing"

        for node in nodeStatus:
            changeEdge = f"{node}-{processing}"
            if (nodeStatus[node]=="visited" and edgeStatus.get((node,processing))== "queued"):
                edgeStatus[changeEdge] = "visited"
                if not isOriented:
                    edgeStatus[f"{processing}-{node}"] = "visited"
            
        #* node: orange -> white
        #* edges: orange -> black
        steps.append({'nodeStatus': dict(nodeStatus), 'edgeStatus': dict(edgeStatus), 'currentShortest': dict(currentShortest)})

        # this assumes currentDistance is the shortest distance
        # update neighbor's shortest 
        for neighbor in theNeighbors[processing]:
            currentEdge = f"{processing}-{neighbor}" 
            reverseEdge = f"{neighbor}-{processing}"

            if nodeStatus[neighbor] == "unvisited":
                edgeStatus[currentEdge] = "processing"
                print(currentEdge, edgeWeights)
                
                if (processing, neighbor) in edgeWeights:
                    competition = currentDistance + edgeWeights[(processing, neighbor)]
                    print(f"Competition for {processing} -> {neighbor}: {competition}")  # Check if this path is shorter

                    if competition < currentShortest[neighbor]:
                        currentShortest[neighbor] = competition
                        heapq.heappush(prioQueue, (competition, neighbor))
                        print(prioQueue)
                        nodeStatus[neighbor] = "queued"      
                        edgeStatus[currentEdge] = "processing"

                    if not isOriented:
                        edgeStatus[reverseEdge] = "processing"
                    
            else:
                edgeStatus[currentEdge] = "useless"
                if not isOriented:
                    edgeStatus[reverseEdge] = "useless"

        #* nodes: yellow -> orange
        #* edges: yellow -> orange or opaque
        steps.append({'nodeStatus': dict(nodeStatus), 'edgeStatus': dict(edgeStatus), 'currentShortest': dict(currentShortest)})

        # add processing to visited and reset
        nodeStatus[processing] = "visited"
        
        #* node: white -> black
        steps.append({'nodeStatus': dict(nodeStatus), 'edgeStatus': dict(edgeStatus), 'currentShortest': dict(currentShortest)})
    
    return steps

if __name__ == "__main__":
    # Read input data from stdin
    input_str = sys.stdin.read()

    # Parse the JSON input data
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        sys.exit(1)

    # Extract required data from the parsed JSON
    try:
        theNeighbors = data["graphAdjacencyList"]
        edgeWeights = {tuple(k.split('-')): v for k, v in data["edgeWeights"]}
        source = data["source"]
        isOriented = data["isOriented"]
    except KeyError as e:
        print(f"Missing key in input JSON data: {e}")
        sys.exit(1)

    # Convert edgeWeights to the format your dijkstras function expects
    # Assuming edgeWeights should be a dictionary {('node1', 'node2'): weight, ...}
    
    # Call the dijkstras function with input data
    steps = dijkstras(theNeighbors, edgeWeights, source, isOriented)

    # Print the steps in JSON format
    for step in steps:
        print(json.dumps(step, indent=2))
        print("\n")  # Adds an extra newline for clearer separation between steps



