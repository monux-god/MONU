#!/usr/bin/env python3
"""
MONU PAPA BOT - State Management System
"""

from enum import Enum, auto

class State(Enum):
    MAIN_MENU = auto()
    WAIT_NUMBER = auto()
    WAIT_TG = auto()
    WAIT_AADHAR = auto()
    WAIT_PAYMENT_PROOF = auto()
    ADMIN_BROADCAST = auto()
    ADMIN_GIVE_CREDIT_ID = auto()
    ADMIN_GIVE_CREDIT_AMT = auto()
    ADMIN_ADD_UNLIMITED_ID = auto()
    ADMIN_ADD_UNLIMITED_DAYS = auto()

STATE_LABELS = {
    State.WAIT_NUMBER: "WAIT_NUMBER",
    State.WAIT_TG: "WAIT_TG",
    State.WAIT_AADHAR: "WAIT_AADHAR",
    State.WAIT_PAYMENT_PROOF: "WAIT_PAYMENT_PROOF",
    State.ADMIN_BROADCAST: "ADMIN_BROADCAST",
    State.ADMIN_GIVE_CREDIT_ID: "ADMIN_GIVE_CREDIT_ID",
    State.ADMIN_GIVE_CREDIT_AMT: "ADMIN_GIVE_CREDIT_AMT",
    State.ADMIN_ADD_UNLIMITED_ID: "ADMIN_ADD_UNLIMITED_ID",
    State.ADMIN_ADD_UNLIMITED_DAYS: "ADMIN_ADD_UNLIMITED_DAYS"
}