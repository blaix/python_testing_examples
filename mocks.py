import unittest
from flexmock import flexmock

#
# Super convoluted example that we want to test:
#

class UserService:
    def upgrade_user_by_id(user_id):
        user = self.get_user_by_id(user_id)
        if user.admin:
            user.super_admin = true
        else:
            user.admin = true

#
# Traditional tests:
#

class TestUpgradeUser(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        # Load some fixtures or something for a regular user and an admin user
        pass
        
    def test_upgrades_from_normal_to_admin(self):
        self.user_service.upgrade_user_by_id(123)
        
        # Takes multiple steps to verify:
        user = self.user_service.get_user_by_id(123)
        self.assertTrue(user.admin)
        self.assertFalse(user.super_admin)

    def test_upgrades_from_admin_to_super_admin(self):
        self.user_service.upgrade_user_by_id(321)
        
        # Takes multiple steps to verify:
        user = self.user_service.get_user_by_id(321)
        self.assertTrue(user.admin)
        self.assertTrue(user.super_admin)

#
# Mock-based test.
#

class TestUpgradeUserMock(unittest.TestCase):
    """
    When using mocks, we are asserting the communication between our objects,
    as opposed to testing based on the state of our objects. This emphasizes
    the "Tell Don't Ask" principle: http://c2.com/cgi/wiki?TellDontAsk

    Testing this way is a poor fit for the implentation we've written above,
    since it had intimate knowledge of the inner state of our User object, and
    made decisions based on that. This is something we want to avoid. Because
    of this, mock-based testing is a great fit for test-first development -
    since you'll want to keep your mocks simple and straightforward, resulting
    in the interaction between your objects being simple and straightforward -
    and a bad fit for coming in and adding tests after the fact - where you'll
    be trying to backport whatever convoluted logic you came up with to mocks.
    
    So I'm going to write the test first for a refactored implementation of
    that method here.
    """
    
    def test_upgrade_user(self):
        user = flexmock()
        user.should_receive('upgrade')
        upgrade_user_refactored(user) # If we call this method, and it doesn't
                                      # call user.upgrade(), our test will fail

# The new implementation:
def upgrade_user_refactored(user):
    user.upgrade()

# I didn't go as far as making this something you could actually run, sorry!
# if __name__ == '__main__':
#     unittest.main()
