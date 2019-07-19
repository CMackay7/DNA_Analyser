# Gets called by delete_lanes in user input handler handles removing the centroids from
# the list so they will not be places on the image


# This method will find the lane they clicked on and remove it from the list, it takes the list of grouped
# centroids and the position of the users click it will search and delete
def find_and_delete_lanes(centroids, click_pos):
    has_line_been_hit = True
    loop_length = len(centroids)

    for i in range(loop_length):
        for curr_point in centroids[i]:
            # The reason it adds and takes 2 away is so there is a margin of error in the users click
            if (click_pos[1] + 2) > curr_point[1] > (click_pos[1] - 2) and has_line_been_hit:
                del centroids[i]
                return centroids
    return centroids


# This method will find the centroid they clicked on and remove it from the list, it takes the list of centroids
# and the position of the users click it will search and delete
def find_and_delete_centroids(centroids, click_pos):
    x = 0
    for curr_point in centroids:
        if (click_pos[1] + 5) > curr_point[1] > (click_pos[1] - 5) and (click_pos[0] + 5) > curr_point[0] > \
                (click_pos[0] - 5):
            print(centroids)
            del centroids[x]
            print(centroids)
            return centroids
        x = x + 1
    return centroids


# Add lines to the image, given the two clicks and add the points to the centroids
def add_line(centroids, click1, click2):
    too_add = [click1, click2]
    centroids.append(too_add[:])
    return centroids

