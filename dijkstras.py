import heapq
import json
import sys

# input_str = sys.stdin.read()
# print(f"Received raw input: {input_str}", file=sys.stderr)

#! BEWARE
#! the edge a -> b is now a tuple ('a','b')  
#! in graphAdjacencyList and in edgeWeights

def dijkstras(graphAdjacencyList, edgeWeights, source, isOriented):
    
    prioQueue = [(0, source)]
    processing = None

    edgeStatus = {}
    nodeStatus = {node: "unvisited" for node in graphAdjacencyList} # always populated
    nodeStatus[source] = "queued"

    currentShortest = {node: float('inf') for node in graphAdjacencyList}
    currentShortest[source] = 0

    steps = []  

    while prioQueue:
        # pop out next shortest guy from source
        currentDistance, processing = heapq.heappop(prioQueue)
        nodeStatus[processing] = "processing"

        for node in nodeStatus:
            changeEdge = f"{node}-{processing}"
            if (nodeStatus[node]=="visited" and edgeStatus.get(changeEdge)== "queued"):
                edgeStatus[changeEdge] = "visited"
                if not isOriented:
                    edgeStatus[f"{processing}-{node}"] = "visited"
            
        #* node: orange -> white
        #* edges: orange -> black
        steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "currentShortest": dict(currentShortest)})

        # this assumes currentDistance is the shortest distance
        # update neighbor's shortest 
        for neighbor in graphAdjacencyList[processing]:
            currentEdge = f"{processing}-{neighbor}" 
            reverseEdge = f"{neighbor}-{processing}"

            if nodeStatus[neighbor] == "unvisited":
                edgeStatus[currentEdge] = "processing"
                
                if (processing, neighbor) in edgeWeights:
                    competition = currentDistance + edgeWeights[(processing, neighbor)]

                    if competition < currentShortest[neighbor]:
                        currentShortest[neighbor] = competition
                        heapq.heappush(prioQueue, (competition, neighbor))
                        nodeStatus[neighbor] = "queued"      
                        edgeStatus[currentEdge] = "queued"

                    if not isOriented:
                        edgeStatus[reverseEdge] = "queued"
                    
            else:
                edgeStatus[currentEdge] = "useless"
                if not isOriented:
                    edgeStatus[reverseEdge] = "useless"

        #* nodes: yellow -> orange
        #* edges: yellow -> orange or opaque
        steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "currentShortest": dict(currentShortest)})

        # add processing to visited and reset
        nodeStatus[processing] = "visited"
        
        #* node: white -> black
        steps.append({"nodeStatus": dict(nodeStatus), "edgeStatus": dict(edgeStatus), "currentShortest": dict(currentShortest)})
    return steps


if __name__ == "__main__":
    # Read input data from stdin
    input_str = sys.stdin.read()
    try:
        data = json.loads(input_str)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error decoding JSON: {e}\n")
        sys.exit(1)

    # Extract required data from the parsed JSON
    try:
        graphAdjacencyList = data["graphAdjacencyList"]
        edgeWeights = {tuple(k.split('-')): v for k, v in data["edgeWeights"]}
        source = data["source"]
        isOriented = data["isOriented"]
        
        # sys.stderr.write("graphAdjacencyList:\n" + json.dumps(graphAdjacencyList, indent=2) + "\n")
        # sys.stderr.write("edgeWeights:\n" + json.dumps(edgeWeights, indent=2) + "\n")
        # sys.stderr.write("source: " + json.dumps(source) + "\n")
        # sys.stderr.write("isOriented: " + json.dumps(isOriented) + "\n")

    except KeyError as e:
        print(f"Missing key in input JSON data: {e}")
        sys.exit(1)
    
    # Call the dijkstras function with input data
    steps = dijkstras(graphAdjacencyList, edgeWeights, source, isOriented)

    # Print the steps in JSON format
    final_output = {"steps": steps}

    for step in steps:
        # Convert 'inf' to "Infinity" within each step as needed
        for node, distance in step["currentShortest"].items():
            if distance == float('inf'):
                step["currentShortest"][node] = "Infinity"
    print(json.dumps(final_output, indent=1))  # Print the modified steps list as a single JSON object
