
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Endpoint to get all drones
@app.get("/drones/")
async def get_drones():
    pass

# Endpoint to get all drones by availability status
@app.get("/drones/{status}")
async def get_drones_by_status(status):
    pass

# Endpoint to get a specific drone by ID
@app.get("/drones/{id}")
async def get_drone_by_id(id):
    pass

# Endpoint to update a drone's status
@app.put("/drones/{id}")
async def update_drone_status(id, status):
    pass

# Endpoint to create a new drone    
@app.post("/drones/")
async def create_drone(id, name, status, current_mission_id,possible_missions_ids, image):
    pass

# Endpoint to modify possible missions for a drone
@app.put("/drones/{id}/possible_missions")
async def modify_possible_missions(id, possible_missions_ids):
    pass


# Endpoint to get all missions
@app.get("/missions/")
async def get_missions():
    pass

# Endpoint to create a new mission
@app.post("/missions/")
async def create_mission(id, trjectory,duration,distance):
    pass


# Endpoint to get all schedules
@app.get("/schedules/")
async def get_schedules():
    pass



# Endpoint to create a new schedule
@app.post("/schedules/")
async def create_schedule(id, drone_id, mission_id, start_time, end_time,status):
    pass

# Endpoint to update a schedule's status
@app.put("/schedules/{id}")
async def update_schedule_status(id, status):
    pass

# Endpoint to get schedules date range
@app.get("/schedules/{start_date}/{end_date}")
async def get_schedules_date_range(start_date, end_date):
    pass

# Endpoint to get schedules by drone
@app.get("/schedules/{drone_id}")
async def get_schedules_by_drone(drone_id):
    pass

mongodb_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
