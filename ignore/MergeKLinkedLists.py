"""
For your reference:
class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
"""

def merge_k_lists(lists):
    """
    Args:
     lists(list_LinkedListNode_int32)
    Returns:
     LinkedListNode_int32
    """

    ## in case all lists have no values
    dummy = current = LinkedListNode(0)
    
    if not lists or all(not list_ for list_ in lists):
        ## in a dummy list with Node =0 the next element is [] which they want!!
        return dummy.next
    
    ## initiate a heap to use
    import heapq
    heapUse=[]
    
    ## i is the index and list_i is the ith list in lists
    for i,list_i in enumerate(lists):
    ## if list_i has elements add them to heap
        if list_i: 
            heapq.heappush(heapUse,  (list_i.value, i))
    
    ## dummy Listnode initiate
    ## LinkedListNode comes from __init__

    
            
    while heapUse:
        val, i = heapq.heappop(heapUse)
        current.next = LinkedListNode(val)
                
        if lists[i] and lists[i].next:
            heapq.heappush(heapUse, (lists[i].next.value, i))
            lists[i] = lists[i].next
        current = current.next
    
    return dummy.next