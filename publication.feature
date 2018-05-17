Feature: Publication of an article

  Scenario: Make an article version ready to publish
    Given version 1 of article 1234 is in English
    And I can publish articles
    When version 1 of article 1234 is sent to the Article Store
    Then I can see version 1 of article 1234 on the Dashboard
    And I can publish version 1 of article 1234

  Scenario: Update an article version
    Given version 1 of article 1234 is in English
    And version 1 of article 1234 is in the Article Store
    When version 1 of article 1234 is updated
    And version 1 of article 1234 is sent to the Article Store
    Then I can see the update to version 1 of article 1234 on the Dashboard

  @future
  Scenario: Preview an article version
    Given version 1 of article 1234 is in English
    And I can preview articles on Journal
    When version 1 of article 1234 is sent to the Article Store
    Then I can preview version 1 of article 1234 on Journal

  @future
  Scenario: Publish an article version
    Given version 1 of article 1234 is in English
    And version 1 of article 1234 is in the Article Store
    When I publish version 1 of article 1234
    Then I can see that version 1 of article 1234 has been published on the Dashboard
    And I can read version 1 of article 1234 on Journal

  @future
  Scenario: Publish multiple versions of an article
    Given version 1 of article 1234 is in English
    And version 1 of article 1234 has been published
    And version 2 of article 1234 is in English
    And version 2 of article 1234 is in the Article Store
    When I publish version 2 of article 1234
    Then I can see version 2 of article 1234 has been published on the Dashboard
    And I can read version 2 of article 1234 on Journal

  @future
  Scenario: Publish an article version in multiple languages
    Given version 1 of article 1234 is in English and Portuguese
    And version 1 of article 1234 is in the Article Store
    When I publish version 1 of article 1234
    Then I can read version 1 of article 1234 in English on Journal
    And I can read version 1 of article 1234 in Portuguese on Journal
