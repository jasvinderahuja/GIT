def can_attend_all_meetings(intervals):
    """
    Args:
     intervals(list_list_int32)
    Returns:
     int32
    """
    max_index_meetings = len(intervals)-1
    
    if max_index_meetings <= 0:
        return 1
    
    ## how to check overlap? [a,b] [c,d]
    ## Look at when there is not an overlap
    ## if b < c
    intervals_sorted = sorted(intervals, key = lambda x: x[0])
    for i in range(0, max_index_meetings):
        if max(intervals_sorted[i]) > min(intervals_sorted[(i+1)]):
            return 0
    return 1