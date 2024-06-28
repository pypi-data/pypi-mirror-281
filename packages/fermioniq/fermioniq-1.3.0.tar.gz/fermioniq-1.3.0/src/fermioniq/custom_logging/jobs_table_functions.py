from datetime import datetime

from rich import box
from rich.table import Table


def format_time(time: str | None) -> str:
    if time is None:
        return "-"
    else:
        dt_obj = datetime.fromisoformat(time)
        # Detect local timezone
        local_tz = datetime.now().astimezone().tzinfo
        dt_obj_local = dt_obj.astimezone(local_tz)

        return str(dt_obj_local.strftime("%d-%m %H:%M:%S"))


def format_status(slurm_status: str, status_code: int) -> str:

    match status_code:
        case -1:
            status = slurm_status
        case 0:
            status = "finished"
        case 1:
            status = "failed"
        case 2:
            status = "timeout"
        case 3:
            status = "out of memory"
        case 4:
            status = "node fail"
        case 128:
            status = "cancelled"
        case 200:
            status = "unknown error"

    return status
