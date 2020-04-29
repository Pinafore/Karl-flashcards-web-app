import requests

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas, evaluate
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Fact])
def get_next_set(
    db: Session = Depends(deps.get_db),
    user_id: int = None,
    deck_ids: List[int] = None,
    limit: int = 20,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get next set of facts for review using user's schedule.
    Allows superusers to view anyone's future schedule.
    """
    if user_id:
        user = crud.user.get(db=db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not (crud.user.is_superuser(current_user) or user_id == current_user.id):
            raise HTTPException(status_code=400, detail="This user does not have the necessary permissions")
    else:
        user = current_user

    if deck_ids is None:
        facts = crud.fact.get_study_set(db=db, user=user, limit=limit)
    else:
        for deck_id in deck_ids:
            deck = crud.deck.get(db=db, id=deck_id)
            if not deck:
                raise HTTPException(status_code=404, detail="One or more of the specified decks does not exist")

        facts = crud.fact.get_study_set(db=db, user=user, deck_ids=deck_ids, limit=limit)
    return facts

@router.put("/", response_model=List[bool], summary="Update Fact Set with the correct schedule")
def update_schedule_set(
    *,
    db: Session = Depends(deps.get_db),
    facts_in: List[schemas.Schedule] = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
        Updates the schedules of the returned fact set using the current user's assigned schedule
    """

    successes = []
    for fact_in in facts_in:
        fact = crud.fact.get(db=db, id=fact_in.fact_id)
        if not fact:
            raise HTTPException(status_code=404, detail="Fact not found")
        success = crud.fact.update_schedule(db=db, user=current_user, db_obj=fact, schedule=fact_in)
        successes.append(success)
    return successes


@router.get("/evaluate", response_model=Optional[bool], summary="Evaluates accuracy of typed answer to the given fact")
def evaluate_answer(
    *,
    db: Session = Depends(deps.get_db),
    fact_id: int,
    typed: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    fact = crud.fact.get(db=db, id=fact_id)
    if not fact:
        raise HTTPException(status_code=404, detail="Fact not found")

    if typed is None:
        return False
    else:
        return evaluate.evaluate_answer(eval_fact=fact, typed=typed)


@router.get("/status", response_model=bool, summary="Checks status of connection to scheduler")
def scheduler_status() -> Any:
    try:
        r = requests.post("http://host.docker.internal:4000/api/karl/status", json=[])
        r.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xxx
        return True
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
        raise HTTPException(status_code=555, detail="Connection to scheduler is down")