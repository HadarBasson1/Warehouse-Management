from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Union
from bson import ObjectId

class Drone(BaseModel):
    id: int
    name: str
    status: str
    current_mission_id: Optional[Union[int, str]]
    possible_missions_ids: List[int]

class Mission(BaseModel):
    id: int
    trajectory_id: int
    duration: int
    priority: int


class TimestampModel(BaseModel):
    t: int
    i: int

class Schedule(BaseModel):
    id: int
    drone_id: int
    mission_id: int
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        json_encoders = {
            ObjectId: str
        }

class ScheduleCreatePayload(BaseModel):
    drone_id: int
    mission_id: int
    start_time: datetime    
    end_time: datetime    
    status: str

class CreateDronePayload(BaseModel):
    name: str
    status: str
    current_mission_id: Optional[int]
    possible_missions_ids: List[int]


class UpdateStatusPayload(BaseModel):
     status: str

class CreateMissonPayload(BaseModel):
    trajectory_id: int
    duration: int
    priority: int

class ModifyPossibleMissionsPayload(BaseModel):
    possible_missions_ids: List[int]
