"""Same-host subprocess supervision. Remote lease loss is never process-exit proof."""
from dataclasses import dataclass
import multiprocessing as mp
import os
import signal
from uuid import uuid4
from .contracts import StopProof, Rejected

def _child(connection, target, arguments):
    # A separate process group lets the owning supervisor terminate descendants.
    os.setsid()
    try:
        result=target(*arguments)
        connection.send(('completed',result))
    except BaseException:
        connection.send(('failed',None))
    finally: connection.close()

@dataclass
class Handle:
    instance: object
    process: object
    connection: object

class Supervisor:
    def __init__(self,settings):
        self.settings=settings; self.context=mp.get_context('spawn'); self.proofs={}
    def start(self,instance,target,*arguments):
        parent,child=self.context.Pipe(duplex=False)
        process=self.context.Process(target=_child,args=(child,target,arguments),daemon=False)
        process.start();child.close()
        return Handle(instance,process,parent)
    def stop(self,handle):
        p=handle.process
        p.join(self.settings.stop_grace)
        if p.is_alive():
            try:os.killpg(p.pid,signal.SIGTERM)
            except ProcessLookupError:pass
            # Child may not have reached setsid; target the known multiprocessing child too.
            if p.is_alive():p.terminate()
            p.join(self.settings.kill_grace)
        if p.is_alive():
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            if p.is_alive():p.kill()
            p.join(self.settings.kill_grace)
        if p.is_alive():raise Rejected('process_exit_unknown')
        # Only trusted single-process task adapters are admitted in this increment.
        # Reaping this direct child does not claim remote/external-call settlement.
        proof=StopProof(handle.instance,'local-exit:'+uuid4().hex)
        self.proofs[proof.evidence_ref]=handle.instance
        handle.connection.close()
        return proof
    def stopped(self,proof,attempt):
        return self.proofs.get(proof.evidence_ref)==attempt['owner_instance']==proof.instance
