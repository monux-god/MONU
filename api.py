#!/usr/bin/env python3
"""
MONU PAPA BOT - Professional API Manager
Fixed: New API format, records parse from "0","1" keys
"""

import requests
import config

class APIManager:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })
        self.timeout = 20

    def _execute(self, url, params=None):
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()
            return {"error": f"HTTP_{response.status_code}"}
        except requests.exceptions.Timeout:
            return {"error": "TIMEOUT"}
        except requests.exceptions.ConnectionError:
            return {"error": "CONNECTION_ERROR"}
        except Exception as e:
            return {"error": str(e)}

    def fetch_number_data(self, phone):
        """Fetch number data - Parse from direct numeric keys"""
        params = {"key": config.API_KEY, "mobile": phone}
        raw_data = self._execute(config.NUM_API_URL, params)
        
        if raw_data and raw_data.get("error"):
            return {
                "success": False,
                "error": raw_data.get("error"),
                "records": [],
                "total": 0
            }
        
        records = []
        
        if raw_data and isinstance(raw_data, dict):
            for key, value in raw_data.items():
                if key in ["success", "developer", "requested_mobile", "message", "status"]:
                    continue
                
                if key.isdigit() and isinstance(value, dict):
                    if value.get("NAME") or value.get("num") or value.get("MOBILE") or value.get("fname") or value.get("ADDRESS"):
                        records.append(value)
        
        if records:
            return {
                "success": True,
                "records": records,
                "total": len(records),
                "raw": raw_data
            }
        
        return {
            "success": False,
            "error": "NOT_IN_DATABASE",
            "records": [],
            "total": 0
        }

    def fetch_telegram_data(self, term):
        """Fetch Telegram data from API"""
        url = "https://raixinfo3.vercel.app/api/tg"
        params = {"key": config.API_KEY, "id": term}
        raw_data = self._execute(url, params)
        
        if raw_data and raw_data.get("error"):
            return {"success": False, "error": raw_data.get("error")}
        
        if raw_data and raw_data.get("success") and raw_data.get("number"):
            return {
                "success": True,
                "data": {
                    "number": raw_data.get("number"),
                    "country": raw_data.get("country"),
                    "country_code": raw_data.get("country_code"),
                    "cached": raw_data.get("cached"),
                    "response_time": raw_data.get("response_time")
                }
            }
        return {"success": False, "error": "NOT_IN_DATABASE"}

    def fetch_aadhar_data(self, aadhar):
        params = {"key": config.API_KEY, "type": "family", "term": aadhar}
        api_res = self._execute(config.AADHAR_API_URL, params)
        
        if not api_res:
            return {"success": False, "error": "NO_RESPONSE"}
        
        if api_res.get("error"):
            return {"success": False, "error": api_res.get("error")}
        
        details = None
        
        if api_res.get("data"):
            dw = api_res.get("data", {})
            if isinstance(dw, dict):
                if dw.get("details"):
                    details = dw.get("details")
                elif dw.get("result") and dw.get("result").get("details"):
                    details = dw.get("result").get("details")
        
        if not details and api_res.get("result"):
            rw = api_res.get("result", {})
            if isinstance(rw, dict) and rw.get("details"):
                details = rw.get("details")
                
        if not details and api_res.get("details"):
            details = api_res.get("details")

        if details and (details.get("card_info") or details.get("members")):
            return {"success": True, "details": details}
        
        return {"success": False, "error": "SERVICE_OFF"}

engine = APIManager()