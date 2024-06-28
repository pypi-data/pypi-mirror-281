import os

from geometry.change_crs import change_crs

def is_tiff(file):
    """
    Returns a boolean indicating if a file is a tiff image
    
    Parameters:
        file: (Relative) Path to file wanting to check if a tiff
    """
    filename, file_extension = os.path.splitext(file)
    
    file_extension = file_extension.lower()
    
    return file_extension.find(".tif") == 0


def get_tiffs_from_folder(tiff_folder):
    """
    Return all the tiffs files from the tiff_folder
    
    Parameters:
        file: (Relative) Path to folder wanting to check
    """
    if not os.path.isdir(tiff_folder):
        raise Exception(f"Folder {tiff_folder} Doesn't Exist")

    files = os.listdir(tiff_folder)

    tiff_files = []

    for file in files:
        if is_tiff(file):
            file = f"{tiff_folder}{file}"
            tiff_files.append(file)

    return tiff_files


def change_box_crs(bbox, bbox_crs, new_crs):
    """
    Change the CRS of a given bounding box (min_x, min_y, max_x, max_y)

    Parameters:
        - bbox: Bounding Box to change the crs of
        - bbox_crs: CRS of the given bounding box
        - new_crs: CRS to set to the bbox
    """
    if bbox_crs == new_crs:
        return bbox

    lowest_point = (bbox[0], bbox[1])
    lowest_point = change_crs(lowest_point, bbox_crs, new_crs)
    highest_point = (bbox[2], bbox[3])
    highest_point = change_crs(highest_point, bbox_crs, new_crs)

    new_bbox = [lowest_point[0], lowest_point[1], highest_point[0], highest_point[1]]

    return new_bbox
