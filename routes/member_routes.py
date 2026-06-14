import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal

logger = logging.getLogger(__name__)


router = APIRouter()