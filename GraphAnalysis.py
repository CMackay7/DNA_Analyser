import statistics


# This set of functions (go_along_data, check_drop, decrease) are used in order to find the end and start of the first
# and last peak in the data. For the end of the first peak it will recurse through the values in the data and when
# the values start to decrease it will call check_drop. Check drop will dgo though the data while it is decreasing
# until it hits data that is rising again (could be the end) so it will check weather the data has dropped 30% if
# so it will mark this as the edge (vis versa for the end of the final peak)

# I use op as the operator so the same code can be used for going over the data forwards and backwards
def go_along_data(points, current_point, op):
    next_point = op(current_point, 1)
    if points[next_point] >= points[current_point]:
        return go_along_data(points, next_point, op)
    else:
        check, point = check_drop(points, current_point, points[current_point], op)

        if check:
            return point
        else:
            return go_along_data(points, next_point, op)


def check_drop(points, current_point, drop_start, op):
    next_point = op(current_point, 1)
    if points[current_point] < points[next_point]:
        if decrease(drop_start, points[current_point]):
            return True, current_point
        else:
            return False, current_point
    else:
        return check_drop(points, next_point, drop_start, op)


# If the drop is over 30% then it will mark as an edge, i did this so a small drop on the peak
# will not be falsely classed as an edge.
def decrease(original, new):
    decrease = original - new
    percentage_change = (decrease / original) * 100
    if percentage_change > 40:
        return True
    else:
        return False


# Just used to simple calculate the background data, finds the lowest 10 values and finds the average
def get_background_signal(data):
    sorted_data = sorted(data, reverse=True)
    last_5 = sorted_data[-10:]
    avg = statistics.mean(last_5)
    return avg
