from unittest.mock import patch

from libero_flow.decider import decide


@patch('libero_flow.decider.send_workflow_event')
def test_can_make_start_workflow_decision(mock_send_event, workflow_with_pending_state):
    decision = decide(workflow_with_pending_state)
    assert decision['decision'] == 'start-workflow'
    assert decision['workflow_id']


@patch('libero_flow.decider.send_workflow_event')
def test_can_make_do_nothing_decision_with_finished_state(mock_send_event, workflow_with_finished_state):
    decision = decide(workflow_with_finished_state)
    assert decision['decision'] == 'do-nothing'
    assert decision['workflow_id']


@patch('libero_flow.decider.send_workflow_event')
def test_can_make_do_nothing_decision_with_cancelled_state(mock_send_event, workflow_with_cancelled_state):
    decision = decide(workflow_with_cancelled_state)
    assert decision['decision'] == 'do-nothing'
    assert decision['workflow_id']


@patch('libero_flow.decider.send_workflow_event')
def test_can_make_schedule_activities_decision(mock_send_event, workflow_with_in_progress_state):
    decision = decide(workflow_with_in_progress_state)
    assert decision['decision'] == 'schedule-activities'
    assert decision['workflow_id']
    assert len(decision['activities']) == 1


@patch('libero_flow.decider.send_workflow_event')
def test_will_fail_a_workflow_if_required_activity_perma_fails(mock_send_event,
                                                               workflow_with_perma_failed_required_activity):
    decision = decide(workflow_with_perma_failed_required_activity)
    assert decision['decision'] == 'workflow-failure'


@patch('libero_flow.decider.send_workflow_event')
def test_will_schedule_multiple_independent_activities(mock_send_event, wf_with_multi_independent_acts):
    decision = decide(wf_with_multi_independent_acts)
    assert decision['decision'] == 'schedule-activities'
    assert decision['workflow_id']
    assert len(decision['activities']) == 2


@patch('libero_flow.decider.send_workflow_event')
def test_will_reschedule_a_temp_failed_activity(mock_send_event, workflow_with_temp_failed_activity):
    decision = decide(workflow_with_temp_failed_activity)
    assert decision['decision'] == 'schedule-activities'
    assert decision['workflow_id']
    assert len(decision['activities']) == 1


@patch('libero_flow.decider.send_workflow_event')
def test_will_complete_workflow_if_all_activities_complete(mock_send_event, wf_with_all_activities_complete):
    decision = decide(wf_with_all_activities_complete)
    assert decision['decision'] == 'workflow-finished'

