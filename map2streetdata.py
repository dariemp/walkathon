#!/usr/bin/env python
import math
from xml.dom.minidom import parse
from geopy.distance import distance as geo_distance

LOCAL_COORD_ORIGIN_LATITUD = 50.8
LOCAL_COORD_ORIGIN_LONGITUD = -114.3


def earth_coord_2_local_coord(lat, lon):
    x = geo_distance((lat, lon), (lat, LOCAL_COORD_ORIGIN_LONGITUD))
    y = geo_distance((lat, lon), (LOCAL_COORD_ORIGIN_LATITUD, lon))
    return x, y


def local_coord_2_earth_coord(x, y):
    # FIXME : wasn't working
    return lat, lon


def cartesian_distance(pointA, pointB):
    x1 = pointA[0]
    y1 = pointA[1]
    x2 = pointB[0]
    y2 = pointB[1]
    return math.sqrt( (x2-x1)**2 + (y2-y1)**2 )


def get_intersection(way1_nodes, way2_nodes, node_data):
    for i in range(len(way1_nodes)-1):
        for j in range(len(way2_nodes)-1):
            if way1_nodes[i] == way2_nodes[j]:
                return node_data[way1_nodes[i]]
            else:
                node1_coord= node_data[way1_nodes[i]]
                next_node1_coord = node_data[way1_nodes[i+1]]
                node2_coord= node_data[way2_nodes[j]]
                next_node2_coord = node_data[way2_nodes[j+1]]
                result = calculate_intersection(node1_coord, next_node1_coord, node2_coord, next_node2_coord)
                if result:
                    return result
    return None


def calculate_intersection(line1_point1, line1_point2, line2_point1, line2_point2):
    x1 = line1_point1[1]
    y1 = line1_point1[0]
    x2 = line1_point2[1]
    y2 = line1_point2[0]
    x3 = line2_point1[1]
    y3 = line2_point1[0]
    x4 = line2_point2[1]
    y4 = line2_point2[0]
    denominator = (x4-x3)*(y2-y1) - (x2-x1)*(y4-y3)
    if denominator == 0:
        return None
    s = ((x4-x3)*(y3-y1)-(x3-x1)*(y4-y3)) / denominator
    t = ((x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)) / denominator
    if s >= 0 and t <= 1:
        x = x1 + s*(x2-x1)
        y = y1 + s*(y2-y1)
        assert math.isclose(x, x3 + t*(x4-x3)), 'Wrong intersection calculation'
        assert math.isclose(y, y3 + t*(y4-y3)), 'Wrong intersection calculation'
        return x, y
    return None

def get_all_intersections(ways_data, nodes_data):
    intersections = list()
    ways_data_items = ways_data.items()
    for way1_id, way1_nodes in ways_data_items:
        for way2_id, way2_nodes in ways_data_items:
            if way1_id == way2_id:
                continue
            intersection = get_intersection(way1_nodes, way2_nodes, nodes_data)
            if intersection:
                intersections.append(intersection)
    return intersections


def main():
    dom = parse('map.osm')
    nodes = dom.getElementsByTagName('node')
    nodes_data = {int(node.getAttribute('id')) : (float(node.getAttribute('lat')), float(node.getAttribute('lon'))) for node in nodes}
    ways = dom.getElementsByTagName('way')
    ways_data = {int(way.getAttribute('id')): [int(child_node.getAttribute('ref')) for child_node in way.getElementsByTagName('nd')] for way in ways}
    intersections = get_all_intersections(ways_data, nodes_data)
    print((intersections[1], intersections[0]))


if __name__ == '__main__':
    main()
