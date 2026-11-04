"""Pure-stdlib, single-owner reservation ledger for D1A v2 work.

Reservations are irrevocable and made before each guard request. One ticket
may be in flight; roles and slots cannot be replayed or reassigned. Missing
actual counters stay unknown. Stop/failure preserves reserved upper bounds.
This module performs no scientific work, persistence, or process control.
"""
from dataclasses import dataclass
from typing import Optional
from threading import get_ident

@dataclass(frozen=True)
class Slot:
    context: int
    index: int
    seed: int

@dataclass(frozen=True)
class Ticket:
    sequence: int
    slot: Slot
    role: str
    logical_rows: int
    callbacks: int
    reference_nodes: int
    reference_cells: int
    saved_solves: int

class BudgetError(RuntimeError):
    """Fail-closed admission or ledger-state error."""

ROLES = (("generation",128,1,0,0,0), ("q4",4,1,0,0,0),
         ("qj4",64,1,0,0,0), ("qj16",1024,1,0,0,0),
         ("reference",0,0,1092,1088,1))
CAPS = {"logical_rows":19520,"callbacks":64,"fits":16,"context_fits":8,
        "reference_nodes":17472,"reference_cells":17408,"saved_solves":16,
        "max_batch":1024}

class BudgetLedger:
    """Controller-thread ledger; caller supplies frozen registry slots."""
    def __init__(self, slots: tuple[Slot, ...]):
        coords={(s.context,s.index) for s in slots}
        seeds=(3258714074,614436862,2983410662,2461864690,214314417,2692160139,1391606087,3129792625,4154278181,3104292383,2097005719,2218801880,2967568667,2649780005,3244027303,1433599097)
        expected=tuple((c,i) for i in range(8) for c in (0,1))
        if len(slots)!=16 or tuple((s.context,s.index) for s in slots)!=expected or tuple(s.seed for s in slots)!=seeds:
            raise ValueError("slots must match the exact frozen registry order and seeds")
        self._slots=tuple(slots); self._owner=get_ident()
        self._si=0; self._ri=0; self._seq=0; self._flight=None
        self._stopped=False; self._reason=None
        self._totals={k:0 for k in ("logical_rows","callbacks","reference_nodes","reference_cells","saved_solves","fits")}
        self._context_fits=[0,0]
        self._records=[{"slot":s,"status":"planned","attempted":[],"completed":[],"partial":[],"skipped":[],"actual_rows":None,"actual_callbacks":None,
                         "known_rows_lower_bound":0,"known_callbacks_lower_bound":0,
                         "unknown_rows":False,"unknown_callbacks":False,
                         "role_details":[]} for s in slots]

    def _check(self):
        if get_ident()!=self._owner: raise BudgetError("wrong ledger owner thread")

    def _stop(self, reason):
        if self._stopped:
            return
        self._stopped=True; self._reason=reason
        if self._flight is not None:
            r=self._records[self._si]
            role=self._flight.role
            if role not in r["partial"]:
                r["partial"].append(role)
            for detail in reversed(r["role_details"]):
                if detail["role"]==role and detail["state"]=="inflight":
                    detail["state"]="partial"
                    break
            r["status"]="partial"
            r["actual_rows"]=r["actual_callbacks"]=None
            r["unknown_rows"]=r["unknown_callbacks"]=True
        self._flight=None
        for n in range(self._si,len(self._records)):
            r=self._records[n]
            if r["status"]=="planned":
                r["status"]="skipped"; r["skipped"]=[x[0] for x in ROLES]
            elif n==self._si:
                r["skipped"].extend(x[0] for x in ROLES[self._ri:]
                                    if x[0] not in r["partial"])

    def reserve(self, context:int, index:int, role:str)->Ticket:
        self._check()
        if self._stopped:
            raise BudgetError("ledger stopped")
        if self._flight is not None:
            self._stop("reservation_while_inflight")
            raise BudgetError("reservation already in flight")
        if (type(context) is not int or type(index) is not int or
                not isinstance(role,str)):
            self._stop("invalid_reservation_arguments")
            raise BudgetError("invalid reservation arguments")
        if self._si>=16:
            self._stop("all_slots_consumed")
            raise BudgetError("all planned slots consumed")
        s=self._slots[self._si]
        if (context,index)!=(s.context,s.index):
            self._stop("out_of_order_slot")
            raise BudgetError("out-of-order slot")
        if self._ri>=len(ROLES) or role!=ROLES[self._ri][0]:
            self._stop("duplicate_or_out_of_order_role")
            raise BudgetError("duplicate or out-of-order role")
        name,rows,calls,nodes,cells,solves=ROLES[self._ri]
        additions=dict(zip(("logical_rows","callbacks","reference_nodes","reference_cells","saved_solves"),(rows,calls,nodes,cells,solves)))
        for k,v in additions.items():
            if self._totals[k]+v>CAPS[k]:
                self._stop("quota_exceeded"); raise BudgetError("fixed quota exceeded")
        if rows>CAPS["max_batch"]:
            self._stop("batch_exceeded"); raise BudgetError("batch cap exceeded")
        if name=="generation" and (self._totals["fits"]>=16 or self._context_fits[context]>=8):
            self._stop("fit_cap_exceeded"); raise BudgetError("fit cap exceeded")
        self._totals.update({k:self._totals[k]+v for k,v in additions.items()})
        if name=="generation":
            self._totals["fits"]+=1; self._context_fits[context]+=1
        r=self._records[self._si]
        r["status"]="attempted"; r["attempted"].append(name)
        r["actual_rows"]=r["actual_callbacks"]=None
        t=Ticket(self._seq,s,name,rows,calls,nodes,cells,solves)
        r["role_details"].append({"role":name,"reserved_rows":rows,
            "reserved_callbacks":calls,"reserved_reference_nodes":nodes,
            "reserved_reference_cells":cells,"reserved_saved_solves":solves,
            "actual_rows":None,"actual_callbacks":None,"success":None,"state":"inflight"})
        self._seq+=1; self._flight=t; return t

    def complete(self, sequence:int, *, actual_rows:Optional[int], actual_callbacks:Optional[int], success:bool)->None:
        self._check(); t=self._flight
        if t is None or type(sequence) is not int or t.sequence!=sequence:
            self._stop("invalid_completion_sequence")
            raise BudgetError("completion does not match ticket")
        if type(success) is not bool:
            self._stop("invalid_success_type")
            raise BudgetError("success must be bool")
        valid_types=((actual_rows is None or type(actual_rows) is int) and
                     (actual_callbacks is None or type(actual_callbacks) is int))
        valid_bounds=(valid_types and
                      (actual_rows is None or 0<=actual_rows<=t.logical_rows) and
                      (actual_callbacks is None or 0<=actual_callbacks<=t.callbacks))
        r=self._records[self._si]
        detail=r["role_details"][-1]
        if not valid_bounds:
            detail["state"]="partial"; detail["success"]=False
            if t.role not in r["partial"]: r["partial"].append(t.role)
            r["status"]="partial"
            self._stop("invalid_actual_counters")
            raise BudgetError("actual counters must be non-bool ints within reservation or None")
        detail["actual_rows"]=actual_rows
        detail["actual_callbacks"]=actual_callbacks
        detail["success"]=success
        if actual_rows is None:
            r["unknown_rows"]=True
        else:
            r["known_rows_lower_bound"]+=actual_rows
        r["actual_rows"]=None if r["unknown_rows"] else r["known_rows_lower_bound"]
        if actual_callbacks is None:
            r["unknown_callbacks"]=True
        else:
            r["known_callbacks_lower_bound"]+=actual_callbacks
        r["actual_callbacks"]=None if r["unknown_callbacks"] else r["known_callbacks_lower_bound"]
        known=actual_rows is not None and actual_callbacks is not None
        if not success or not known:
            detail["state"]="partial"
            if t.role not in r["partial"]: r["partial"].append(t.role)
            r["status"]="partial"
        else:
            detail["state"]="completed"; r["completed"].append(t.role)
        self._flight=None
        if not success:
            self._stop("unit_failed"); return
        if not known:
            self._stop("actual_counter_unknown"); return
        self._ri+=1
        if self._ri==len(ROLES):
            r["status"]="completed"; self._si+=1; self._ri=0

    def abort_inflight(self, reason:str)->None:
        self._check()
        if not isinstance(reason,str) or not reason: raise ValueError("reason must be non-empty")
        self._stop(reason)

    def snapshot(self)->dict:
        self._check()
        return {"stopped":self._stopped,"stop_reason":self._reason,
                "inflight":self._flight,"totals_reserved":dict(self._totals),
                "slots":tuple({**r,"attempted":tuple(r["attempted"]),
                    "completed":tuple(r["completed"]),"partial":tuple(r["partial"]),
                    "skipped":tuple(r["skipped"]),
                    "role_details":tuple(dict(d) for d in r["role_details"])} for r in self._records)}


def snapshot_digest(value):
    """Canonical controller/worker agreement without large IPC payloads."""
    import hashlib
    import json
    from dataclasses import asdict, is_dataclass
    def encode(item):
        if is_dataclass(item):
            return asdict(item)
        raise TypeError('Unexpected ledger value')
    raw = json.dumps(value, default=encode, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()
