def find_top_k_frequent_elements(arr, k):
    """
    Args:
     arr(list_int32)
     k(int32)
    Returns:
     list_int32
    """
    
    import heapq
    from collections import Counter
    
    a_dict = Counter(arr)
    
    ## dictionary method gives time-out error!
    # a_dict = {}

    # for element in arr:
    #    if element not in a_dict:
    #        a_dict[element] = 1
    #    else:
    #        a_dict[element] += 1
    
    heapUse=[]
    for key, value in a_dict.items():
        heapq.heappush(heapUse, -value)
    
    ret_freqs = []
    for n in range(-1,-k-1,-1):
        new_max = heapq.heappop(heapUse)*-1
        ret_freqs.append(new_max)
    
    ret_arr=[]
    for key, value in a_dict.items():
            if value in ret_freqs and key not in ret_arr:
                ret_arr.append(key)
                if len(ret_arr) == k:
                    return ret_arr