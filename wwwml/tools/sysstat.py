from langchain.tools import tool
import subprocess


def shell(cmd):
    output = subprocess.check_output(cmd, shell=True)
    return output


@tool
def free():
    """free - Display amount of free and used memory in the system"""
    return shell("free")


@tool
def iostat():
    """iostat - Report Central Processing Unit (CPU) statistics and input/output statistics for devices and partitions."""
    return shell("iostat")


@tool
def mpstat():
    """mpstat - Report processors related statistics"""
    return shell("mpstat")
