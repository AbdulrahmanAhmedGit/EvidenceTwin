"""Independently executable worker; no production task/provider enabled by default."""
import argparse
import time
from uuid import uuid4
from .contracts import Rejected, Contention, CommitUnknown
from .recovery import Recovery
from .supervisor import Supervisor

class Worker:
    def __init__(self,repository,principal,task=None,supervisor=None):
        self.repository=repository;self.principal=principal;self.task=task
        self.supervisor=supervisor or Supervisor(repository.settings)
        if task is not None and repository.adapters.stop is not self.supervisor:
            raise Rejected('execution_stop_adapter_mismatch')
    def run(self,stop_event):
        """Bounded polling for explicitly configured, trusted adapters only."""
        if self.task is None:raise Rejected('execution_adapter_unavailable')
        from .contracts import CapacityUnavailable
        while not stop_event.is_set():
            try:self.once()
            except (CapacityUnavailable,Contention):pass
            stop_event.wait(self.repository.settings.polling_seconds)

    def once(self):
        if self.task is None:raise Rejected('execution_adapter_unavailable')
        r=self.repository;p=self.principal
        instance=uuid4();lease=r.claim(p,instance)
        if lease is None:return False
        handle=self.supervisor.start(instance,self.task)
        heartbeat_at=time.monotonic()+r.settings.heartbeat_seconds
        message=None;lost=False;uncertain=False;misses=0;heartbeat_key=None
        try:
            while True:
                if message is None and handle.connection.poll(.05):
                    try:message=handle.connection.recv()
                    except EOFError:message=('failed',None)
                if message is None and not handle.process.is_alive():message=('failed',None)
                if message is not None and not uncertain:break
                if time.monotonic()>=heartbeat_at:
                    if heartbeat_key is None:heartbeat_key=uuid4().hex
                    try:
                        renewed=r.heartbeat(p,lease,heartbeat_key)
                        lease=r.current_lease(p,renewed) if uncertain else renewed
                        heartbeat_key=None;misses=0;uncertain=False
                    except (Contention,CommitUnknown):
                        uncertain=True;misses+=1
                        if misses>=r.settings.missed_heartbeats:lost=True;break
                    except Rejected:
                        lost=True;break
                    heartbeat_at=time.monotonic()+r.settings.heartbeat_seconds
                if message is not None and uncertain:time.sleep(.01)
            proof=self.supervisor.stop(handle)
            if lost:return False  # Recovery controller must inspect durable state.
            if message and message[0]=='completed':
                r.publish(p,lease,uuid4().hex,message[1],stop_proof=proof)
            else:
                Recovery(r).retire(p,lease.job_id,uuid4().hex,expected_version=lease.job_version,lease=lease,proof=proof)
            return True
        finally:
            if handle.process.is_alive():self.supervisor.stop(handle)


def main():
    parser=argparse.ArgumentParser(description='EvidenceTwin isolated execution worker')
    parser.add_argument('--check',action='store_true',help='Report configured execution readiness')
    parser.parse_args()
    # No arbitrary --task import, fake authorizer, or legacy provider fallback.
    parser.exit(2,'Execution unavailable: configure reviewed authorization, validation and task adapters. No jobs claimed.\n')

if __name__=='__main__':main()
