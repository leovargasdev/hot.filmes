# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s hot.filmes -t test_bla.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src hot.filmes.testing.HOT_FILMES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_bla.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a bla
  Given a logged-in site administrator
    and an add bla form
   When I type 'My bla' into the title field
    and I submit the form
   Then a bla with the title 'My bla' has been created

Scenario: As a site administrator I can view a bla
  Given a logged-in site administrator
    and a bla 'My bla'
   When I go to the bla view
   Then I can see the bla title 'My bla'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add bla form
  Go To  ${PLONE_URL}/++add++bla

a bla 'My bla'
  Create content  type=bla  id=my-bla  title=My bla


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the bla view
  Go To  ${PLONE_URL}/my-bla
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a bla with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the bla title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
