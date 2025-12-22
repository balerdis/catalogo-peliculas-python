#/app/core/database/models.py
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, Boolean, Date, BigInteger, Text, ForeignKey, func
from .connection import Base
from sqlalchemy.orm import relationship