Feature: post comment to package version
  As a Player
  I want to post comment to package version
  So that I can suggest some idea for the game

  Scenario: post comment require sign in before
    Given package name "call me MT" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 1            | 2013-10-10 23:21:00 |

    When I post comment "great job" to the package
    Then I should receive 401 Unauthorized

  Scenario: Empty Comment
    Given package name "call me MT" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 1            | 2013-10-10 23:21:00 |

    When I access the package detail
    Then I should receive 200 OK
     And I should see comment_count 0 in the package version detail

    When I access comment list of the package
    Then I should receive 200 OK

  Scenario: Post Comment and set status published/unpublished

    Given I sign in as player name "fox20century" exists in game center
    Given package name "call me MT" has a set of versions below:
      | version_name | version_code | released_datetime   |
      | 1.0          | 1            | 2013-10-10 23:21:00 |

    When I post comment "great job" to the package
    Then I should receive 201 Created
     And I should receive comment "great job" from response

    # new comment is_public = False
    When I access the package detail
    Then I should receive 200 OK
     And I should see comment_count 0 in the package version detail

    # set comment is_public = True
    Given the comment of package name "call me MT" version_code "1" change to published
     When I access the package detail
     Then I should receive 200 OK
      And I should see comment_count 1 in the package version detail

     When I access comment list of the package
     Then I should receive 200 OK
      And I should see comment list of the package version in comment page

     When I visit my profile using my authorization token
     Then I should receive 200 OK
      And I should see the player profile with comment_count value 1

     When I visit my commented package page
     Then I should receive 200 OK
      And I should see the package commented by me in result list

    # set comment is_public = False
    Given the comment of package name "call me MT" version_code "1" change to unpublished
     When I access the package detail
     Then I should receive 200 OK
      And I should see comment_count 0 in the package version detail
