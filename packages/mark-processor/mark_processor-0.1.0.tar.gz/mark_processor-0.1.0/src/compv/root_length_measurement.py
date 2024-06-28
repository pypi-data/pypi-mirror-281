import argparse
import json
import logging
import os

import cv2
import keras.backend as K
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import tensorflow as tf
from keras.callbacks import EarlyStopping
from keras.layers import (
    BatchNormalization,
    Conv2D,
    Conv2DTranspose,
    Dropout,
    Input,
    Lambda,
    MaxPooling2D,
    UpSampling2D,
    concatenate,
)
from keras.models import Model
from patchify import patchify, unpatchify
from skan import Skeleton, draw, summarize
from skan.csr import skeleton_to_csgraph
from skimage.morphology import remove_small_objects, skeletonize

from instance_segmentation import segment_instances
from mask_prediction import predict_mask


def measure_root_lengths(mask):
    """
    Measure the lengths of primary and lateral roots in the given mask.

    This function analyzes the root system in the provided mask image, segments the roots, skeletonizes them,
    and computes the lengths of primary and lateral roots. It returns a list of dictionaries with the x-coordinate
    of the primary root start, the primary root length, and a list of lateral root lengths.

    :param mask: Input mask image where the root system needs to be analyzed.
    :type mask: numpy.ndarray
    :return: List of dictionaries containing the x-coordinate of the primary root start, the primary root length, 
             and a list of lateral root lengths.
    :rtype: list of dict
    :author: Stijn Heesters

    **Usage:**

    This function measures the lengths of the primary and lateral roots in the given mask image.

    **Example:**

    .. code-block:: python

        import numpy as np
        from your_module import measure_root_lengths

        mask = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        root_lengths = measure_root_lengths(mask)
        print(root_lengths)

    **Details:**

    - Segments the input mask image to identify root instances.
    - Skeletonizes the segmented image to extract the root skeleton.
    - Constructs a graph from the skeleton to compute root lengths using Dijkstra's algorithm.
    - Identifies the primary root as the longest path from the top to the bottom of the image.
    - Computes the lengths of lateral roots branching off from the primary root.

    **Dependencies:**

    This function requires the following libraries:
    - numpy
    - networkx
    - skimage.morphology
    - skan

    :note: Ensure that the input mask image is a binary image where roots are represented by non-zero values.
    """

    segmented = segment_instances(mask)
    binary = segmented[:, :, 0]
    binary[binary != 0] = 1

    s = skeletonize(binary)
    skeleton_data = summarize(Skeleton(s))
    skeleton_data = skeleton_data.reset_index()

    G = nx.from_pandas_edgelist(
        skeleton_data,
        source="node-id-src",
        target="node-id-dst",
        edge_attr="branch-distance",
    )

    plants = []

    for i in range(skeleton_data["skeleton-id"].max() + 1):
        plant_skeleton = skeleton_data[skeleton_data["skeleton-id"] == i]

        p_root_start_node_id = plant_skeleton[
            plant_skeleton["coord-src-0"] == plant_skeleton["coord-src-0"].min()
        ]["node-id-src"].values[0]

        p_root_end_node_id = plant_skeleton[
            plant_skeleton["coord-dst-0"] == plant_skeleton["coord-dst-0"].max()
        ]["node-id-dst"].values[0]

        p_root_length = nx.dijkstra_path_length(
            G, p_root_start_node_id, p_root_end_node_id, weight="branch-distance"
        )

        logging.info(
            f"Plant: {i}",
            f"Root length: {p_root_length}" "\n",
        )

        primary_root_start_index = plant_skeleton[
            plant_skeleton["coord-src-0"] == plant_skeleton["coord-src-0"].min()
        ].index[0]

        primary_root_start_x = int(
            plant_skeleton.loc[primary_root_start_index]["coord-src-1"]
        )

        lateral_roots = plant_skeleton[
            (plant_skeleton["branch-type"] == 1)
            & (plant_skeleton["node-id-src"] != p_root_start_node_id)
            & (plant_skeleton["node-id-dst"] != p_root_end_node_id)
        ]

        l_root_list = []

        for index, row in lateral_roots.iterrows():
            root_length = nx.dijkstra_path_length(
                G, row["node-id-src"], row["node-id-dst"], weight="branch-distance"
            )
            l_root_list.append(root_length)

        plants.append(
            {
                "x": primary_root_start_x,
                "p_root_length": p_root_length,
                "l_root_lengths": l_root_list,
            }
        )

    sorted_plants = sorted(plants, key=lambda plant: plant["x"])

    return sorted_plants


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask-path", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    args = parser.parse_args()

    mask = cv2.imread(os.path.join(args.mask_path, "mask.tif"), cv2.IMREAD_GRAYSCALE)
    root_lengths = measure_root_lengths(mask)
    logging.info("Measured root lengths:", root_lengths)

    # Save the root lengths in JSON file
    with open(os.path.join(args.output_path, "root_lengths.json"), "w") as f:
        json.dump(root_lengths, f)
