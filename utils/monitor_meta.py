import abc
import time
import csv
import os
import logging
from functools import wraps
from datetime import datetime

logger = logging.getLogger(__name__)

def api_monitor(retry_limit=3):
    """
    Generic decorator for timing, retrying, and logging failures to CSV.
    :param retry_limit: Total number of attempts (default 3).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0]  # The 'self' instance of the device
            last_err = None

            for attempt in range(1, retry_limit + 1):
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_err = e
                    duration = time.perf_counter() - start
                    logger.warning(f"API {func.__name__} attempt {attempt}/{retry_limit} failed: {e}")
                    
                    if attempt == retry_limit:
                        # Final failure logic: Log to CSV
                        _log_to_csv(func.__name__, str(e), duration)
                        
                        # Trigger failure recovery if defined in the instance
                        if hasattr(instance, "on_api_final_failure"):
                            instance.on_api_final_failure(func.__name__, e)
                        
                        raise last_err
                    time.sleep(0.5) 
            return None
        return wrapper
    return decorator

def _log_to_csv(api, err, dur):
    """Utility to log error data into a CSV file."""
    file = "api_failure_report.csv"
    headers = ["Timestamp", "API", "Error", "Duration"]
    exists = os.path.isfile(file)
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not exists:
            writer.writeheader()
        writer.writerow({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "API": api, "Error": err, "Duration": f"{dur:.4f}"
        })

class ApiMonitorMeta(abc.ABCMeta):
    """
    Metaclass that auto-injects monitor logic based on exclusion rules.
    """
    def __new__(mcls, name, bases, attrs):
        # Define which methods should NEVER be monitored to prevent recursion
        exclude_list = attrs.get("_EXCLUDE_FROM_MONITOR", [])
        
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and not attr_name.startswith("_"):
                if attr_name not in exclude_list:
                    attrs[attr_name] = api_monitor()(attr_value)
        return super().__new__(mcls, name, bases, attrs)