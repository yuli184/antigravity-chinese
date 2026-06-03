# -*- coding: utf-8 -*-
"""
Antigravity 2.0 汉化还原脚本
"""

import os
import sys
import shutil
import subprocess
import time

def detect_resources_path():
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        path = os.path.join(local_app_data, "Programs", "antigravity", "resources")
        if os.path.exists(path):
            return path
    elif sys.platform == "darwin":
        path = "/Applications/Antigravity.app/Contents/Resources"
        if os.path.exists(path):
            return path
    else:
        path = os.path.expanduser("~/Antigravity/Antigravity-x64/resources")
        if os.path.exists(path):
            return path
    return None

def terminate_processes():
    print("正在清理占用文件的后台进程...")
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "Antigravity.exe"], capture_output=True)
        subprocess.run(["taskkill", "/F", "/IM", "language_server.exe"], capture_output=True)
    else:
        subprocess.run(["pkill", "-f", "Antigravity"], capture_output=True)
        subprocess.run(["pkill", "-f", "language_server"], capture_output=True)
    time.sleep(2)

def main():
    print("==========================================")
    print("  Antigravity 2.0 英文原版恢复工具")
    print("==========================================")
    
    resources_dir = detect_resources_path()
    if not resources_dir:
        print("错误：未能自动探测到软件的安装路径。")
        input("按任意键退出...")
        sys.exit(1)
        
    print(f"检测到软件资源路径：{resources_dir}")
    input("请确保软件已完全关闭。按下【回车键】开始还原英文版...")

    terminate_processes()

    asar_file = os.path.join(resources_dir, "app.asar")
    backup_file = os.path.join(resources_dir, "app.asar.bak")

    if os.path.exists(backup_file):
        try:
            # 恢复原版
            os.remove(asar_file)
            shutil.copy2(backup_file, asar_file)
            # 可选：删除备份，或者保留备份文件
            os.remove(backup_file)
            print("\n🎉 成功还原为英文原版！备份文件已清理。")
        except Exception as e:
            print(f"\n❌ 还原失败: {e}")
    else:
        print("\n❌ 未找到原版备份文件 (app.asar.bak)，无法自动还原。")
        print("如果是由于软件损坏，建议重新安装客户端即可。")

    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
