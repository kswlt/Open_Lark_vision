# Manual GitHub Settings（仓库所有者需在网页端操作）

以下设置无法通过 git push 完成，需在 GitHub 仓库 Settings 中手动开启。

## 1. Private Vulnerability Reporting
Settings → Code security and analysis → Private vulnerability reporting → Enable。
外部报告漏洞时不要在公开 Issue 中讨论。

## 2. 分支保护（main）
Settings → Branches → Add rule（或 Rulesets）：
- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass
- 选择当前 CI jobs：`Frontend`, `Backend (ruff / pytest / compileall / smoke)`, `Docker`, `Secret scan (gitleaks)`
- ✅ Require branches to be up to date before merging

## 3. 旧仓库处理
见 `docs/SECURITY_MIGRATION.md`：建议将旧仓库 `kswlt/Lark_vision` 设为 private 或 archive。

## 4. Secrets
本仓库 CI 不依赖任何 secret 即可运行（默认 Mock 模式）。
如启用 gitleaks 付费规则，需在 Settings → Secrets 配置 `GITLEAKS_LICENSE`。
