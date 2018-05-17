Feature: Publication of an article

  Scenario: Ingest an article
    Given a new article X
    When I ingest article X
    Then I should see article X on the dashboard in ready-to-publish state

  Scenario: Publish an article
    Given an ingested article X
    #When I publish article X from the dashboard
    When I publish article X
    Then I should see article X on the dashboard in published state
    And I should see article X on journal

  @future
  Scenario: Preview an article
    Given a new article X
    When I ingest article X
    Then I should see a preview of article X on journal

  @future
  Scenario: Multiple versions
    Given a published article X
    When I ingest and publish version 2 of article X from the dashboard
    Then I should see version 2 of article X on the dashboard in published state
    And I should see version 2 of article X on journal

  @future
  Scenario: Multilingual articles
    Given an ingested article X in languages en and pr
    When I ingest and publish article X
    Then I should see article X on journal
    And I should see the article X in pr on journal

  @future
  Scenario: Figures
    Given an article X with 2 figures
    When I ingest and publish article X
    Then I should see article X on the dashboard in published state
    And I should see article X on journal
