from libero_flow.decider import decide


def test_can_make_start_workflow_decision(workflow_with_pending_state):
    decision = decide(workflow_with_pending_state)
    assert decision['decision'] == 'start-workflow'
    assert decision['workflow_id']


def test_can_make_do_nothing_decision_with_finished_state(workflow_with_finished_state):
    decision = decide(workflow_with_finished_state)
    assert decision['decision'] == 'do-nothing'
    assert decision['workflow_id']


def test_can_make_do_nothing_decision_with_cancelled_state(workflow_with_cancelled_state):
    decision = decide(workflow_with_cancelled_state)
    assert decision['decision'] == 'do-nothing'
    assert decision['workflow_id']


def test_can_make_schedule_activities_decision(workflow_with_in_progress_state):
    decision = decide(workflow_with_in_progress_state)
    assert decision['decision'] == 'schedule-activities'
    assert decision['workflow_id']
    assert len(decision['activities']) == 1


def test_will_fail_a_workflow_if_required_activity_perma_fails(workflow_with_perma_failed_required_activity):
    decision = decide(workflow_with_perma_failed_required_activity)
    assert decision['decision'] == 'workflow-failure'


def test_will_schedule_multiple_independent_activities(wf_with_multi_independent_acts):
    decision = decide(wf_with_multi_independent_acts)
    assert decision['decision'] == 'schedule-activities'
    assert decision['workflow_id']
    assert len(decision['activities']) == 2


# TODO will re schedule an activity with a temp failure

# TODO test_will_complete_workflow_if_all_activities_complete

