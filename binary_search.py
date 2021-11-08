def binary_search(link_list, link):
    low = 0
    high = len(link_list) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        # If link is greater, ignore left half
        if link_list[mid] < link:
            low = mid + 1

        # If link is smaller, ignore right half
        elif link_list[mid] > link:
            high = mid - 1

        # means link is present at mid
        else:

            return link_list[mid]

    # If we reach here, then the element was not present
    return -1
