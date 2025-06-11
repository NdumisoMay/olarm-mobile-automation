Feature: Login functionality

  @OL-1001
  Scenario: Click first login and check fields
    Given the user is on the landing screen
    When the user clicks the login button
    Then the username and password fields should be visible

  @OL-1002
  Scenario: Invalid login attempt
    Given the user is on the login screen
    When the user enters invalid credentials
    Then an error message should be displayed

  @OL-1003
  Scenario: Valid login attempt
    Given the user is on the login screen
    When the user enters valid credentials
    Then the user should be logged in successfully

  @OL-1004
  Scenario: User logout
    Given the user is logged in
    When the user performs logout from My Devices
    Then the user should be returned to the login screen

#  @OL-1005
#  Scenario: Reset application
#    Given the app is installed
#    When the app is reset
#    Then the app should be uninstalled successfully
