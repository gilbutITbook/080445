def quicksort(alist):
    if len(alist) <= 1:
        return alist

    pivot = alist[len(alist) // 2]  # 피벗 요소 선택 (보통 중간값)
    left = [x for x in alist if x < pivot]  # 피벗보다 작은 요소들
    middle = [x for x in alist if x == pivot]  # 피벗과 같은 요소들
    right = [x for x in alist if x > pivot]  # 피벗보다 큰 요소들

    return quicksort(left) + middle + quicksort(right)

