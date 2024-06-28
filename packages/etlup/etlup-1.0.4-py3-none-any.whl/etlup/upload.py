from .data_models import ConstrCongAdapter, load_model
from datetime import datetime
from pydantic import TypeAdapter
from typing import Union
import json
import pytz
import os
import warnings

def user_default_tz():
    """
    !NOT IMPLEMENTED! It would be nice to auto catch user timezone from their computer maybe
    """
    user_tz = datetime.now().astimezone().tzinfo
    warnings.warn(f"Explicit timezone information was not provided using your system default: {user_tz}")
    return user_tz

def val_datetime(date_obj: Union[str, datetime]) -> datetime:
    dt = TypeAdapter(datetime)
    return dt.validate_python(date_obj)


class ETLup:
    def __init__(self, api_key: Union[str, None] = None, timezone: Union[str, None] = None):
        self.api_key = api_key
        self.timezone = timezone #measurement date tz takes precedent though
        self._constrs = [] #list of filled data models
        self._process_timezone()

    def _process_timezone(self):
        #check timezone is a valid timezone
        if self.timezone is not None:
            if self.timezone not in pytz.all_timezones:
                raise ValueError(f"Your timezone {self.timezone} is not a valid timezone, please select a correct one from: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
            #get it to timezone object
            self.timezone = pytz.timezone(self.timezone)
            #if it is None and measurement date has no timezone the model validator will catch it!

    def add_constr(self, constr_dict: dict):
        #validate measurement date for timezone info
        if isinstance(constr_dict, dict) and 'measurement_date' in constr_dict:
            meas_date = val_datetime(constr_dict['measurement_date']) #gets string into datetime obj, and validates for free
            if meas_date.tzinfo is None and self.timezone is not None:
                constr_dict['measurement_date'] = self.timezone.localize(meas_date) #interprets meas_date to be in the self.timezone time
        #append loaded model to constr
        self._constrs.append(load_model(constr_dict))
        return self
    
    def to_file(self, filepath=""):
        if self._constrs == []:
            raise ValueError("Cannot convert to file when no assembly or tests were uploaded")
        if not filepath:
            filepath = os.path.join(os.getcwd(), 'construction_upload.json')
        with open(filepath, 'w') as json_file:
            validated_cong = ConstrCongAdapter.validate_python(self._constrs)
            cong_bytes = ConstrCongAdapter.dump_json(validated_cong)
            #do this to get the correct mime type!
            cong_obj = json.loads(cong_bytes.decode('utf-8'))
            json.dump(cong_obj, json_file, indent=4)