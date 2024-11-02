import logging
import pandas as pd
from fastapi import FastAPI
from contextlib import asynccontextmanager
import requests
from rec_service import Recommendations
features_store_url = "http://127.0.0.1:8010"
events_store_url = "http://127.0.0.1:8020"

logger = logging.getLogger("uvicorn.error")

rec_store = Recommendations()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting")
    rec_store.load(
        "personal",
        "../recsys/recommendations/recommendations.parquet",
        columns=["user_id", "track_id", "cb_score"],
    )
    rec_store.load(
        "default",
        "../recsys/recommendations/top_popular.parquet",
        columns=["track_id", "score"],
    )
    yield
    logger.info("Stopping")
    
app = FastAPI(title="recommendations", lifespan=lifespan)

def dedup_ids(ids):
    """
    Дедублицирует список идентификаторов, оставляя только первое вхождение
    """
    seen = set()
    ids = [id for id in ids if not (id in seen or seen.add(id))]

    return ids

@app.post("/recommendations_online")
async def recommendations_online(user_id: int, k: int = 100):
    """
    Возвращает список онлайн-рекомендаций длиной k для пользователя user_id
    """
    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    params = {"user_id": user_id, "k": k}
    resp = requests.post(events_store_url + "/get", headers=headers, params=params)
    events = resp.json()
    events = events["events"]
    items = []
    scores = []
    for track_id in events:
        params = {"track_id": track_id, "k": k}
        resp = requests.post(features_store_url +"/similar_items", headers=headers, params=params)
        item_similar_items = resp.json()
        items += item_similar_items["track_id_2"]
        scores += item_similar_items["score"]
    combined = list(zip(items, scores))
    combined = sorted(combined, key=lambda x: x[1], reverse=True)
    combined = [item for item, _ in combined]

    recs = dedup_ids(combined)

    return {"recs": recs[:k]}

@app.post("/recommendations_offline")
async def recommendations_offline(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """
    recs = rec_store.get(user_id, k)

    return {"recs": recs}

@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 100):
    """
    Возвращает список рекомендаций длиной k для пользователя user_id
    """
    recs_offline = await recommendations_offline(user_id, k)
    recs_online = await recommendations_online(user_id, k)
    recs_offline = recs_offline["recs"]
    recs_online = recs_online["recs"]
    recs_blended = []

    min_length = min(len(recs_offline), len(recs_online))
    for i in range(min_length):
        if i%2==0:
            recs_blended.append(recs_offline[i])
        else:
            recs_blended.append(recs_online[i])
        
    if min_length < k:
        for i in range(k-min_length):
            if (k-min_length)%2==0:
                recs_blended.append(recs_offline[min_length+i])
            else:
                recs_blended.append(recs_online[min_length+i])
    recs_blended = dedup_ids(recs_blended)
    recs_blended = recs_blended[:k]

    return {"recs": recs_blended}