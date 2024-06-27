from skan import Skeleton, summarize
import numpy as np
import cv2
import skimage
import matplotlib.pyplot as plt
import math
import pandas as pd


def get_x_y(row):
    x1 = row["image-coord-src-0"]
    y1 = row["image-coord-src-1"]

    x2 = row["image-coord-dst-0"]
    y2 = row["image-coord-dst-1"]
    
    return x1, y1, x2, y2
def calculate_angle(row):
    x1, y1, x2, y2 = get_x_y(row)
    delta_x = x2 - x1
    delta_y = y2 - y1

    angle_radians = math.atan2(delta_y, delta_x)

    angle_degrees = math.degrees(angle_radians)
    return angle_degrees
def get_merge_points(row):
    angle = row["angle"]
    branch_distance = row["branch-distance"]
    branch_type = row["branch-type"]
    angle_src = row["src_angle"]
    angle_dst = row["dst_angle"]
    root_type = row["root_type"]
    if (abs(angle) == 45) or (abs(angle) == 90) or (angle == 0) or (branch_distance < 45):# And branch distance and euclidean distance are same?
        if branch_type == 1:
            return False
        elif (abs(angle_src - angle_dst) > 2) and (branch_distance > 20):
            return False
        elif (root_type == "Primary") and (branch_distance > 20):
            return False
        return True
    else:
        return False   
def draw_root(
    coordinates: np.array,
    image: np.array,
    x_offset: float,
    y_offset: float,
    colour: list = (0, 0, 0),
    thickness: int = 1,
) -> np.array:
    """
    This function visualises the given coordinates on the image with the provided colour and thickness.

    :param coordinates: array of (y, x) coordinates that has to be visualised
    :param image: image for visualisation
    :param x_offset: left bound for the current plant - used to draw on the real image using the coordinates from the sliced image that focuses on a certain plant
    :param y_offset: top bound for the current plant - used to draw on the real image using the coordinates from the sliced image that focuses on a certain plant
    :param colour: colour with which to draw
    :param thickness: thickness of the line, with 1 being the default single pixel

    :return: returns image where the given coordinates are highlighted with the provided colour
    """

    # loop through all the coordinates pairs and visualise them
    for y, x in coordinates:
        y += y_offset
        x += x_offset

        # Make the lines a bit thicker so that the're more visible
        for i in range(-thickness, thickness + 1):
            for j in range(-thickness, thickness + 1):
                if 0 <= y + i < image.shape[0] and 0 <= x + j < image.shape[1]:
                    image[y + i, x + j] = colour

    return image
def get_angle_source(row, subset_skeleton_ob):
    index = row.name

    yx = subset_skeleton_ob.path_coordinates(index)

    x=yx[:, 1]
    y=yx[:, 0]

    first_x = x[0]
    first_y = y[0]

    if len(x) > 30:
        second_x = x[30]
        second_y = y[30]
    else:
        second_x = x[-1]
        second_y = y[-1]
    
    delta_x = second_x - first_x
    delta_y = second_y - first_y

    angle_radians = math.atan2(delta_y, delta_x)

    angle_degrees = math.degrees(angle_radians)

    return angle_degrees
def get_angle_destination(row, subset_skeleton_ob):
    index = row.name
    

    yx = subset_skeleton_ob.path_coordinates(index)
    x = yx[:, 1]
    y = yx[:, 0]

    if len(x) > 30:
        first_x = x[-30]
        first_y = y[-30]
        second_x = x[-1]
        second_y = y[-1]
    else:
        first_x = x[0]
        first_y = y[0]
        second_x = x[-1]
        second_y = y[-1]
    
    delta_x = second_x - first_x
    delta_y = second_y - first_y

    angle_radians = math.atan2(delta_y, delta_x)

    angle_degrees = math.degrees(angle_radians)

    return angle_degrees
def set_up_branches(skeleton_ob, subset_branch):
    subset_branch['plant'] = subset_branch['plant'].fillna("None")
    subset_branch['root_type'] = subset_branch['root_type'].fillna("None")
    subset_branch.loc[:, "angle"] = subset_branch.apply(calculate_angle, axis=1)
    subset_branch["connected_angle"] = np.inf
    subset_branch["dst_angle"] = subset_branch.apply(get_angle_destination, args=(skeleton_ob,), axis=1)
    subset_branch["src_angle"] = subset_branch.apply(get_angle_source, args=(skeleton_ob,), axis=1)
    subset_branch["merge_point"] = subset_branch.apply(get_merge_points, axis=1)
    subset_branch["root_id"] = "None"

    return subset_branch
def get_merge_point_df(subset_branch):
    merge_point_df = subset_branch[subset_branch["merge_point"] == True]
    merge_point_df = merge_point_df.copy()
    merge_point_df["merge_point_id"] = "None"

    merge_point_id = 0
    while (merge_point_df["merge_point_id"] == "None").any():
        merge_point_df_none = merge_point_df[merge_point_df["merge_point_id"] == "None"]

        merge_point_df_none_row = merge_point_df_none.iloc[0]

        node_id_dst = merge_point_df_none_row["node-id-dst"]
        node_id_src = merge_point_df_none_row["node-id-src"]

        sources = np.array([node_id_dst, node_id_src])

        len_sources = len(sources)
        len_new_sources = 0

        while len_sources != len_new_sources:
            len_sources = len_new_sources
            for node in sources:
                new_nodes = merge_point_df[merge_point_df["node-id-src"] == node]["node-id-src"]
                sources = np.concatenate([sources, new_nodes])
                new_nodes = merge_point_df[merge_point_df["node-id-src"] == node]["node-id-dst"]
                sources = np.concatenate([sources, new_nodes])
                new_nodes = merge_point_df[merge_point_df["node-id-dst"] == node]["node-id-src"]
                sources = np.concatenate([sources, new_nodes])
                new_nodes = merge_point_df[merge_point_df["node-id-dst"] == node]["node-id-dst"]
                
                sources = np.concatenate([sources, new_nodes])
                sources = np.unique(sources)
            len_new_sources = len(sources)
        
        merge_point_df.loc[merge_point_df["node-id-src"].isin(sources), "merge_point_id"] = merge_point_id
        merge_point_df.loc[merge_point_df["node-id-dst"].isin(sources), "merge_point_id"] = merge_point_id
        merge_point_id += 1

    return merge_point_df
def get_unique_elements(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    
    unique_in_arr1 = set1 - set2
    unique_in_arr2 = set2 - set1
    unique_elements = list(unique_in_arr1.union(unique_in_arr2))
    
    return unique_elements
def get_all_sources(destination_id, merge_point_df):
    temp_row = merge_point_df[merge_point_df["node-id-src"] == destination_id]

    if len(temp_row) == 0:
        temp_row = merge_point_df[merge_point_df["node-id-dst"] == destination_id]
    if len(temp_row) == 0:
        return pd.DataFrame()
    else:
        merge_point_id = temp_row["merge_point_id"].iloc[0]
        sources_rows = merge_point_df[merge_point_df["merge_point_id"] == merge_point_id]

        sources_src = sources_rows["node-id-src"]
        sources_dst = sources_rows["node-id-dst"]

        sources = get_unique_elements(sources_src, sources_dst)
    return sources
def find_closest_angle(sources, start_angle):
    closest_angle = np.inf
    for index, row in sources.iterrows():
        angle = row["src_angle"]
        if abs(angle - start_angle) < closest_angle:
            closest_angle = abs(angle - start_angle)
            closest_angle_index = index
    return closest_angle_index, closest_angle
def get_next_root(working_row, subset_branch, merge_point_df, root_id):
    node_id_destination = working_row["node-id-dst"]
    start_angle = working_row["dst_angle"]
    plant = working_row["plant"]

    sources_nodes = get_all_sources(node_id_destination, merge_point_df)
    sources = subset_branch[subset_branch["node-id-src"].isin(sources_nodes)]

    if sources.empty:
        sources = subset_branch[subset_branch["node-id-src"] == node_id_destination]

    sources = sources[(sources["root_type"] != "Primary")]
    if sources.empty:
        return pd.DataFrame(), subset_branch
    
    ### Find the closest angle from sources ###

    destination_nodes = get_all_sources(node_id_destination, merge_point_df)
    destinations = subset_branch[subset_branch["node-id-dst"].isin(destination_nodes)]

    if destinations.empty:
        destinations = subset_branch[subset_branch["node-id-dst"] == node_id_destination]

    destinations = destinations[destinations.index != working_row.name]        

    destinations = destinations[destinations["merge_point"] == False]

    destinations["best_fit_index"] = "None"
    destinations["best_fit_angle"] = np.inf

    closest_angle_index, closest_angle = find_closest_angle(sources, start_angle)

    for dest_index, dest_row in destinations.iterrows():
        if dest_index == working_row.name:
            continue
        for source_index, source_row in sources.iterrows():
            angle = source_row["src_angle"]
            if abs(angle - dest_row["dst_angle"]) < dest_row["best_fit_angle"]:
                destinations.loc[dest_index, "best_fit_angle"] = abs(angle - dest_row["dst_angle"])
                destinations.loc[dest_index, "best_fit_index"] = source_index
                dest_row["best_fit_angle"] = abs(angle - dest_row["dst_angle"])

    correct_angle = True
    steps = 0
    while correct_angle:
        if steps > 10:
            correct_angle = False
        else:
            steps += 1
        same_closest_index = destinations[destinations["best_fit_index"] == closest_angle_index]

        if not same_closest_index.empty:
            closer_angles = same_closest_index[same_closest_index["best_fit_angle"] < closest_angle]
            if not closer_angles.empty:
                new_sources = sources[sources.index != closest_angle_index]
                if new_sources.empty:
                    return pd.DataFrame(), subset_branch
                closest_angle_index, closest_angle = find_closest_angle(new_sources, start_angle)
            else:
                correct_angle = False
        else:
            correct_angle = False


    ### Assign the new row
    index_row = subset_branch.loc[closest_angle_index]
    ## Check if angle is close enough

    if abs(index_row["src_angle"] - start_angle) > 100:
        return pd.DataFrame(), subset_branch

    subset_branch.loc[closest_angle_index, "root_type"] = "Lateral"
    subset_branch.loc[closest_angle_index, "plant"] = plant
    subset_branch.loc[closest_angle_index, "root_id"] = f"Lateral_{root_id}"
    index_row_copy = index_row.copy()

    index_row_copy["plant"] = plant
    index_row = index_row_copy.copy()
    if index_row.name == working_row.name:
        return pd.DataFrame(), subset_branch
    return index_row, subset_branch
def follow_path(subset_branch, merge_point_df):
    primary_subset = subset_branch[subset_branch["root_type"] == "Primary"]

    root_id = 0
    for index, row in primary_subset.iterrows():
        index_row = subset_branch.loc[index]
        while not index_row.empty:
            index_row, subset_branch = get_next_root(index_row, subset_branch, merge_point_df, root_id)
        root_id += 1

    return subset_branch
def assign_merge_points_to_plant(subset_branch):
    merge_point_subset = subset_branch[subset_branch["merge_point"] == True]
    merge_point_subset = merge_point_subset[merge_point_subset["root_type"] == "None"]
    for index, row in merge_point_subset.iterrows():
        source = row["node-id-src"]
        sources = subset_branch[(subset_branch["node-id-dst"] == source) & (subset_branch["plant"] != "None")]

        if sources.empty:
            continue
        first_source = sources.iloc[0]
        plant = first_source["plant"]
        root_id = first_source["root_id"]
        subset_branch.loc[index, "plant"] = plant
        subset_branch.loc[index, "root_type"] = "Lateral"
        subset_branch.loc[index, "root_id"] = root_id
        

    return subset_branch
def assign_unassigned_branches(subset_branch: pd.DataFrame):
    """
    This function assigns the unassigned branches to the closest plant. It iterates over the rows where the plant is "None" and assigns the closest plant to the current row.
    :param subset_branch: subset of the dataframe with all the branches. It should have an additional 'plant' and 'root_type' column, with primary roots marked as 'Primary' and the rest as 'None'.
    :param subset_skeleton_ob_arr: skeleton object array of the image.
    :param colors: list of colors to draw the lateral roots with.
    :param img2: image off the petri dish to draw the roots on.
    :return: subset_branch: dataframe with the roots assigned to the plants.
    """
    # Filter the dataframe to the rows where the plant is "None".
    # This is the roots that have not been assigned to any plant yet.
    # Assume subset_branch is your DataFrame
    none_plants_df = subset_branch[subset_branch["plant"] == "None"]

    # Iterate over the rows where plant is "None"
    for index, row in none_plants_df.iterrows():
        # Initialize the minimum angle difference and the closest plant
        min_angle_diff = np.inf
        closest_plant = None
        closest_root_id = None
        closest_index = None


        src_angle = row["angle"]
        src_node = row["node-id-src"]
        subset_branch_src = subset_branch[subset_branch["node-id-dst"] == src_node]
        if not subset_branch_src.empty:
            subset_branch_src_plants = subset_branch_src[subset_branch_src["plant"] != "None"]
            if not subset_branch_src_plants.empty:
                if len(subset_branch_src_plants) > 1:
                    closest_angle = np.inf
                    for ind, r in subset_branch_src_plants.iterrows():
                        angle = r["angle"]
                        if abs(angle - src_angle) < closest_angle:
                            closest_angle = abs(angle - src_angle)
                            closest_plant = r["plant"]
                            closest_index = ind
                
                else:
                    closest_angle = abs(subset_branch_src_plants.iloc[0]["angle"] - src_angle)
                    closest_plant = subset_branch_src_plants.iloc[0]["plant"]
                    closest_index = subset_branch_src_plants.index[0]
                
                if closest_angle < 40:
                    subset_branch.at[index, "plant"] = closest_plant
                    subset_branch.loc[index, "root_type"] = "Lateral"

        
        # Coordinates and angle of the source point
        src_x = row["image-coord-src-0"]
        src_y = row["image-coord-src-1"]
        
        # List to hold the distances and corresponding target rows
        distances = []
        
        # Find the distances to points where plant is not "None"
        for target_index, target_row in subset_branch[subset_branch["root_id"] != "None"].iterrows():


            
            # Coordinates of the destination point
            dst_x = target_row["image-coord-dst-0"]
            dst_y = target_row["image-coord-dst-1"]
            
            # Calculate the Euclidean distance
            distance = np.sqrt((src_x - dst_x) ** 2 + (src_y - dst_y) ** 2)
            
            # Append the distance and target row to the list
            distances.append((distance, target_row, target_index))
        
        # Sort the distances list by distance
        distances.sort(key=lambda x: x[0])
        
        # Select the 5 closest points
        closest_targets = distances[:5]
        
        # Find the closest point by angle
        for distance, target_row, target_index in closest_targets:
            
            if distance > 45:
                target_row["angle"] = 1000
            # Angle of the target point
            dst_angle = target_row["angle"]
            
            # Calculate the absolute angle difference
            angle_diff = abs(src_angle - dst_angle)
            
            # If the angle difference is less than the current minimum angle difference, update the closest plant
            if angle_diff < min_angle_diff:
                min_angle_diff = angle_diff
                closest_plant = target_row["plant"]
                closest_root_id = target_row["root_id"]
                closest_index = target_index
        
        # Assign the closest plant to the current row
        subset_branch.at[index, "plant"] = closest_plant
        subset_branch.loc[index, "root_type"] = "Lateral"
        subset_branch.loc[index, "root_id"] = closest_root_id
        # Get the path coordinates and draw on the image
    return subset_branch
def draw_lateral(subset_branch: pd.DataFrame, subset_skeleton_ob_arr: Skeleton, img2: np.array,
                 colors: list = [(0, 128, 255), (240, 32, 160), (255, 0, 0), (255, 0, 255), (0, 255, 0)]) -> np.array:
    """
    This function draws the lateral roots on the image. It uses the subset_dataframe and draaws each cordinate of the lateral branches.
    :param subset_branch: subset of the dataframe with all the branches. It should have an additional 'plant' and 'root_type' column, with primary roots marked as 'Primary' and the rest as 'None'.
    :param subset_skeleton_ob_arr: skeleton object array of the image.
    :param img2: image off the petri dish to draw the roots on.
    :param colors: list of colors to draw the lateral roots with.
    :return: img2: image with the roots drawn on it.
    """
    # We look one more time over the dataframe, and draw all of the lateral roots on the image here.
    for index, row in subset_branch.iterrows():
        if row["root_type"] == "Primary" or row["plant"] is None or np.isnan(row["plant"]):
            continue
        xy = subset_skeleton_ob_arr.path_coordinates(index)
        img2 = draw_root(xy, img2, 0, 0, (colors[int(row["plant"])]))
    return img2

def get_lateral(subset_branch, skeleton_ob_loc, image):
    img2 = image.copy()
    colors = [(0, 128, 255), (240, 32, 160),
              (255, 0, 0), (255, 0, 255), (0, 255, 0)]

    subset_branch = set_up_branches(skeleton_ob_loc, subset_branch)
    merge_point_df = get_merge_point_df(subset_branch)
    subset_branch = follow_path(subset_branch, merge_point_df)
    subset_branch = assign_merge_points_to_plant(subset_branch)
    subset_branch = assign_unassigned_branches(subset_branch)
    subset_branch = subset_branch[subset_branch["plant"] != "None"]
    img2 = draw_lateral(subset_branch, skeleton_ob_loc, img2, colors)

    return img2, subset_branch