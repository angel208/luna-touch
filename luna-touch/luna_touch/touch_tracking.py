from collections import OrderedDict
from scipy.spatial import distance

from luna_touch import _const
from luna_touch.Touch import Touch
import pprint


def get_list_from_dictionary( dictionary ):
    try:
        return list(dictionary.values())
    except:
        return []

def get_distances_between_points_in_two_lists( list1, list2 ):
    try:
        return distance.cdist( list1 , list2 )
    except:
        return []

def to_dictionary( touch_list ):
    
    return_dict = OrderedDict()

    try:
        for touch in touch_list: 
            return_dict[touch.id] = touch

        return return_dict
    except:
        return OrderedDict()

def mark_all_touches_as_missed(previous_frame_touches):

    updated_touches = previous_frame_touches

    
    for index, touch in previous_frame_touches.items():

        
        if(touch.frames_missing <= _const.TOUCH_TRACKING_MAX_MISSED_FRAMES):
        
            updated_touches[touch.id].state = _const.TOUCH_STATE_MISSED
            updated_touches[touch.id].frames_missing += 1

        else:
            
            updated_touches[touch.id].state = _const.TOUCH_STATE_ENDED
            updated_touches[touch.id].frames_missing = 0

    return updated_touches

    


def track_touches_changes( previous_frame_touches, current_frame_touches ):
    
    if len(previous_frame_touches) == 0:
        return to_dictionary(current_frame_touches)

    if len(current_frame_touches) == 0:
        return mark_all_touches_as_missed(previous_frame_touches)

    touches_changes = find_min_distance_btw_points( previous_frame_touches, current_frame_touches )

    updated_touches = previous_frame_touches

    for detected_touch in touches_changes:

        prev_touch_id = detected_touch['id'] 

        #if new touch
        if prev_touch_id == None:
            next_available_id = get_next_available_id( updated_touches )

            previous_index = detected_touch['prev_index']

            touch_to_be_added = current_frame_touches[previous_index]
            touch_to_be_added.id = next_available_id

            updated_touches[next_available_id] = touch_to_be_added


        elif detected_touch['curr_pos'] == None:
            if(previous_frame_touches[prev_touch_id].frames_missing <= _const.TOUCH_TRACKING_MAX_MISSED_FRAMES):
                updated_touches[prev_touch_id].state = _const.TOUCH_STATE_MISSED
                updated_touches[prev_touch_id].frames_missing += 1
            else:
                updated_touches[prev_touch_id].state = _const.TOUCH_STATE_ENDED
                updated_touches[prev_touch_id].frames_missing = 0

        elif detected_touch['prev_pos'] == detected_touch['curr_pos']:
            updated_touches[prev_touch_id].state = _const.TOUCH_STATE_STILL
            updated_touches[prev_touch_id].frames_missing = 0

        elif detected_touch['prev_pos'] != detected_touch['curr_pos']:

            #if detected_touch['distance'] <= _const.TOUCH_TRACKING_MAX_RATIO:
            updated_touches[prev_touch_id].state = _const.TOUCH_STATE_MOVED
            updated_touches[prev_touch_id].frames_missing = 0
            updated_touches[prev_touch_id].position = detected_touch['curr_pos']
            #falta delta time, delta pos y area
            '''else:
                #previous touch goes missing
                updated_touches[prev_touch_id].state = _const.TOUCH_STATE_MISSED
                updated_touches[prev_touch_id].frames_missing += 1

                #current touch is a new touch
                next_available_id = get_next_available_id( updated_touches )
                updated_touches[next_available_id] = Touch( detected_touch['curr_pos'] , _const.DEFAULT_TOUCH_AREA)
            '''

    
    return updated_touches


def not_ended_touches( current_frame_touches ):

    not_ended_touches = OrderedDict()
    
    for index, touch in current_frame_touches.items():
        if touch.state != _const.TOUCH_STATE_ENDED:
            not_ended_touches[index] = touch

    return not_ended_touches

def find_min_distance_btw_points( previous_frame_touches, current_frame_touches ):

    prev_points_position = [ touch.position for touch in get_list_from_dictionary(previous_frame_touches)]
    curr_points_position = [ touch.position for touch in current_frame_touches ]

    prev_touches =  [ ( touch.id , touch.position ) for touch in get_list_from_dictionary(previous_frame_touches)]

    distances_matrix = get_distances_between_points_in_two_lists( prev_points_position , curr_points_position )

    minimal_distances_for_each_row = distances_matrix.min(axis =  _const.PY_AXIS_ROW)

    rows = minimal_distances_for_each_row.argsort() 
 

    unsorted_cols = distances_matrix.argmin(axis = _const.PY_AXIS_ROW)
    cols = unsorted_cols[rows]


    already_asigned_rows = set()
    already_asigned_cols = set()

    result_matrix = []

    for (row, col) in zip( rows, cols ):

        if row in already_asigned_rows or col in already_asigned_cols:
            continue 

        result_matrix.append( { "id" : prev_touches[row][0], 
                                "prev_pos" : prev_touches[row][1], 
                                "curr_pos": curr_points_position[col],
                                "distance": int(round(distances_matrix[row][col]))  
        })


        already_asigned_rows.add(row)
        already_asigned_cols.add(col)

    unasigned_touches_prev_frame = set(range(0, distances_matrix.shape[0])).difference(already_asigned_rows)
    unasigned_touches_curr_frame = set(range(0, distances_matrix.shape[1])).difference(already_asigned_cols)

    for unasigned_touch in unasigned_touches_prev_frame:
        result_matrix.append( { "id" : prev_touches[unasigned_touch][0], 
                                "prev_pos" : prev_touches[unasigned_touch][1], 
                                "curr_pos": None,
                                "distance": None   
        })
        

    for unasigned_touch in unasigned_touches_curr_frame:
        result_matrix.append( { "id" : None, 
                                "prev_pos" : None, 
                                "curr_pos": curr_points_position[unasigned_touch],
                                "distance": None,
                                "prev_index": unasigned_touch
        })

    return result_matrix

def get_next_available_id( touch_list ):

    for i, touch in enumerate(touch_list) :
        if i not in touch_list:
            return i

    new_index_at_end_of_list = len(touch_list)

    return new_index_at_end_of_list




