
from datetime import datetime
from fastapi import FastAPI, HTTPException
from typing import List
from models import Drone,Mission,Schedule,ScheduleCreatePayload,CreateDronePayload,UpdateStatusPayload,CreateMissonPayload,ModifyPossibleMissionsPayload
from db.database import Database
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")
mongodb_uri = config['MONGODB_URI']
db_name = config['DB_NAME']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database(mongodb_uri, db_name)
drones_collection = db.get_collection("Drones")
missions_collection = db.get_collection("Missions")
schedules_collection = db.get_collection("Schedules")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/drones/", response_model=List[Drone])
async def get_drones():
    try:
        drones = list(drones_collection.find())
        return drones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drones/status/{status}", response_model=List[Drone])
async def get_drones_by_status(status: str):
    try:
        drones = list(drones_collection.find({"status": status}))
        if not drones:
            raise HTTPException(status_code=404, detail="No drones found with the specified status")
        return drones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drones/id/{id}",response_model=Drone)
async def get_drone_by_id(id: int):
    try:
        drone = drones_collection.find_one({"id": id})
        if not drone:
            raise HTTPException(status_code=404, detail="No drones found with the specified id")
        return drone
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
        
@app.put("/drones/{id}", response_model=Drone)
async def update_drone_status(id: int, payload: UpdateStatusPayload):
    try:
            drone = drones_collection.find_one({"id": id})
            if not drone:
                raise HTTPException(status_code=404, detail="No drones found with the specified id")

            new_status = payload.status
            drones_collection.update_one({"id": id}, {"$set": {"status": new_status}})
            updated_drone = drones_collection.find_one({"id": id})
            return updated_drone

    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/drones/",response_model=Drone)
async def create_drone(payload: CreateDronePayload):
    try:
        last_drone = drones_collection.find_one(sort=[("id", -1)])
        if last_drone:
            drone_id = last_drone["id"] + 1
        else:
            drone_id = 1

        drone = Drone(
            id=drone_id,
            name=payload.name,
            status=payload.status,
            current_mission_id=payload.current_mission_id,
            possible_missions_ids=payload.possible_missions_ids,
        )
        drone_dict = drone.__dict__
        drones_collection.insert_one(drone_dict)
        created_drone = drones_collection.find_one({"id": drone_id})
        return created_drone
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.put("/drones/{id}/possible_missions", response_model=Drone)
async def modify_possible_missions(id: int, payload: ModifyPossibleMissionsPayload):
    try:
        drone = drones_collection.find_one({"id": id})
        if not drone:
            raise HTTPException(status_code=404, detail="No drones found with the specified id")
        drones_collection.update_one({"id": id}, {"$set": {"possible_missions_ids": payload.possible_missions_ids}})
        updated_drone = drones_collection.find_one({"id": id})
        
        return updated_drone

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/missions/", response_model=List[Mission])
async def get_missions():
    try:
        missions = list(missions_collection.find())
        return missions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
           
@app.post("/missions/", response_model=Mission)
async def create_mission(payload: CreateMissonPayload):
    try:
        last_mission = missions_collection.find_one(sort=[("id", -1)])
        if last_mission:
            mission_id = last_mission["id"] + 1
        else:
            mission_id = 1
        mission = Mission(
            id=mission_id,
            trajectory_id=payload.trajectory_id,
            duration=payload.duration,
            priority=payload.priority,
        )
        mission_dict = mission.__dict__
        missions_collection.insert_one(mission_dict)

        created_mission = missions_collection.find_one({"id": mission_id})
        return created_mission
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schedules/", response_model=List[Schedule])
async def get_schedules():
    try:
        schedules = list(schedules_collection.find())
        return schedules
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
@app.post("/schedules/",response_model=Schedule)
async def create_schedule(payload: ScheduleCreatePayload):
    try:
        last_schedule = schedules_collection.find_one(sort=[("id", -1)])
        if last_schedule:
            schedule_id = last_schedule["id"] + 1
        else:
            schedule_id = 1

        schedule = Schedule(
            id=schedule_id,
            drone_id=payload.drone_id,
            mission_id=payload.mission_id,
            start_time=payload.start_time,
            end_time=payload.end_time,
            status=payload.status,
        )
        schedule_dict = schedule.__dict__
        schedules_collection.insert_one(schedule_dict)
        created_schedule = schedules_collection.find_one({"id": schedule_id})
        return created_schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/schedules/{id}",response_model=Schedule)
async def update_schedule_status(id:int, payload: UpdateStatusPayload):
    try:
        existing_schedule = schedules_collection.find_one({"id": id})
        if not existing_schedule:
            raise HTTPException(status_code=404, detail=f"Schedule with id {id} not found")
        schedules_collection.update_one({"id": id}, {"$set": {"status": payload.status}})
        updated_schedule = schedules_collection.find_one({"id": id})
        return updated_schedule

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schedules/{start_date}/{end_date}",response_model=List[Schedule])
async def get_schedules_date_range(start_date,end_date):
    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
        schedules = list(schedules_collection.find({
            "start_time": {"$gte": start_datetime},
            "end_time": {"$lte": end_datetime}
        }))
        response_schedules = [
            Schedule(
                id=schedule["id"],
                drone_id=schedule["drone_id"],
                mission_id=schedule["mission_id"],
                start_time=schedule["start_time"],
                end_time=schedule["end_time"],
                status=schedule["status"],
            )
            for schedule in schedules
        ]

        return response_schedules

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/schedules/{drone_id}",response_model=List[Schedule])
async def get_schedules_by_drone(drone_id:int):
    try:
        schedules = list(schedules_collection.find({"drone_id": drone_id}))
        response_schedules = [
            Schedule(
                id=schedule["id"],
                drone_id=schedule["drone_id"],
                mission_id=schedule["mission_id"],
                start_time=schedule["start_time"],
                end_time=schedule["end_time"],
                status=schedule["status"],
            )
            for schedule in schedules
        ]

        return response_schedules

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
