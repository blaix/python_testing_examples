import unittest
from user import User # my dummy class for sake of example
from flexmock import flexmock

#
# Super convoluted example method that we want to test:
#

def user_has_silver(user):
    return 'silver' in user.get_subscriptions()

#
# Traditional tests:
#

class TestUserHasSilver(unittest.TestCase):
    def setUp(self):
        # Maybe load some fixtures for users with and without silver...
        pass
        
    def test_returns_true_if_subscriptions_include_silver(self):
        # Grab user from one of the fixtures we loaded in our imaginary setup:
        user = User(123)
        self.assertTrue(user_has_silver(user))

    def test_returns_false_if_subscriptions_do_not_include_silver(self):
        # Grab user from one of the fixtures we loaded in our imaginary setup:
        user = User(321)
        self.assertFalse(user_has_silver(user))

#
# Isolated tests. Stubbing with flexmock:
#

class TestUserHasSilverWithStubs(unittest.TestCase):
    """
    We are only testing the user_has_silver method, we don't care that
    it is passed an actual user object, and we assume that the user's
    subscriptions method is working (and has it's own tests).
    So we create a "test double" to stand in for a user, and stub the
    subscriptions method, setting the state for each test.
    
    This isolates our tests. For example, if the subscriptions method on user
    breaks for some reason, it should only break the tests for the
    subscriptions method, not our tests for the user_has_silver here.
    
    This also has the benefit of freeing us from worrying about any
    underlying implementation. Subscriptions could be coming from a
    database, a third-party service, etc. We don't care in these
    tests. We only care that given a set of subscriptions on a user,
    our user_has_silver method returns the expected results.
    """
    
    def test_returns_true_if_subscriptions_include_silver(self):
        user = flexmock(get_subscriptions=lambda: ['silver'])
        self.assertTrue(user_has_silver(user))
    
    def test_returns_false_if_subscriptions_do_not_include_silver(self):
        user = flexmock(get_subscriptions=lambda: ['bronze'])
        self.assertFalse(user_has_silver(user))

if __name__ == '__main__':
    unittest.main()
