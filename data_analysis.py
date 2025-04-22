import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import csv 
from scipy.spatial.distance import euclidean
from scipy.spatial import Voronoi, voronoi_plot_2d

path = "results/"

def clustering(bacteria, pairs, color_expression):
    # Extracting the spatial positions (x, y) as features for clustering, and converting to micrometers
    positions = np.array([[float(bacterium[1]) / 10, float(bacterium[2]) / 10] for bacterium in bacteria])

    # DBSCAN clustering
    db = DBSCAN(eps=5, min_samples=2).fit(positions)  # Adjusted eps for micrometers

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
        clusters[label].append([float(bacterium[1]) / 10, float(bacterium[2]) / 10])  # Convert to micrometers

    # Calculate the centroid of each cluster
    centroids = {}
    for cluster_id, cluster_bacteria in clusters.items():
        cluster_positions = np.array(cluster_bacteria)
        centroid = cluster_positions.mean(axis=0)  # Calculate the centroid
        centroids[cluster_id] = centroid


    # Print the centroids
    centroids_points = []
    print("\nCentroids of Clusters (in micrometers):")
    for cluster_id, centroid in centroids.items():
        print(f"Cluster {cluster_id} Centroid: {centroid[0]} {centroid[1]} µm")
        centroids_points.append([float(centroid[0]),float(centroid[1])])

    print("ARRAY",centroids_points)

    # save centroids in a file
    with open(path+f"centroids_{color_expression}.txt", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x','y'])
        writer.writerows(centroids_points)

    # Plot the clusters with centroids and Y-axis inverted
    plt.scatter(positions[:, 0], positions[:, 1], c=labels, cmap='viridis', label='Bacteria (µm)')
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
    plt.gca().invert_yaxis()
    plt.savefig(color_expression + '_in_micrometers.png')
    plt.show()
    
def voronoi(arr, filename):
    points = np.array(arr)
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor)
    plt.savefig(filename, transparent=True)
    plt.show()

def graph_clustering():
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
        #print(bacterias_time[0])

    # LOOK IN TIME 1 FOR BACTERIAS GFP
    bacteria_gfp = [bacterium for bacterium in bacterias_time[1500] if int(bacterium[5]) > 0]
    bacteria_rfp = [bacterium for bacterium in bacterias_time[1500] if int(bacterium[6]) > 0]
    bacteria_yfp = [bacterium for bacterium in bacterias_time[1500] if int(bacterium[7]) > 0]

    # Define the relationship between centroids to draw lines between them and calculate distances.
    # (a, b) represents a line between centroid a and centroid b.
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

    clustering(bacteria_gfp, pairs_g, "GFP")
    clustering(bacteria_rfp, pairs_r,  "RFP")
    clustering(bacteria_yfp, pairs_y,  "YFP")

def graph_voronoi():
    color_expression = ["GFP", "RFP", "YFP"]
    all_centroids = []
    for color in color_expression:
        with open(path+f"centroids_{color}.txt", newline='') as csvfile: 
            spamreader = csv.reader(csvfile)
            first_row = next(spamreader)
            print(first_row)
            centroids = []
            for row in spamreader:
                centroids.append([float(row[0]), float(row[1])])
                all_centroids.append([float(row[0]), float(row[1])])    
            voronoi(centroids, path+ f"voronoi_{color}.png")
    voronoi(all_centroids, path+"voronoi_all.png")



def main():
    #graph_clustering()
    graph_voronoi()

    

main()