import logging
from mysql.connector import IntegrityError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from database.member_db import MemberDB


class Member(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(max_length=255)

class MemberUP(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    email: str | None = Field(max_length=255, default=None)
        

router = APIRouter()


router.post("")
def add_member(data: Member):
    logging.info("A request to create a new member has been received.")
    try:
        new_id = MemberDB.create_membear(data.model_dump())
        logging.info(f"Request to create a new member completed successfully, id: {new_id}")
        return {"msg": f"member new id: {new_id} created"}
    
    except IntegrityError as e:
        logging.exception(e)

        if e.errno == 1062:
            raise HTTPException(status_code=409, detail=f"email alrady exist")
        
        raise HTTPException(status_code=400, detail=f"bad requests")
    

@router.get("")
def get_all_members():
    logging.info("A request to get all members has been received.")
    members = MemberDB.get_all_members()

    logging.info("Request to accept all members completed successfully.")
    return members

@router.get("/{id}")
def get_member_by_id(id: int):
    logging.info("A request to get member by id has been received.")

    found = MemberDB.get_members_by_id(id)

    if found is None:
        logging.error(f"member id {id} not found")
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    logging.info("Request to accept member by id completed successfully.")
    return found

@router.patch("/{id}")
def update_member(id: int, data: MemberUP):
    logging.info("A request to update member by id has been received.")

    updated = MemberDB.update_member(id, data.model_dump(exclude_none=True))

    if not updated:
        logging.error(f"member id {id} not found")
        raise HTTPException(status_code=404, detail=f"member id {id} not found")
    
    logging.info("Request to update member by id completed successfully.")
    return {"msg": f"member id {id} updated."}


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    logging.info("A request to deactive member by id has been received.")
    deactive = MemberDB.deactive_member(id)

    if not deactive:
        logging.info(f"member id {id} not found.")
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    logging.info("Request to deactive member by id completed successfully.")
    return {"msg": f"member id {id} become deactive"}


@router.patch("/{id}/activate")
def deactivate_member(id: int):
    logging.info("A request to active member by id has been received.")
    active = MemberDB.active_member(id)

    if not active:
        logging.info(f"member id {id} not found.")
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    logging.info("Request to active member by id completed successfully.")
    return {"msg": f"member id {id} become active"}
        