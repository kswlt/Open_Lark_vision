# RELEASE CHECKLIST — v1.0.0

## P0（必须全部完成才能发布）
- [x] 干净源码迁移（不带旧 .git）
- [x] PolyForm Noncommercial 1.0.0 LICENSE
- [x] COMMERCIAL_LICENSE.md / CLA.md
- [x] AUTH_MODE public|private + VIEWER/ADMIN token
- [x] 默认只读（FEISHU_*_SYNC_ENABLED=0）
- [x] 去 ADAM 运行时硬编码（team.yaml / /api/meta）
- [x] 赛季节点从 team.yaml 读取
- [x] Dockerfile node:22-alpine + compose volumes 修复
- [x] CI：frontend / backend(ubuntu+windows×py3.11/3.12) / docker / gitleaks / pip-audit / npm audit
- [x] Mock 默认无需飞书/相机即可启动
- [x] 安全回归测试 8 例 + 既有 49 tests 全绿

## P1
- [ ] CI 在 GitHub 上实际全绿（本仓库 owner 到 Actions 页面确认）
- [ ] 旧仓库 `kswlt/Lark_vision` 设为 private 或 archive
- [ ] 飞书侧检查曾暴露文档 token 的分享权限
- [ ] Settings → Branch protection：main 要求 PR + status checks
- [ ] Settings → Private vulnerability reporting 开启

## P2
- [ ] 真实华睿相机在 Windows 上回归验证（Linux 相机依赖厂商 SDK，不宣称）
- [ ] README 截图替换为 Mock 数据截图
- [ ] 真实 Windows / Ubuntu fresh clone 手工验证一次

## 发布
- 全部 P0 + P1 完成后：
  - 打 tag `v1.0.0`
  - 写 GitHub Release
  - **不自动执行，等待维护者确认**
