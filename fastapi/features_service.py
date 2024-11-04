import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI

logger = logging.getLogger(__name__)
logging.basicConfig(filename='../rec_service.log', level=logging.INFO)
class SimilarItems:

    def __init__(self):

        self._similar_items = None

    def load(self, type, path, **kwargs):
        """
        Загружаем данные из файла
        """
        logger.info(f"Loading data, type: {type}")
        self._similar_items = pd.read_parquet(path, **kwargs)
        self._similar_items = self._similar_items.set_index("track_id_1")
        logger.info(f"Loaded")

    def get(self, track_id: int, k: int = 10):
        """
        Возвращает список похожих объектов
        """
        try:
            i2i = self._similar_items.loc[track_id].head(k)
            i2i = i2i[["track_id_2", "score"]].to_dict(orient="list")
        except KeyError:
            logger.error(f"No recommendations found for track_id: {track_id}")
            i2i = {"track_id_2": [], "score": {}}

        return i2i

sim_items_store = SimilarItems()

@asynccontextmanager
async def lifespan(app: FastAPI):
    sim_items_store.load(
        "similar",
        "../recsys/recommendations/similar.parquet",
        columns=["track_id_1", "track_id_2", "score"],
    )
    logger.info("Ready!")
    yield

app = FastAPI(title="features", lifespan=lifespan)

@app.post("/similar_items")
async def recommendations(track_id: int, k: int = 10):
    """
    Возвращает список похожих объектов длиной k для track_id
    """
    i2i = sim_items_store.get(track_id, k)

    return i2i