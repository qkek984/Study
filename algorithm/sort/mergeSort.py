def merge(left,right):
    tmp=[]
    while left or right:
        if left and right:
            if left[0] <= right[0]:
                tmp.append(left.pop(0))
            else:
                tmp.append(right.pop(0))
        elif left:
            tmp.append(left.pop(0))
        else:
            tmp.append(right.pop(0))
    return tmp

def mergeSort(arr): 
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = arr[:mid]
    right = arr[mid:]
    left=mergeSort(left)
    right=mergeSort(right)
    return merge(left,right)
