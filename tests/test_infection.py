import os, sys
sys.path.insert(0, os.path.abspath(".."))

import unittest
from src.graph import Graph
from src.user import User, INITIAL_SITE_VERSION
from src.infection import infect_total, find_closest_subset_sum_of_graphs, infect_limited, INFECTED_SITE_VERSION
from util import verify_arrays_have_same_content


def verify_users_in_a_group_are_infected(graph):
    users = graph.get_users()
    assert all(user.site_version == INFECTED_SITE_VERSION for user in users)


def construct_graph_of_count(count):
    graph = Graph()
    user1 = User()
    graph.add_user(user1)
    for i in range(0, count-1):
        user = User()
        graph.add_user(user)
        graph.connect_users(user1.get_id(), user.get_id())
    return graph


class TestTotalInfection(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.user1 = User()
        self.user2 = User()
        self.user3 = User()
        self.user4 = User()
        self.users = [self.user1, self.user2, self.user3, self.user4]

    def test_total_infection_on_component_with_one_user(self):
        user = self.user1
        self.graph.add_user(user)
        infection_count = infect_total(user)
        assert infection_count == 1
        verify_users_in_a_group_are_infected(self.graph)

    def test_total_infection_on_component_with_two_users(self):
        user1 = self.user1
        user2 = self.user2
        self.graph.add_user(user1)
        self.graph.add_user(user2)
        self.graph.connect_users(user1.get_id(), user2.get_id())

        infection_count = infect_total(user1)
        assert infection_count == 2
        verify_users_in_a_group_are_infected(self.graph)

    def test_total_infection_on_component_with_three_users_in_a_cycle(self):
        user1 = self.user1
        user2 = self.user2
        user3 = self.user3
        users = [user1, user2, user3]

        for user in users:
            self.graph.add_user(user)

        self.graph.connect_users(user1.get_id(), user2.get_id())
        self.graph.connect_users(user1.get_id(), user3.get_id())
        self.graph.connect_users(user2.get_id(), user3.get_id())

        infection_count = infect_total(user1)
        assert infection_count == 3
        verify_users_in_a_group_are_infected(self.graph)

    def test_total_infection_on_components_with_three_users_connected_to_one_user(self):
        user1 = self.user1
        self.graph.add_user(user1)
        users = self.users

        for user in users[1:]:
            self.graph.add_user(user)
            self.graph.connect_users(user1.get_id(), user.get_id())

        infection_count = infect_total(users[1])
        assert infection_count == 4
        verify_users_in_a_group_are_infected(self.graph)


class TestLimitedInfection(unittest.TestCase):
    def test_correct_components_are_chosen_when_there_are_components_whose_user_count_sum_to_target(self):
        """
        tests that correct connected components (user graphs) are selected when
        there exists set of components whose user count sum exactly to the desired infection count
        """
        graphs = []
        sizes = [1, 2, 3]
        for size in sizes:
            graphs.append(construct_graph_of_count(size))
        target = sum(sizes)
        selected_graphs, target_diff = find_closest_subset_sum_of_graphs(
            graphs, len(graphs), target)
        assert target_diff == 0
        verify_arrays_have_same_content(selected_graphs, graphs)

    def test_correct_components_are_chosen_when_closest_infection_count_is_less_than_target(self):
        """
        tests that correct connected components (user graphs) are selected in the case where
        the closest aggregate number of users of components is less than the desired infection count.
        """
        graphs = []
        sizes = [3, 6, 12]
        target = 10
        expected_user_count = 9
        
        for size in sizes:
            graphs.append(construct_graph_of_count(size))

        expected_graphs = graphs[0:2]

        selected_graphs, target_diff = find_closest_subset_sum_of_graphs(
            graphs[:], len(graphs), target)

        assert target - target_diff == expected_user_count
        verify_arrays_have_same_content(selected_graphs, expected_graphs)

    def test_correct_components_are_chosen_when_closest_infection_count_is_greater_than_target(self):
        """
        tests that correct connected components (user graphs) are selected in the case where
        the closest aggregate number of users of components is greater than the desired infection count.
        """
        graphs = []
        sizes = [3, 6, 12]
        target = 17
        expected_user_count = 18

        for size in sizes:
            graphs.append(construct_graph_of_count(size))
        expected_graphs = graphs[1:]

        selected_graphs, target_diff = find_closest_subset_sum_of_graphs(
            graphs, len(graphs), target)
        assert target - target_diff == expected_user_count
        verify_arrays_have_same_content(selected_graphs, expected_graphs)

    def test_component_is_chosen_if_every_component_is_greater_than_target_count(self):
        num_users = 20
        graph = construct_graph_of_count(num_users)
        expected_graphs = graphs = [graph]
        target = 5
        expected_infection_count = num_users

        selected_graphs, target_diff = find_closest_subset_sum_of_graphs(
            graphs, len(graphs), target)
        assert target_diff == target - num_users
        verify_arrays_have_same_content(selected_graphs, expected_graphs)

    def test_limited_infection_when_there_exist_components_that_sum_to_target(self):
        expected_graphs = graphs = []
        sizes = [1, 2, 3]
        for size in sizes:
            graphs.append(construct_graph_of_count(size))
        target = expected_infection_count = sum(sizes)

        infection_count = infect_limited(graphs, target)
        assert infection_count == expected_infection_count

        for graph in expected_graphs:
            verify_users_in_a_group_are_infected(graph)

    def test_limited_infection_for_components_whose_closest_sum_is_less_than_target(self):
        graphs = []
        sizes = [3, 6, 12]
        target = 10
        expected_infection_count = 9

        for size in sizes:
            graphs.append(construct_graph_of_count(size))

        expected_graphs = graphs[0:2]

        infection_count = infect_limited(graphs, target)
        assert infection_count == expected_infection_count

        for graph in expected_graphs:
            verify_users_in_a_group_are_infected(graph)

    def test_limited_infection_for_components_whose_closest_sum_is_greater_than_target(self):
        graphs = []
        sizes = [3, 6, 12]
        target = 17
        expected_infection_count = 18

        for size in sizes:
            graphs.append(construct_graph_of_count(size))
        expected_graphs = graphs[1:]

        infection_count = infect_limited(graphs, target)
        assert infection_count == expected_infection_count

        for graph in expected_graphs:
            verify_users_in_a_group_are_infected(graph)

    def test_component_is_infected_if_num_users_in_every_component_is_greater_than_target(self):
        graph = construct_graph_of_count(20)
        graphs = [graph]
        target = 5
        expected_infection_count = 20

        infection_count = infect_limited(graphs, target)
        assert infection_count == expected_infection_count

        for graph in graphs:
            verify_users_in_a_group_are_infected(graph)
