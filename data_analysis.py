import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import csv 
from scipy.spatial.distance import euclidean
from scipy.spatial import Voronoi, voronoi_plot_2d

path = "results/"

def clustering(bacteria):
    # Extracting the spatial positions (x, y) as features for clustering, and converting to micrometers
    positions = np.array([[float(bacterium[1]) / 10, float(bacterium[2]) / 10] for bacterium in bacteria])

    # Calculate the offsets (minimum values to shift positions into positive coordinates)
    offset_x = -np.min(positions[:, 0]) 
    offset_y = np.min(positions[:, 1]) 
    print(offset_y, "OFFSETT Y")

    # Shift all bacteria positions
    shifted_positions = positions + np.array([offset_x, offset_y])

    # DBSCAN clustering
    db = DBSCAN(eps=5, min_samples=2).fit(shifted_positions)  # Adjusted eps for micrometers

    # Get cluster labels
    labels = db.labels_

    # Number of clusters found (-1 indicates noise points)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f'Number of clusters: {n_clusters}')

    # Organize bacteria into clusters
    clusters = {}
    for label, bacterium in zip(labels, bacteria):
        if label not in clusters:
            clusters[label] = []
        # Convert to micrometers and use shifted positions for clustering
        clusters[label].append([float(bacterium[1]) / 10 + offset_x, float(bacterium[2]) / 10 + offset_y])

    # Calculate the centroid of each cluster
    centroids = {}
    for cluster_id, cluster_bacteria in clusters.items():
        cluster_positions = np.array(cluster_bacteria)
        centroid = cluster_positions.mean(axis=0)  # Calculate the centroid
        centroids[cluster_id] = centroid


    #Invert the Y-values for both the centroids and shifted positions
    shifted_positions[:, 1] = -shifted_positions[:, 1]  
    for cluster_id, centroid in centroids.items():
        centroid[1] = -centroid[1]  

    return centroids, shifted_positions, labels


def graph_distance_between_centroids(centroids, positions, labels, pairs, color_expression):
    #Print the centroids
    plt.scatter(positions[:, 0], positions[:, 1], c=labels, cmap='viridis', label='Bacteria')
    print(centroids, "centroids")
    for cluster_id, centroid in centroids.items():
        plt.scatter(centroid[0], centroid[1], s=200, c='red', marker='X', label=f'Centroid {cluster_id}')
        plt.text(centroid[0], centroid[1], f'Centroid {cluster_id}', fontsize=12, color='red')

    # Draw lines between specified pairs of centroids
    for cluster_id_1, cluster_id_2 in pairs:
        centroid_1 = centroids.get(cluster_id_1)
        centroid_2 = centroids.get(cluster_id_2)
        if centroid_1 is not None and centroid_2 is not None:
            plt.plot([centroid_1[0], centroid_2[0]], [centroid_1[1], centroid_2[1]], 'k--', lw=2)  # 'k--' is a dashed black line
            distance = euclidean(centroid_1, centroid_2)
            plt.text((centroid_1[0] + centroid_2[0]) / 2, (centroid_1[1] + centroid_2[1]) / 2, 
                    f'{distance:.2f} µm', fontsize=12, color='blue', ha='center')  # Distance in micrometers
    plt.xlabel('X (µm)')
    plt.ylabel('Y (µm)')
    plt.title(f'DBSCAN Clustering of {color_expression}-Positive Bacteria with Centroids and Lines (µm)')
    plt.legend()
    plt.savefig(f"{path}/{color_expression}_in_micrometers.png", transparent=True)
    plt.show()


def voronoi(arrs, bacteria_points, filename, colors, labels): 
    allpoints = []
    for arr in arrs:
        allpoints.extend(arr)
    points = np.array(allpoints)
    vor = Voronoi(points)

    fig = voronoi_plot_2d(vor, point_size=6)
    # add to the fig the label of the points to say the blue is the voronoi points
    plt.scatter([], [], c='blue', marker='o', label='Voronoi points')
    # add a unity of messure for the axis
    plt.xlabel('X (µm)')
    plt.ylabel('Y (µm)')
    plt.title('Voronoi Diagram of Bacteria Clusters (µm)')
    for bacteria, color, label in zip(bacteria_points, colors, labels):
        # Add bacteria points
        sub_bacteria_points = np.array(bacteria)
        plt.scatter(sub_bacteria_points[:, 0], sub_bacteria_points[:, 1], c=color, marker='o', label=label)
        plt.legend()

    plt.savefig(filename, transparent=True)
    plt.show()


# Global variables
# Arrays that represent the relation between centroids, they are used to calculate distance between centroids
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
    # id	 x	 y	 theta	 volume	 gfp	 rfp	 yfp	 cfp
    with open('data/conteos.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        first_row = next(spamreader)  # Read the first row (header)
        bacteria_actual_group = []
        for row in spamreader:
            if(row[0] == "id"):
                bacterias_time.append(bacteria_actual_group)
                bacteria_actual_group = []
            else:
                bacteria_actual_group.append(row)
        print("Number of times periods", len(bacterias_time))

    # Obtain bacteria in a specific time (i.e 1500)
    bacteria_gfp = [bacterium for bacterium in bacterias_time[1500] if int(bacterium[5]) > 0]
    bacteria_rfp = [bacterium for bacterium in bacterias_time[1500] if int(bacterium[6]) > 0]
    bacteria_yfp = [bacterium for bacterium in bacterias_time[1500] if int(bacterium[7]) > 0]

    # Clustering process
    centroids_gfp, positions_gfp, labels_gfp = clustering(bacteria_gfp)
    centroids_rfp, positions_rfp, labels_rfp = clustering(bacteria_rfp)
    centroids_yfp, positions_yfp, labels_yfp = clustering(bacteria_yfp)

    # GRAPHING DISTANCE BETWEEN CENTROIDS
    graph_distance_between_centroids(centroids_gfp, positions_gfp, labels_gfp, pairs_g, "GFP")
    graph_distance_between_centroids(centroids_rfp, positions_rfp, labels_rfp, pairs_r, "RFP")
    graph_distance_between_centroids(centroids_yfp, positions_yfp, labels_yfp, pairs_y, "YFP")

    # Convert Dictionary to array
    centroids_array_grp = np.array(list(centroids_gfp.values()))
    centroids_array_rfp = np.array(list(centroids_rfp.values()))
    centroids_array_yfp = np.array(list(centroids_yfp.values()))

    # all points with voronoi
    voronoi(
        [centroids_array_grp, centroids_array_rfp, centroids_array_yfp], 
        [positions_gfp, positions_rfp, positions_yfp], 
        path+f"voronoi_all.png", 
        ["green", "red", "darkorange"],
        ["Bacteria GFP", "Bacteria RFP", "Bacteria YFP"]
    )
    

if __name__ == "__main__":
    main()