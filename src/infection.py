import sys
from Queue import Queue

INFECTED_SITE_VERSION = "B"

def infect_total(user):
    infected_count = 0

    q = Queue()
    q.put(user)
    visited = set([])

    while q.qsize():
        curr_user = q.get()
        if curr_user not in visited:
            visited.add(curr_user)
            # "infecting" user to have updated site version
            curr_user.update_site_version(INFECTED_SITE_VERSION)
            infected_count += 1
            for connection in curr_user.get_connections():
                if connection not in visited:
                    q.put(connection)

    return infected_count


def find_closest_subset_sum_of_graphs(graphs, n, target):
    if n == 0:
        return [], target

    if target < 0:
        return [], target

    curr = graphs[n - 1]
    closest_subset_excl_curr, excl_sum_diff = find_closest_subset_sum_of_graphs(graphs, n - 1, target)
    closest_subset_incl_curr, incl_sum_diff = find_closest_subset_sum_of_graphs(graphs, n - 1, target - curr.num_users)
    closest_subset_incl_curr.append(curr)

    if len(closest_subset_excl_curr) == 0 and excl_sum_diff == target:
        return closest_subset_incl_curr, incl_sum_diff

    if abs(excl_sum_diff) <= abs(incl_sum_diff):
        return closest_subset_excl_curr, excl_sum_diff
    else:
        return closest_subset_incl_curr, incl_sum_diff


def infect_limited(graphs, desired_infection_count):
    infection_count = 0
    #selected_graphs, user_count = get_groups_of_users_whose_counts_sum_closest_to_target(
    #    graphs, desired_infection_count)
    selected_graphs, target_diff = find_closest_subset_sum_of_graphs(
        graphs, len(graphs), desired_infection_count)
    for graph in selected_graphs:
        users = graph.get_users()
        infection_count += infect_total(users[0])
    return infection_count




