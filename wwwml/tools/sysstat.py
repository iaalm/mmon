import subprocess

from langchain.tools import tool
from loguru import logger


def shell(cmd) -> str:
    output = subprocess.check_output(cmd, shell=True)
    return output


@tool
def iostat() -> str:
    """iostat - Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions."""

    logger.info("Checking IO")
    return shell("iostat -dxsm 1 3 | grep -v loop")


@tool
def vmstat() -> str:
    """vmstat - Report virtual memory statistics."""

    logger.info("Checking Memory")
    return shell("vmstat -S m 1 3")


@tool
def mpstat() -> str:
    """mpstat - Report processors related statistics."""

    logger.info("Checking CPU")
    return shell("mpstat 1 3")


@tool
def cat(filename: str) -> str:
    """cat - Read file. Only allow files in /proc and /sys"""

    logger.info(f"Reading file {filename}")
    if not filename.startswith("/proc/") and not filename.startswith("/sys/"):
        logger.warning("try to read file not in /proc or /sys")
        return ""

    with open(filename, "r") as f:
        return "\n".join(f.readlines())
