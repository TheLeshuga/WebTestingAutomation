@listofcontrollers
Feature: List of controllers

  Background:
    Given I am on the login page
    And I sign in with valid credentials
    And I click the list of controllers section
  @alerts
  Scenario: User filters a list of controllers by active alerts
    When I click the "View with alerts" option
    Then the page shows a controllers list that have alerts, if any
  @todos
  Scenario: User gets a list of all controllers (no filters applied)
    Then the page shows a list of controllers, if any