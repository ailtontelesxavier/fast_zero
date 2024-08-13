from datetime import datetime
from http import HTTPStatus
from typing import Annotated

import pytz
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fast_zero.core.database import get_session

from fast_zero.juridico.models import NegociacaoCredito, ParcelamentoNegociacao

router = APIRouter(prefix='/juridico', tags=['negociação'])
T_Session = Annotated[Session, Depends(get_session)]