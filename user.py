class User:
    """
    Dummy class for sake of example, to make the stubs.py actually run.
    """

    def __init__(self, user_id):
        self.user_id = user_id
        
    def get_subscriptions(self):
        if self.user_id == 123:
            return ['silver']
        else:
            return ['bronze']
