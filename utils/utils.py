import cv2
import json




def read_box_json_file(input_bbox_path):
    '''
    Read JSON file of the objects that will trackers.
    Returns
    -------
    Json of coordinates.
    '''
    with open(input_bbox_path, 'r') as f:
        dicts_bbox = json.load(f)

    return(dicts_bbox)   


def validate_json(input_boxes_json_path):       
    '''
    Coordinates validation.
    Returns
    -------
    List of coordinates.
    '''
    assert all(type(elem) == int for elem in input_boxes_json_path['coordinates']), \
        "coordinates should be ints"

    return(input_boxes_json_path)    