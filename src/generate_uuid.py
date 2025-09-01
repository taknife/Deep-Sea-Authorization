#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/28 15:40
# @Author  : taknife
# @Project : Deep-Sea-Authorization
# @File    : generate_uuid.py

from subprocess import check_output
from hashlib import sha1
from re import sub


def get_motherboard_uuid():
    """获取主板 UUID"""
    try:
        # 尝试用 wmic 获取 UUID
        result = check_output("wmic csproduct get UUID", shell=True).decode().strip().split("\n")
        uuid = result[1].strip() if len(result) > 1 else None
        if uuid and uuid != "UUID":
            return uuid

        # wmic 获取失败，尝试使用 PowerShell
        result = check_output(
            "powershell -command \"(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID\"",
            shell = True
        ).decode().strip()
        return result if result else "UNKNOWN_UUID"

    except Exception as e:
        return f"Error: {e}"


def get_cpu_id():
    """获取 CPU 序列号"""
    try:
        # wmic 获取 CPU ID
        result = check_output("wmic cpu get ProcessorId", shell=True).decode().strip().split("\n")
        cpu_id = result[1].strip() if len(result) > 1 else None
        if cpu_id:
            return cpu_id

        # wmic 失败，尝试 PowerShell
        result = check_output(
            "powershell -command \"(Get-CimInstance -Class Win32_Processor).ProcessorId\"",
            shell = True
        ).decode().strip()
        return result if result else "UNKNOWN_CPU"

    except Exception as e:
        return f"Error: {e}"


def sha1_uuid():
    """生成 SHA1 哈希的 UUID"""
    cpu_id = get_cpu_id()
    mb_uuid = get_motherboard_uuid()
    key = "q8s(9*&m$k"

    if "Error" in cpu_id or "Error" in mb_uuid:
        return "ERROR_GENERATING_UUID"

    uid_str = f"{cpu_id}-{mb_uuid}-{key}"
    sha1_hash = sha1()
    sha1_hash.update(uid_str.encode('utf-8'))
    return sha1_hash.hexdigest()


def format_uuid():
    """格式化 UUID（4-4-4-4-4 形式）"""
    raw_uuid = sha1_uuid()
    return sub(r"(.{4})", r"\1-", raw_uuid)[:-1]


# 运行测试
print("CPU ID:", get_cpu_id())
print("Motherboard UUID:", get_motherboard_uuid())
print("Generated UUID:", format_uuid())
