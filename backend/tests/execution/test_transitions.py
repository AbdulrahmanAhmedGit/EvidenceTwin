import pytest
from evidencetwin_backend.execution.transitions import EDGES,allowed,validate_pair
from evidencetwin_backend.execution.contracts import Rejected,JobState,AttemptState

@pytest.mark.parametrize('event',list(EDGES))
def test_ex08_09_every_approved_event(event):
    src,dst,actor,ast,adt=EDGES[event];allowed(event,src,dst,actor,ast,adt)
    with pytest.raises(Rejected):allowed(event,src,dst,'unauthorized',ast,adt)

@pytest.mark.parametrize('src',list(JobState))
@pytest.mark.parametrize('dst',list(JobState))
def test_ex08_forbidden_job_pairs(src,dst):
    matching=[(k,v) for k,v in EDGES.items() if v[:2]==(src,dst)]
    if matching:
        for k,v in matching:allowed(k,*v)
    else:
        with pytest.raises(Rejected):allowed('unlisted',src,dst,'worker')

def test_ex09_pair_rejects_empty_attempts():
    with pytest.raises(Rejected):validate_pair({'current_attempt_id':1,'id':2},[],{})
