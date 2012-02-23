import unittest
from flexmock import flexmock

#
# Super convoluted example that we want to test:
#

def upgrade_user(user, log=Logger()):
    if user.admin:
        user.super_admin = True
    else:
        user.admin = True
    log.add("Upgraded user: " + user.id)

#
# Traditional tests:
#

class TestUpgradeUser(unittest.TestCase):
    def setUp(self):
        # Load some fixtures or something for a regular user and an admin user
        pass
        
    def test_upgrades_from_normal_to_admin(self):
        # Some user we loaded in a fixture that is not an admin:
        user = User(123)
        upgrade_user(user)
        self.assertTrue(user.admin)
        self.assertFalse(user.super_admin)

    def test_upgrades_from_admin_to_super_admin(self):
        # Some user we loaded in a fixture that is an admin:
        user = User(321)
        upgrade_user(user)
        self.assertTrue(user.admin)
        self.assertTrue(user.super_admin)
    
    def test_adds_log_message(self):
        # Some crazy-ass test here, read the test log maybe? Gross.
        #...
        pass

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
        user = flexmock(id=123)
        log = flexmock()
        
        user.should_receive('upgrade')
        log.should_receive('add').with("Upgraded user: 123")
        
        # If either of the above methods are not called, or called with the
        # wrong parameters in the case of the log message, then our test
        # will fail.
        
        # This is also a trivial example of dependency injection (we can pass
        # in our own logger, a test double in this case):
        upgrade_user_refactored(user, log)

# The new implementation. Much more straightforward.
def upgrade_user_refactored(user_id, log=Logger()):
    user.upgrade()
    log.add("Upgraded user: " + user.id)

# I didn't go as far as making this something you could actually run, sorry!
# if __name__ == '__main__':
#     unittest.main()
