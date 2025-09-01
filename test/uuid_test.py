#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/29 15:32
# @Author  : taknife
# @Project : Deep-Sea-Authorization
# @File    : uuid_test.py
import uuid
import hashlib
import platform
import os
import subprocess
import sys

def get_mac_address():
    """获取 MAC 地址"""
    mac = uuid.getnode()
    return str(mac)

def get_machine_id():
    """获取系统唯一标识，跨平台"""
    system = platform.system()
    machine_id = ""

    try:
        if system == "Windows":
            # 使用 wmic 获取主板序列号
            cmd = 'wmic baseboard get serialnumber'
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            lines = output.decode().splitlines()
            if len(lines) >= 2:
                machine_id = lines[1].strip()
        elif system == "Linux":
            # 尝试读取 /etc/machine-id
            if os.path.exists("/etc/machine-id"):
                with open("/etc/machine-id", "r") as f:
                    machine_id = f.read().strip()
            else:
                # fallback: 使用主机名
                machine_id = platform.node()
        elif system == "Darwin":  # macOS
            cmd = "ioreg -l | grep IOPlatformSerialNumber"
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
            output = output.decode()
            # 解析序列号
            import re
            match = re.search(r'"IOPlatformSerialNumber" = "(.+)"', output)
            if match:
                machine_id = match.group(1)
    except Exception as e:
        # 出现异常就用主机名
        machine_id = platform.node()

    return machine_id or "unknown_machine"

def generate_device_uuid():
    """生成跨平台硬件指纹 UUID"""
    hw_info = []

    # 系统信息
    hw_info.append(platform.system())
    hw_info.append(platform.machine())
    hw_info.append(platform.version())
    hw_info.append(platform.processor())

    # 硬件唯一标识
    hw_info.append(get_machine_id())
    hw_info.append(get_mac_address())

    # 拼接成字符串
    hw_string = "-".join(hw_info)

    # SHA256 哈希
    hash_digest = hashlib.sha256(hw_string.encode()).hexdigest()

    # 转成 UUID
    device_uuid = str(uuid.UUID(hash_digest[:32]))
    return device_uuid

if __name__ == "__main__":
    device_uuid = generate_device_uuid()
    print("本设备唯一 UUID:", device_uuid)
