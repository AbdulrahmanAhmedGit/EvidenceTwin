"""Shared, transactional reservations. Terminal job state never releases permits."""
from uuid import uuid4
from sqlalchemy import select, update, insert, func
from . import tables as t
from .contracts import CapacityUnavailable, Rejected

def lock_scopes(conn, keys):
    rows={r['key']:dict(r) for r in conn.execute(select(t.capacity_scopes).where(
        t.capacity_scopes.c.key.in_(sorted(set(keys)))).order_by(t.capacity_scopes.c.key).with_for_update()).mappings()}
    if set(rows)!=set(keys): raise CapacityUnavailable('capacity_unconfigured')
    return rows

def reserve(conn, scopes, job, attempt, logical_key, external=None):
    rows=lock_scopes(conn,scopes)
    for key in sorted(rows):
        r=rows[key]
        existing=conn.execute(select(t.reservations.c.id).where(t.reservations.c.scope_key==key,
            t.reservations.c.logical_key==logical_key,t.reservations.c.released_at.is_(None))).scalar_one_or_none()
        if existing: raise Rejected('duplicate_reservation')
        changed=conn.execute(update(t.capacity_scopes).where(t.capacity_scopes.c.key==key,
            t.capacity_scopes.c.version==r['version'],t.capacity_scopes.c.in_use<t.capacity_scopes.c.capacity)
            .values(in_use=t.capacity_scopes.c.in_use+1,version=t.capacity_scopes.c.version+1)).rowcount
        if changed!=1: raise CapacityUnavailable('capacity_full')
        conn.execute(insert(t.reservations).values(id=uuid4(),scope_key=key,job_id=job,attempt_id=attempt,
            external_operation_id=external,logical_key=logical_key,reserved_at=func.clock_timestamp()))

def release(conn, job, attempt, proof, *, external=None, analyses_only=False):
    if not proof: raise Rejected('release_proof_required')
    conditions=[t.reservations.c.job_id==job,t.reservations.c.attempt_id==attempt,t.reservations.c.released_at.is_(None)]
    if external is not None: conditions.append(t.reservations.c.external_operation_id==external)
    if analyses_only: conditions.append(t.reservations.c.external_operation_id.is_(None))
    rows=list(conn.execute(select(t.reservations).where(*conditions)).mappings())
    if not rows:return
    lock_scopes(conn,[r['scope_key'] for r in rows])
    for r in rows:
        n=conn.execute(update(t.reservations).where(t.reservations.c.id==r['id'],t.reservations.c.released_at.is_(None))
            .values(released_at=func.clock_timestamp(),release_proof_ref=proof)).rowcount
        if n:
            n=conn.execute(update(t.capacity_scopes).where(t.capacity_scopes.c.key==r['scope_key'],t.capacity_scopes.c.in_use>0)
                .values(in_use=t.capacity_scopes.c.in_use-1,version=t.capacity_scopes.c.version+1)).rowcount
            if n!=1:raise Rejected('reservation_counter_corrupt')
