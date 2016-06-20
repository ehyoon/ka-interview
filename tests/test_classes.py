import os, sys
sys.path.insert(0, os.path.abspath(".."))

import unittest
from src.graph import Graph
from src.user import User, INITIAL_SITE_VERSION
from src.infection import INFECTED_SITE_VERSION
from util import verify_arrays_have_same_content

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User()

    def test_initial_user_creation(self):
        expected_default = {
            'site_version': INITIAL_SITE_VERSION,
            'connections': []
        }
        for key, value in expected_default.viewitems():
            assert getattr(self.user, key, None) == value

    def test_user_id_generation(self):
        user1 = User()
        user2 = User()
        assert user2.get_id() == user1.get_id() + 1

    def test_update_site_version_on_user(self):
        self.user.update_site_version(INFECTED_SITE_VERSION)
        assert self.user.site_version == INFECTED_SITE_VERSION

    def test_add_user_connection(self):
        another_user = User()
        self.user.add_connection(another_user)
        assert another_user in self.user.connections


class TestGraph(unittest.TestCase):
    def test_initial_graph_creation(self):
        expected_default = {
            'users': {},
            'num_users': 0
        }
        graph = Graph()
        for key, value in expected_default.viewitems():
            assert getattr(graph, key, None) == value

    def test_add_users_to_a_graph(self):
        graph = Graph()
        user = User()
        user_id = user.get_id()
        graph.add_user(user)

        assert user_id in graph.users and graph.users[user_id] == user

    def test_connect_users_in_a_graph(self):
        graph = Graph()
        user1 = User()
        user2 = User()
        graph.add_user(user1)
        graph.add_user(user2)

        graph.connect_users(user1.get_id(), user2.get_id())
        assert user2 in user1.get_connections() and user1 in user2.get_connections()
