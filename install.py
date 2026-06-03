# -*- coding: utf-8 -*-
"""
Antigravity 2.0 一键汉化注入脚本 (增强版 - 包含确认对话框及系统词汇汉化)
支持 Windows, macOS, Linux
"""

import os
import sys
import shutil
import subprocess
import time
import tempfile

# ---------------------------------------------------------
# 1. 默认安装路径探测
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 2. 依赖检查 (asarPy)
# ---------------------------------------------------------
def ensure_asarpy():
    try:
        import asarPy
    except ImportError:
        print("正在自动安装解包组件 (asarPy)...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "asarPy"], check=True, capture_output=True)
            print("组件安装成功！")
        except Exception as e:
            print(f"组件安装失败，请手动运行 'pip install asarPy' 后重试。错误: {e}")
            sys.exit(1)

# ---------------------------------------------------------
# 3. 强行关闭占用进程
# ---------------------------------------------------------
def terminate_processes():
    print("正在清理占用文件的后台进程...")
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/F", "/IM", "Antigravity.exe"], capture_output=True)
        subprocess.run(["taskkill", "/F", "/IM", "language_server.exe"], capture_output=True)
    else:
        subprocess.run(["pkill", "-f", "Antigravity"], capture_output=True)
        subprocess.run(["pkill", "-f", "language_server"], capture_output=True)
    time.sleep(2)

# ---------------------------------------------------------
# 4. 汉化核心注入代码 (新增确认弹窗相关词条)
# ---------------------------------------------------------
DOM_TRANSLATOR_CODE = """
// --- Antigravity Chinese Translation Injection ---
(function() {
    const dict = {
        // 侧边栏
        "New Conversation": "新建对话",
        "Conversation History": "历史对话",
        "Scheduled Tasks": "定时任务",
        "Shortcuts": "快捷键",
        "Provide Feedback": "提供反馈",

        // 设置左侧菜单与标题
        "General": "常规",
        "Account": "账户",
        "Permissions": "权限",
        "Appearance": "外观",
        "Models": "模型",
        "Customizations": "自定义",
        "Browser": "浏览器",
        "App": "应用",
        "Conversations": "会话",
        
        // 会话安全与配置
        "Security Preset": "安全预设",
        "Choose a predefined security preset for the agent. This controls terminal auto-execution policy, and file access policy.": "为智能体选择预设的安全级别。这控制了终端的自动执行策略和文件访问策略。",
        "Outside of folders file access policy": "工作文件夹外文件访问策略",
        "Configures how the agent tries to access files outside of its working folders.": "配置智能体尝试访问其工作文件夹之外的文件时的策略。",
        "Terminal Command Auto Execution": "终端命令自动执行",
        "Controls whether terminal commands require your approval before running.": "控制终端命令在运行前是否需要您的批准。",
        "Agent Behavior": "智能体行为",
        "Artifact Review Policy": "交付物（Artifact）审核策略",
        "Specifies Agent's behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在要求审核交付物时的行为，交付物是它创建的文档以提供更丰富的对话体验。",
        "Local Permissions": "本地权限",
        "Inherits from": "继承自",
        "global settings": "全局设置",
        "Local permissions have higher priority.": "本地权限优先级更高。",
        "Learn more": "了解更多",
        "File Access Rules": "文件访问规则",
        "Configure allowed and denied paths for file reads and writes.": "配置文件读写的允许和拒绝路径。",
        "Network Access Rules": "网络访问规则",
        "Configure allowed and denied URLs for reading.": "配置允许和拒绝访问的网址。",
        "Terminal Commands": "终端命令",
        "Configure allowed terminal commands.": "配置允许执行的终端命令。",
        "Open": "打开",
        "Always Ask": "总是询问",
        "Require Review": "需要审核",
        "Custom": "自定义",
        
        // 外观设置
        "Verbose agent chat": "详细智能体思考过程",
        "Display and preserve intermediate thinking steps": "显示并保留中间思考步骤",
        "Select light, dark, or inherit system settings.": "选择浅色、深色，或继承系统设置。",
        "Light Theme": "浅色主题",
        "Dark Theme": "深色主题",
        "Preset": "预设",
        "Background": "背景",
        "Foreground": "前景",
        "Accent": "强调色",

        // 应用设置
        "Prevent Sleep": "防止休眠",
        "Prevent the computer from sleeping while the app is running.": "软件运行期间防止电脑进入休眠状态。",
        "Keep In Menu Bar": "保持在菜单栏",
        "The app will be accessible from the menu bar and will keep running in the background when all windows are closed.": "即使关闭所有窗口，应用程序仍可通过菜单栏访问，并在后台持续运行。",
        "Manage application settings.": "管理应用程序设置。",
        "App Settings": "应用设置",
        "Notification Settings": "通知设置",
        "Notifications": "通知",
        "Open System Preferences": "打开系统首选项",

        // 账号设置
        "Enable Telemetry": "启用遥测/数据收集",
        "When toggled on, Antigravity collects usage data to help Google enhance performance and features.": "开启后，Antigravity 将收集使用数据以帮助 Google 提升性能和功能。",
        "Marketing Emails": "营销邮件",
        "Receive product updates, tips, and promotions from Google Antigravity via email.": "通过电子邮件接收来自 Google Antigravity 的产品更新、提示和促销信息。",
        "Your Plan: Google AI Pro": "您的计划：Google AI Pro",
        "Upgrade": "升级",
        "Sign Out": "退出登录",
        "By using this app, you agree to its Terms of Service": "使用本应用即表示您同意其服务条款",
        "Terms of Service": "服务条款",
        
        // 聊天交互界面
        "Ask anything, @ to mention, / for actions": "问任何问题，使用 @ 提及，/ 触发指令",
        "Commands": "命令",
        "Type to search...": "搜索命令...",
        "No items found": "未找到匹配项",
        "to navigate": "进行导航",
        "to select": "以选择",
        "Toggle Sidebar": "切换侧边栏",
        "Toggle Auxiliary Pane": "切换辅助面板",
        "Focus Input": "聚焦输入框",
        "Open Settings": "打开设置",

        // -------------------------------------------------
        // 新增：权限及确认弹窗相关词汇
        // -------------------------------------------------
        "Allow": "允许",
        "Deny": "拒绝",
        "Reason": "申请原因",
        "Run Command": "运行命令",
        "Run command": "运行命令",
        "Terminal Command": "终端命令",
        "CommandLine": "命令行",
        "Command Line": "命令行",
        "Execute": "执行",
        "Approved": "已批准",
        "Pending approval": "等待批准",
        "Task ID": "任务 ID",
        "Working Directory": "工作目录",
        "Cancel": "取消",
        "Close": "关闭",
        "Confirm": "确认",
        "Submit": "提交",
        "Skip": "跳过",
        "Requesting permission": "请求运行权限",
        "Insufficient permissions": "权限不足",
        "Permission requested": "已请求权限",
        "Target": "目标",
        "Action": "操作",
        "Grant Permission": "授予权限",
        "Deny Permission": "拒绝权限",
        "Always Allow": "总是允许",
        "Always Deny": "总是拒绝",
        "Always allow for this session": "在此会话中总是允许",
        "Always deny for this session": "在此会话中总是拒绝",
        "Run in background": "后台运行",
        "Keep running in background": "保持后台运行",
        "Execution output": "执行输出",
        "Error executing command": "执行命令时出错",
        "Command completed successfully": "命令执行成功",
        "The command failed with exit code": "命令执行失败，退出代码为",
        "WaitMsBeforeAsync": "异步等待时间（毫秒）",
        "This command is running asynchronously in the background.": "该命令正在后台异步运行。",
        "View logs": "查看日志",
        "Clear logs": "清除日志",
        "Kill task": "终止任务",
        "Command history": "命令历史记录",
        "Operating System": "操作系统",
        "Shell": "终端 Shell",
        "The actual command will NOT execute until you approve it": "在您批准之前，该命令不会实际执行",
        "This tool is proposing to run a command on your behalf": "此工具申请代表您运行以下命令",
        "Ask Permission": "请求授权"
    };

    function walkAndTranslate(node) {
        if (!node) return;
        if (node.nodeType === Node.TEXT_NODE) {
            const val = node.nodeValue;
            const trimmed = val.trim();
            if (dict[trimmed]) {
                node.nodeValue = val.replace(trimmed, dict[trimmed]);
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // 屏蔽输入框的输入内容，仅汉化提示语
            if (node.tagName === 'INPUT' || node.tagName === 'TEXTAREA') {
                const placeholder = node.getAttribute('placeholder');
                if (placeholder && dict[placeholder.trim()]) {
                    node.setAttribute('placeholder', dict[placeholder.trim()]);
                }
            } else if (node.getAttribute && node.getAttribute('contenteditable') === 'true') {
                return; // 屏蔽富文本编辑器内容
            } else if (node.classList && node.classList.contains('monaco-editor')) {
                return; // 屏蔽代码编辑框
            } else {
                for (let i = 0; i < node.childNodes.length; i++) {
                    walkAndTranslate(node.childNodes[i]);
                }
            }
        }
    }

    const observer = new MutationObserver((mutations) => {
        observer.disconnect();
        try {
            for (const mutation of mutations) {
                for (const addedNode of mutation.addedNodes) {
                    walkAndTranslate(addedNode);
                }
                if (mutation.type === 'characterData') {
                    const val = mutation.target.nodeValue;
                    const trimmed = val.trim();
                    if (dict[trimmed]) {
                        mutation.target.nodeValue = val.replace(trimmed, dict[trimmed]);
                    }
                }
            }
        } catch (e) {
            // 忽略翻译中的 DOM 节点异常
        } finally {
            observer.observe(document.body, { childList: true, subtree: true, characterData: true });
        }
    });

    // 页面初次加载翻译
    walkAndTranslate(document.body);
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
})();
"""

# Native 菜单翻译字典
MENU_DICT = {
    "&File": "&文件",
    "&Edit": "&编辑",
    "&View": "&视图",
    "&Window": "&窗口",
    "&Help": "&帮助",
    "About Antigravity": "关于 Antigravity",
    "Services": "服务",
    "Hide Antigravity": "隐藏 Antigravity",
    "Hide Others": "隐藏其他",
    "Show All": "显示全部",
    "Quit Antigravity": "退出 Antigravity",
    "Preferences...": "首选项...",
    "Undo": "撤销",
    "Redo": "恢复",
    "Cut": "剪切",
    "Copy": "复制",
    "Paste": "粘贴",
    "Select All": "全选",
    "Toggle Developer Tools": "切换开发者工具",
    "Minimize": "最小化",
    "Close": "关闭",
    "Zoom": "缩放",
    "Bring All to Front": "全部置于顶层"
}

# ---------------------------------------------------------
# 5. 注入逻辑
# ---------------------------------------------------------
def patch_asar(resources_dir):
    asar_file = os.path.join(resources_dir, "app.asar")
    backup_file = os.path.join(resources_dir, "app.asar.bak")

    # 1. 备份原包
    if not os.path.exists(backup_file):
        print("正在创建原版 app.asar 的备份...")
        shutil.copy2(asar_file, backup_file)
        print("备份创建成功！")
    else:
        print("已检测到原版备份。")

    # 2. 解包到临时文件夹
    temp_dir = os.path.join(tempfile.gettempdir(), f"antigravity_patch_{int(time.time())}")
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
    print("正在解压 app.asar 包...")
    import asarPy
    asarPy.extract_asar(asar_file, temp_dir)

    # 3. 注入 preload.js 和 wizardPreload.js
    preload_paths = [
        os.path.join(temp_dir, "dist", "preload.js"),
        os.path.join(temp_dir, "dist", "ideInstall", "wizardPreload.js")
    ]

    for path in preload_paths:
        if os.path.exists(path):
            print(f"正在注入汉化引擎 -> {os.path.basename(path)}...")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 避免重复注入
            if "Antigravity Chinese Translation Injection" not in content:
                content += "\n" + DOM_TRANSLATOR_CODE
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

    # 4. 汉化 Native Menu
    menu_path = os.path.join(temp_dir, "dist", "menu.js")
    if os.path.exists(menu_path):
        print("正在注入原生菜单翻译...")
        with open(menu_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 将原生菜单的 label 映射替换
        for eng, chn in MENU_DICT.items():
            content = content.replace(f'label: "{eng}"', f'label: "{chn}"')
            content = content.replace(f"label: '{eng}'", f"label: '{chn}'")
            
        with open(menu_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 5. 重打包成 app.asar
    print("正在打包汉化包并覆盖原有程序...")
    asarPy.pack_asar(temp_dir, asar_file)
    
    # 清理临时目录
    shutil.rmtree(temp_dir)
    print("汉化写入完成！")

# ---------------------------------------------------------
# 6. 主执行入口
# ---------------------------------------------------------
def main():
    print("==========================================")
    print("  Antigravity 2.0 一键汉化注入工具")
    print("==========================================")
    
    # 检测路径
    resources_dir = detect_resources_path()
    if not resources_dir:
        print("错误：未能自动探测到 Antigravity 安装目录下的 resources 文件夹。")
        print("请将此脚本移动至 Antigravity 安装目录的 resources 文件夹下运行。")
        input("按任意键退出...")
        sys.exit(1)
        
    print(f"检测到软件资源路径：{resources_dir}")
    input("请确保软件已完全退出。按下【回车键】开始注入...")

    # 清理进程并安装依赖
    terminate_processes()
    ensure_asarpy()

    # 汉化
    try:
        patch_asar(resources_dir)
        print("\n🎉 汉化成功！现在您可以重新启动 Antigravity 体验中文界面了。")
    except Exception as e:
        print(f"\n❌ 汉化过程中发生错误：{e}")
        print("建议运行 restore.py 恢复英文原版，或重新运行此脚本。")
        
    input("\n按回车键退出本窗口...")

if __name__ == "__main__":
    main()
