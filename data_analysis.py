import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import csv 
from scipy.spatial.distance import euclidean
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, Point
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

path = "results/"

def clustering(bacteria):
    # Extract spatial positions (x, y) and convert to micrometers
    positions = np.array([[float(bacterium[1]) / 10, float(bacterium[2]) / 10] for bacterium in bacteria])

    # Compute offsets to shift positions into positive coordinates
    offset_x = -np.min(positions[:, 0]) 
    offset_y = np.min(positions[:, 1]) 
    print(offset_y, "OFFSET Y")

    # Shift all bacteria positions
    shifted_positions = positions + np.array([offset_x, offset_y])

    # Perform DBSCAN clustering (eps in micrometers)
    db = DBSCAN(eps=5, min_samples=2).fit(shifted_positions)

    # Cluster labels (-1 indicates noise)
    labels = db.labels_

    # Number of clusters found (exclude noise label)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f'Number of clusters: {n_clusters}')

    # Organize bacteria into clusters using shifted micrometer coordinates
    clusters = {}
    for label, bacterium in zip(labels, bacteria):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append([float(bacterium[1]) / 10 + offset_x, float(bacterium[2]) / 10 + offset_y])

    # Compute centroid for each cluster
    centroids = {}
    for cluster_id, cluster_bacteria in clusters.items():
        cluster_positions = np.array(cluster_bacteria)
        centroid = cluster_positions.mean(axis=0)
        centroids[cluster_id] = centroid

    # Invert the Y-values for plotting (if required by coordinate system)
    shifted_positions[:, 1] = -shifted_positions[:, 1]
    for cluster_id, centroid in centroids.items():
        centroid[1] = -centroid[1]

    return centroids, shifted_positions, labels


def graph_distance_between_centroids(centroids, positions, labels, pairs, color_expression):
    # Plot bacteria points colored by cluster label
    plt.scatter(positions[:, 0], positions[:, 1], c=labels, cmap='viridis', label='Bacteria')
    print(centroids, "centroids")

    # Plot each centroid and label it
    for cluster_id, centroid in centroids.items():
        plt.scatter(centroid[0], centroid[1], s=200, c='red', marker='X', label=f'Centroid {cluster_id}')
        plt.text(centroid[0], centroid[1], f'Centroid {cluster_id}', fontsize=12, color='red')

    # Draw lines between specified pairs of centroids and annotate distances
    for cluster_id_1, cluster_id_2 in pairs:
        centroid_1 = centroids.get(cluster_id_1)
        centroid_2 = centroids.get(cluster_id_2)
        if centroid_1 is not None and centroid_2 is not None:
            plt.plot([centroid_1[0], centroid_2[0]], [centroid_1[1], centroid_2[1]], 'k--', lw=2)
            distance = euclidean(centroid_1, centroid_2)
            plt.text((centroid_1[0] + centroid_2[0]) / 2, (centroid_1[1] + centroid_2[1]) / 2, 
                    f'{distance:.2f} µm', fontsize=12, color='blue', ha='center')

    plt.xlabel('X (µm)')
    plt.ylabel('Y (µm)')
    plt.title(f'DBSCAN Clustering of {color_expression}-Positive Bacteria with Centroids and Lines (µm)')
    plt.legend()
    plt.savefig(f"{path}/{color_expression}_in_micrometers.png", transparent=True)
    plt.show()


def voronoi(arrs, bacteria_points, filename, colors, labels): 
    # Combine centroid arrays from different channels into a single points array
    allpoints = []
    for arr in arrs:
        allpoints.extend(arr)
    points = np.array(allpoints)
    vor = Voronoi(points)

    fig = voronoi_plot_2d(vor, point_size=6)

    # Add a legend entry for Voronoi points
    plt.scatter([], [], c='blue', marker='o', label='Voronoi points')

    # Label axes with units
    plt.xlabel('X (µm)')
    plt.ylabel('Y (µm)')
    plt.title('Voronoi Diagram of Bacteria Clusters (µm)')

    # Plot bacteria positions for each channel
    for bacteria, color, label in zip(bacteria_points, colors, labels):
        sub_bacteria_points = np.array(bacteria)
        plt.scatter(sub_bacteria_points[:, 0], sub_bacteria_points[:, 1], c=color, marker='o', label=label)
        plt.legend()

    plt.savefig(filename, transparent=True)
    plt.show()


def construct_voronoi_polygons(vor):
    # Build shapely Polygon objects for finite Voronoi regions
    polygons = []
    for region_idx in vor.point_region:
        vertices = vor.regions[region_idx]
        if -1 in vertices or len(vertices) == 0:
            polygons.append(None)
            continue
        polygon = Polygon([vor.vertices[i] for i in vertices])
        polygons.append(polygon)
    return polygons


def validate_bacteria_in_voronoi(bacteria_positions, cluster_labels, polygons):
    # Validate whether bacteria points lie inside their assigned Voronoi polygon
    correct = 0
    total = len(bacteria_positions)
    for position, label in zip(bacteria_positions, cluster_labels):
        if label == -1:
            continue
        point = Point(position)
        polygon = polygons[label]
        if polygon is not None and polygon.contains(point):
            correct += 1
    return correct / total


def obtain_score(centroids, bacteria_positions):
    # Calculate Voronoi regions from centroids and evaluate point inclusion
    vor = Voronoi(centroids)

    # Construct polygons for finite Voronoi regions
    polygons = []
    for region_idx in vor.point_region:
        region = vor.regions[region_idx]
        if not -1 in region and region:  # Ignore regions with a point at infinity
            polygon = Polygon([vor.vertices[i] for i in region])
            polygons.append(polygon)

    inside_count = 0
    inside_points = []
    outside_points = []

    # Check which bacteria lie inside any Voronoi polygon
    for x, y in bacteria_positions:
        point = Point(x, y)
        if any(polygon.contains(point) for polygon in polygons):
            print(point, "point is inside")
            inside_count += 1
            inside_points.append((x, y))
        else:
            outside_points.append((x, y))

    percentage = (inside_count / len(bacteria_positions)) * 100
    print(f"{percentage:.2f}% points are inside the polygons")

    # --- Plotting Section ---
    fig, ax = plt.subplots()

    # Plot polygons as patches
    patches = []
    for poly in polygons:
        if poly is not None and not poly.is_empty:
            patches.append(MplPolygon(list(poly.exterior.coords), closed=True))
    p = PatchCollection(patches, facecolor='lightblue', edgecolor='black', alpha=0.5)
    ax.add_collection(p)

    # Plot points classified as inside or outside
    if inside_points:
        inside_points = list(zip(*inside_points))
        ax.scatter(inside_points[0], inside_points[1], color='green', label='Inside Points')

    if outside_points:
        outside_points = list(zip(*outside_points))
        ax.scatter(outside_points[0], outside_points[1], color='red', label='Outside Points')

    ax.set_aspect('equal')
    ax.legend()
    plt.show()

# Global variables
# Arrays that represent relations between centroids; used to calculate distances between centroids
pairs_g = [
    (4, 2), (4, 3), (3, 2), (3, 6), (3, 5), (2, 1),
    (2, 5), (5, 6), (1, 5), (5, 0), (5, 1), (1, 0)  
]

pairs_r = [
    (3, 2), (3, 4), (3, 0), 
    (2, 0), 
    (0, 4), (0, 1),
    (1, 4)
]

pairs_y = [
    (4, 3), (4, 5), (4, 0), (3, 5), (3, 2), (5, 0),
    (5, 2), (2, 0), (0, 1)  
]


def main():
    bacterias_time = []
    # Expected CSV columns: id, x, y, theta, volume, gfp, rfp, yfp, cfp
    with open('dataset/records_voronoi.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        first_row = next(spamreader)  # Read header row
        bacteria_actual_group = []
        for row in spamreader:
            if(row[0] == "id"):
                bacterias_time.append(bacteria_actual_group)
                bacteria_actual_group = []
            else:
                bacteria_actual_group.append(row)
        print("Number of time periods", len(bacterias_time))

    # Select bacteria at a specific time index (e.g., 1500)
    bacteria_gfp = [bacterium for bacterium in bacterias_time[35] if int(bacterium[5]) > 0]
    bacteria_rfp = [bacterium for bacterium in bacterias_time[35] if int(bacterium[6]) > 0]
    bacteria_yfp = [bacterium for bacterium in bacterias_time[35] if int(bacterium[7]) > 0]

    # Perform clustering
    centroids_gfp, positions_gfp, labels_gfp = clustering(bacteria_gfp)
    centroids_rfp, positions_rfp, labels_rfp = clustering(bacteria_rfp)
    centroids_yfp, positions_yfp, labels_yfp = clustering(bacteria_yfp)

    # Plot distances between centroids
    graph_distance_between_centroids(centroids_gfp, positions_gfp, labels_gfp, pairs_g, "GFP")
    graph_distance_between_centroids(centroids_rfp, positions_rfp, labels_rfp, pairs_r, "RFP")
    graph_distance_between_centroids(centroids_yfp, positions_yfp, labels_yfp, pairs_y, "YFP")

    # Convert centroid dictionaries to arrays
    centroids_array_gfp = np.array(list(centroids_gfp.values()))
    centroids_array_rfp = np.array(list(centroids_rfp.values()))
    centroids_array_yfp = np.array(list(centroids_yfp.values()))

    # Obtain point-in-polygon scores for each channel (optional)
    # obtain_score(centroids_array_gfp, positions_gfp)
    # obtain_score(centroids_array_rfp, positions_rfp)
    # obtain_score(centroids_array_yfp, positions_yfp)

    # Plot combined Voronoi diagram for all channels
    voronoi(
         [centroids_array_gfp, centroids_array_rfp, centroids_array_yfp], 
         [positions_gfp, positions_rfp, positions_yfp], 
         path+f"voronoi_all.png", 
         ["green", "red", "darkorange"],
         ["Bacteria GFP", "Bacteria RFP", "Bacteria YFP"]
    )
    

if __name__ == "__main__":
    main()