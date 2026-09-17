# OPEN_SOURCE_AUDIT — Open_Lark_vision v1.0.0

> 本项目为 **source-available**（源码公开），不是 OSI Open Source。
> 许可证：PolyForm Noncommercial 1.0.0 + 单独商业授权。

## 1. Repository migration
- 旧 `kswlt/Lark_vision` 仅作源码快照；新仓库 `kswlt/Open_Lark_vision` 全新 `git init`，
  不带旧 .git 历史、不 cherry-pick、不 push mirror。
- 复制时排除 `.env`、`team.yaml`、`featured_docs.py`、`all_docs_content.json`、
  `team_roster.json`、`face_library/`、`node_modules`、`.venv`、`dist`、`logs`、`*.exe` 等。

## 2. Git history status
- 新仓库从 first commit 开始，无旧仓库 SHA。
- remote 仅 `git@github.com:kswlt/Open_Lark_vision.git`。

## 3. Secret scan
- 仓库内无硬编码 `FEISHU_APP_SECRET` / token / 私钥；仅变量名引用和 `.example` 占位。
- CI 接入 `gitleaks/gitleaks-action@v2`。

## 4. Historical exposure remediation
- `docs/SECURITY_MIGRATION.md` 记录旧仓库历史曾暴露的文件类型；
  建议旧仓库转 private、飞书侧检查文档 token 分享权限。
- 新工作树不含真实文档正文/人员名单。

## 5. License
- `LICENSE`：PolyForm Noncommercial License 1.0.0 标准正文。
- 非商业（个人/高校/RM 战队/科研）免费；商业需单独授权。

## 6. Commercial licensing
- `COMMERCIAL_LICENSE.md` 说明商业使用需联系 maintainer。

## 7. Contributor licensing
- `CLA.md`：贡献者保留版权，授予 maintainer 使用/修改/分发/再许可/商业许可权利。

## 8. Authentication
- `AUTH_MODE=public|private`；mock 默认 public，feishu 建议 private。
- `VIEWER_TOKEN` 读敏感数据；`ADMIN_TOKEN` 管理写接口。
- camera 接口走 `require_camera`（`CAMERA_PUBLIC` 开关），兼容 `?token=` MJPEG。
- 安全回归测试 8 例覆盖：public 放行 / private 401 / 错误 token 403 /
  viewer 可读 / admin 可读 / admin 写接口 401 / 未知 API 404。

## 9. Feishu permissions
- 文档接口严格白名单：`doc_id not in whitelist → 403`；
  `/api/docs/list` 只暴露配置允许的文档，不枚举应用可见文档。
- 默认 `FEISHU_CHECKIN_SYNC_ENABLED=0`、`FEISHU_ATTENDANCE_SYNC_ENABLED=0`，
  不主动写飞书。

## 10. Privacy
- 仓库不含真实成员姓名、排班、人脸照片、人脸模型、真实文档正文。
- Mock 数据使用虚构姓名。

## 11. Docker
- 单容器 multi-stage：node:22-alpine 构建前端 → python:3.12-slim 运行。
- 默认 `DATA_SOURCE=mock` / `CAMERA_ENABLED=false` / 非 root / healthcheck。
- compose.yaml 修复空 volumes 数组问题。
- **本机实测（Windows + Docker Desktop）**：
  - `docker build`：成功，前端 vite build 通过，镜像产出。
  - `docker compose up -d`：容器启动，waitress 监听 8080。
  - 容器内 `/api/health`：200，返回 `{"status":"ok","dataSource":"mock",...}`。
  - 宿主通过映射端口访问：`/api/health`、`/api/tasks`、`/api/dashboard`、`/api/meta` 全部 200。

## 12. Windows
- `scripts/setup.ps1` / `start.ps1` / `stop.ps1` 就绪。
- 路径全部 `pathlib`，无 `C:\Users\Admin` 硬编码。

## 13. Ubuntu
- `scripts/setup.sh` / `start.sh` / `stop.sh` 就绪；`examples/deployment/systemd/` 示例。

## 14. Node
- 统一 Node 22（Dockerfile / CI / package.json engines）。

## 15. Python
- CI 验证 3.11 / 3.12（ubuntu + windows）。
- Legacy Win7 / Python 3.8 作为 best-effort，不在 CI 矩阵。

## 16. Dependencies
- `requirements.txt` 核心；`requirements-camera.txt` 可选。
- CI 跑 `pip-audit` 和 `npm audit`（非阻塞 warning）。

## 17. Tests
- 本地 `pytest`：49 passed。
- 新增 `tests/test_auth.py` 8 例。

## 18. CI
- Frontend：lint / test / build / npm audit。
- Backend：ubuntu+windows × py3.11/3.12，ruff / pytest / compileall / smoke（含鉴权）。
- Docker：build + compose up + curl health/tasks/dashboard/meta。
- Secret scan：gitleaks。

## 19. Branding
- 运行时 UI 品牌从 `team.yaml` 读取，默认 `RM CONTROL`。
- 仓库 README 保留「Originally developed for ADAM RoboMaster Team」历史说明。

## 20. Trademark assets
- `NOTICE.md`：RoboMaster®/DJI® 商标归属说明，本项目与官方无隶属。

## 21. Documentation
- README 双平台 Quick Start、Docker、Legacy、License、Commercial、Contributing。
- `MANUAL_GITHUB_SETTINGS.md` 列网页端需手工配置项。

## 22. Remaining manual GitHub settings
见 `MANUAL_GITHUB_SETTINGS.md`：分支保护、Private Vulnerability Reporting、旧仓库归档。

## 23. Known limitations
- 华睿相机 Linux 支持依赖厂商 GenTL/CTI SDK，未在 CI 验证。
- 真实飞书凭证需用户自行在飞书开放平台创建应用并配置。
- polyformproject.org 在本构建环境网络不可达，LICENSE 正文为手写标准文本，
  法律准确性建议人工复核。

## 24. Release readiness

### P0 blockers
无。

### P1 blockers
- CI 在 GitHub 上的实际全绿需 owner 到 Actions 页面确认。
- 旧仓库转 private / 飞书文档 token 复查需人工执行。

### P2 improvements
- 真实 fresh-clone 双平台手工验证；截图替换为 Mock。

---

**结论：代码层面 READY FOR v1.0.0；发布动作（tag / Release / 旧仓库处理）等待维护者确认。**
