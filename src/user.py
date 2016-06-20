INITIAL_SITE_VERSION = 'A'

class User:
    current_id = 1

    def __init__(self):
        self.id = self.__assign_id()
        self.site_version = INITIAL_SITE_VERSION
        self.connections = []

    def __assign_id(self):
        id = User.current_id
        User.current_id += 1
        return id

    def get_id(self):
        return self.id

    def update_site_version(self, version):
        self.site_version = version

    def add_connection(self, another_user):
        self.connections.append(another_user)

    def get_connections(self):
        return self.connections

