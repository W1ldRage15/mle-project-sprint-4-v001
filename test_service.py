import requests
import logging
logger = logging.getLogger(__name__)

recommendations_url = "http://127.0.0.1:8000"
events_store_url = "http://127.0.0.1:8020"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
logging.basicConfig(filename='test_service.log', level=logging.INFO)

# для пользователя без персональных рекомендаций
user_id = 2085
event_track_ids =  [7892587, 7984268, 8309869, 20683928]
for event_track_id in event_track_ids:
    resp = requests.post(events_store_url + "/put", 
                         headers=headers, 
                         params={"user_id": user_id, "track_id": event_track_id})

params = {"user_id": user_id, 'k': 10}
resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

logger.info('Started for user without personal recs')
logger.info(recs_offline)
logger.info(recs_online)
logger.info(recs_blended)
logger.info('Finished for user without personal recs')


# для пользователя с персональными рекомендациями, но без онлайн-истории
user_id = 3

params = {"user_id": user_id, 'k': 10}
resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

logger.info('Started for user without online history')
logger.info(recs_offline)
logger.info(recs_online)
logger.info(recs_blended)
logger.info('Finished for user without online history')


# для пользователя с персональными рекомендациями и онлайн-историей
user_id = 4
event_track_ids =  [966, 4094, 9760, 9769, 18392]

for event_track_id in event_track_ids:
    resp = requests.post(events_store_url + "/put", 
                         headers=headers, 
                         params={"user_id": user_id, "track_id": event_track_id})
    
params = {"user_id": user_id, 'k': 10}
resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)

recs_offline = resp_offline.json()["recs"]
recs_online = resp_online.json()["recs"]
recs_blended = resp_blended.json()["recs"]

logger.info('Started for user with all recs')
logger.info(recs_offline)
logger.info(recs_online)
logger.info(recs_blended)
logger.info('Finished for user with all recs')
logger.info('All comments about results in the end of README')
