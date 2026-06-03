# Antigravity 2.0 一键汉化注入工具 (Chinese Localization Patch)

这是一个专为 Google Antigravity 2.0 客户端（Agent Manager）打造的跨平台全自动一键汉化注入工具。

项目使用 Python 实现，不直接修改软件二进制文件，而是通过动态解包、代码注入及重打包技术，安全地为客户端注入中文化的 DOM 拦截翻译引擎。

---

## ✨ 项目特性

- **跨平台自适应**：支持 Windows、macOS 以及 Linux/Ubuntu，能够自动识别系统平台和安装路径。
- **动态 DOM 拦截汉化**：使用前端 `MutationObserver` 机制实时检测 DOM 更新，实现毫秒级翻译且无性能损耗。
- **免二次翻译与输入拦截**：自动拦截 `INPUT`、`TEXTAREA`、富文本编辑区域（`contenteditable="true"`）以及代码编辑器（如 Monaco Editor），**绝对不会**篡改您编写的任何代码和英文输入！
- **原生 UI 菜单汉化**：不仅能汉化窗口内网页，还可以对系统的原生顶部菜单栏（Menu）和系统托盘（Tray）进行深度翻译汉化。
- **确认框/权限窗口深度汉化**：完美支持对工具执行确认、命令运行授权等对话框中的操作选项（如：允许、拒绝、总是允许、终端命令等）进行深度汉化。
- **全自动依赖自愈**：脚本运行时会自动检测并安装 Python 依赖（如 `asarPy`），一键执行，无环境配置门槛。
- **安全备份与一键恢复**：汉化前会自动备份原版的英文 `app.asar` 为 `app.asar.bak`。随时可以通过卸载脚本一键回滚还原。

---

## 🚀 安装步骤

运行汉化脚本前，请确保您的电脑中已安装了 [Python 3](https://www.python.org/)。

### Windows 操作系统
1. 双击运行目录下的 **`双击运行汉化.bat`**。
2. 命令行窗口打开后，根据提示按下 **回车键 (Enter)**。
3. 脚本会自动强行清理残留的占用进程，并完成汉化注入。
4. 提示 **“汉化成功！”** 后即可重新启动软件。

### macOS / Linux 操作系统
1. 在终端（Terminal）中进入项目所在文件夹：
   ```bash
   cd /path/to/antigravity-chinese
   ```
2. 运行安装脚本：
   ```bash
   python install.py
   ```
3. 根据提示按下回车确认，等待脚本执行完成。
4. 重新启动软件即可。

---

## ↩️ 卸载与还原英文原版

如果在使用中遇到任何异常，或者想要恢复英文，可以使用还原脚本：

- **Windows 用户**：双击运行 **`双击还原英文.bat`**。
- **Mac/Linux 用户**：终端运行 `python restore.py`。

或者您也可以手动恢复：进入 Antigravity 安装目录下的 `resources` 文件夹，删除被汉化的 `app.asar`，然后将备份的 `app.asar.bak` 重命名回 `app.asar` 即可。

---

## 🛠️ 技术原理

本工具的原理是通过 python `asarPy` 库解包客户端的 `app.asar` 包：
1. 向 `dist/preload.js`（核心预加载逻辑）与 `dist/ideInstall/wizardPreload.js`（向导预加载逻辑）中注入前端 `DOM_TRANSLATOR` 引擎，实现无感知的 DOM 动态文本翻译替换。
2. 对 `dist/menu.js`（应用菜单）与 `dist/tray.js`（托盘）注入原生包装映射，在主进程底层直接替换文字内容。
3. 最后使用 `asarPy` 将其重新封装回 `app.asar` 覆盖原包。

---

## 📄 开源协议

本项目基于 **[MIT License](LICENSE)** 协议开源。
