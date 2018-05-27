# Walkathon
Walkathon is the code name for an app that allows you to find nice routes to walk through the city of Calgary.

We use a map from OpenStreetMap.org to gather data of possible routes by creating a graph connecting streets and pathways. This way we can traverse the graph by using a modification of a well-know algorithm that takes into account the "niceness" index of the route.

# Tools
**map2streetdata.py**: converts a map from OpenStreetMap.org into a nicer format that we can query from Firebase
