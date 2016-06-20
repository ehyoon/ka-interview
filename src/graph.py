class Graph:
    def __init__(self):
        self.users = {}
        self.num_users = 0

    def get_users(self):
        return self.users.values()

    def add_user(self, user):
        user_id = user.get_id()
        self.users[user_id] = user
        self.num_users += 1

    def connect_users(self, user1_id, user2_id):
        users = self.users

        if user1_id not in users or user2_id not in users:
            raise Exception("User(s) do not exist in this connected component!")

        user1 = users[user1_id]
        user2 = users[user2_id]
        user1.add_connection(user2)
        user2.add_connection(user1)

