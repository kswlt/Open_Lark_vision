# RM CONTROL (Open_Lark_vision) 交接文档

> 面向下一位接手维护者 / 部署者。读完这份就能独立跑起来、改配置、发版。

---

## 1. 项目是什么

**RM CONTROL** —— RoboMaster 战队实验室大屏 Dashboard。

- 数据：飞书多维表格（任务）、飞书考勤/工时表、飞书通讯录头像
- 前端：React + TypeScript + Vite + Tailwind（产物 build 到仓库根 `dist/`）
- 后端：Python Flask + Waitress（`backend/app.py`，单文件入口）
- 可选：工业相机 + YuNet + SFace 人脸签到（华睿 Huaray GenTL SDK）
- 默认 Mock 模式：clone 后不配飞书也能看到完整 Demo

仓库：`git@github.com:kswlt/Open_Lark_vision.git`（main 分支）
旧仓库：`kswlt/Lark_vision`（已废弃，建议转 private，见 `docs/SECURITY_MIGRATION.md`）

---

## 2. 目录结构

```
Open_Lark_vision/
├── backend/
│   ├── app.py                  # Flask 入口（路由 + 认证 + 静态站）
│   ├── config/
│   │   ├── team.example.yaml   # 队伍配置示例（组别/兵种/别名/优先级/赛季节点）
│   │   ├── team_config.py      # 读取 team.yaml，导出 TEAM_NAME/.../MILESTONES
│   │   └── featured_docs.py    # （gitignore）飞书文档白名单
│   ├── services/               # 数据聚合、飞书客户端、sources
│   ├── integrations/camera/    # 相机采集/识别/gallery（optional）
│   ├── tests/                  # pytest（49 用例，含 test_auth.py 8 例）
│   ├── requirements.txt         # 核心依赖
│   └── requirements-camera.txt # 相机可选依赖
├── frontend/
│   ├── src/
│   │   ├── pages/              # Dashboard / Tasks / Groups / Robots / People
│   │   ├── components/         # TopBar / Sidebar / CountdownRow / DocReader...
│   │   ├── api/client.ts       # fetch 封装
│   │   └── store.tsx           # 全局状态 + 定时刷新
│   └── package.json            # engines.node >= 22
├── dist/                       # vite build 输出（gitignore）
├── scripts/                    # start.ps1/sh、stop、setup、deploy.ps1
├── examples/deployment/        # dhcp_server.py、systemd 示例
├── docs/                       # SECURITY_MIGRATION.md
├── .github/workflows/ci.yml    # CI
├── Dockerfile / compose.yaml  # 单容器部署
├── LICENSE                     # PolyForm Noncommercial 1.0.0
├── COMMERCIAL_LICENSE.md
├── CLA.md / NOTICE.md / SECURITY.md
├── README.md
├── RELEASE_CHECKLIST.md
└── OPEN_SOURCE_AUDIT.md
```

---

## 3. 关键配置文件

### 3.1 `backend/.env`（从 `.env.example` 复制）

| 变量 | 默认 | 说明 |
|---|---|---|
| `DATA_SOURCE` | `mock` | `mock` / `feishu` |
| `CAMERA_ENABLED` | `false` | 无相机保持 false |
| `AUTH_MODE` | `public` | `public` / `private`（feishu 强烈建议 private） |
| `VIEWER_TOKEN` | 空 | private 模式读数据用 |
| `ADMIN_TOKEN` | 空 | 管理写接口用 |
| `CAMERA_PUBLIC` | `false` | camera 接口是否免 token |
| `FEISHU_CHECKIN_SYNC_ENABLED` | `0` | 默认不写飞书 |
| `FEISHU_ATTENDANCE_SYNC_ENABLED` | `0` | 默认不写飞书 |
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | — | 飞书自建应用凭证 |
| `FEISHU_APP_TOKEN` / `FEISHU_TABLE_ID` | — | 多维表格 |
| `HOST` / `PORT` | `0.0.0.0` / `8080` | 监听 |

### 3.2 `backend/config/team.yaml`（从 `team.example.yaml` 复制）

队伍名称、组别、兵种、别名、优先级映射、赛季里程碑。
**其他战队 fork 后只改这一个文件 + .env 就能跑，不用改源码。**

---

## 4. 本地启动

### Windows
```powershell
cd Open_Lark_vision
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
Copy-Item backend\.env.example backend\.env
Copy-Item backend\config\team.example.yaml backend\config\team.yaml
cd frontend
npm ci --legacy-peer-deps
npm run build
cd ..
python backend\app.py
# 访问 http://localhost:8080
```

或一键：`.\scripts\setup.ps1` → `.\scripts\start.ps1`

### Ubuntu
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
cp backend/config/team.example.yaml backend/config/team.yaml
cd frontend && npm ci --legacy-peer-deps && npm run build && cd ..
python backend/app.py
```

或：`./scripts/setup.sh` → `./scripts/start.sh`

### Docker
```bash
docker compose up -d --build
# http://localhost:8080  （本机 8080 若被占，改 compose.yaml ports）
```

---

## 5. 认证模型

- `DATA_SOURCE=mock` → `AUTH_MODE=public` 默认放行，方便 clone 即看。
- `DATA_SOURCE=feishu` → 建议 `AUTH_MODE=private`，所有 `/api/tasks|dashboard|people|worktime|docs|duty|...` 需 `Authorization: Bearer <VIEWER_TOKEN>`。
- 管理写接口（`/api/admin/*`）永远要 `ADMIN_TOKEN`。
- camera 接口走 `require_camera`：`CAMERA_PUBLIC=true` 放行，否则走 viewer。
- MJPEG `<img>` 流不支持 header，用 `?token=` query（README 已提示 URL token 会进日志）。

---

## 6. 测试

```bash
# 后端
cd backend
python -m pytest -q          # 49 passed
ruff check app.py services config data camera_checkin.py camera_manager.py integrations tests
python -m compileall app.py services config data camera_checkin.py camera_manager.py integrations tests

# 前端
cd frontend
npm ci --legacy-peer-deps
npm run lint
npm run test
npm run build
```

CI（`.github/workflows/ci.yml`）：
- Frontend：ubuntu + node 22，lint/test/build/npm audit
- Backend：ubuntu + windows × py3.11/3.12，ruff/pytest/compileall/smoke（含 401/403/200 鉴权验证）
- Docker：build + compose up + curl health/tasks/dashboard/meta
- Secret scan：gitleaks

---

## 7. 已知 / 待人工处理

| 事项 | 位置 |
|---|---|
| 旧仓库 `kswlt/Lark_vision` 建议转 private / archive | `MANUAL_GITHUB_SETTINGS.md` |
| main 分支保护 + PR required + status checks | GitHub Settings → Branches |
| Private Vulnerability Reporting | GitHub Settings → Code security |
| 飞书文档 token 曾在旧历史暴露，建议复查分享权限 | `docs/SECURITY_MIGRATION.md` |
| 华睿相机 Linux 支持依赖厂商 GenTL SDK，未在 CI 验证 | README Camera 章节 |
| PolyForm 官方站点在本环境不可达，LICENSE 正文为手写标准文本，法律准确性建议人工复核 | LICENSE |

---

## 8. 发版流程（v1.0.0 之后）

1. 改 `backend/app.py` 顶部 `VERSION`、`frontend/package.json` version、`CHANGELOG.md`。
2. 跑完整测试 + CI 全绿。
3. 本地 docker compose 冒烟一遍。
4. `git tag vX.Y.Z && git push origin vX.Y.Z`
5. GitHub Releases 写 release notes。

**不要 force push、不要重写历史、不要删旧 commit。**

---

## 9. 许可证 & 商业授权

- 代码：**PolyForm Noncommercial License 1.0.0**（见 `LICENSE`）。
- 个人 / 高校 / RM 战队 / 非商业科研：免费使用、修改、分发。
- 商业用途（产品、SaaS、收费部署、有偿服务）：**必须单独联系 maintainer 拿商业授权**（见 `COMMERCIAL_LICENSE.md`）。
- 外部 PR 需同意 `CLA.md`（贡献者保留版权，授予 maintainer 再许可/商业授权权利）。
- RoboMaster® / DJI® 商标归权利人所有，见 `NOTICE.md`。
- 本项目是 **source-available**，不是 OSI Open Source。

---

## 10. 常用排错

| 症状 | 检查 |
|---|---|
| 启动报 `未找到队伍配置` | 复制 team.example.yaml → team.yaml |
| 页面 401 | .env 设了 AUTH_MODE=private 但没传 token，或 token 错 |
| `/api/camera/*` 401 | CAMERA_PUBLIC=false，需 viewer token；或 CAMERA_ENABLED=false 本就该这样 |
| Docker 起了但宿主访问 404 | 本机 8080 被别的进程占，改 compose.yaml ports |
| 前端 build 失败 | Node < 22，升级；`npm ci --legacy-peer-deps` |
| pytest 报飞书连接错误 | 确认 `DATA_SOURCE=mock`，且 conftest 清掉了 FEISHU_* 环境变量 |
| 页面显示 Adam | TopBar 默认已改 RM CONTROL；真实 team name 来自 /api/meta，查 team.yaml |

---

## 11. 当前状态（交接时点）

- main 最新 commit：`b6ff204` docs: record verified docker build + compose smoke test on Windows
- 本地 `pytest`：49 passed
- Docker 本机冒烟：health/tasks/dashboard/meta 全 200
- 未打 v1.0.0 tag，等 maintainer 确认
- 旧仓库未删除
