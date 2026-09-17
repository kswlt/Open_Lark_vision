# Security Migration Notice

> 本文档记录从旧仓库 `kswlt/Lark_vision` 迁移到 `kswlt/Open_Lark_vision` 时的历史敏感信息风险。

## 已识别的历史暴露

以下文件在旧仓库历史中曾包含真实数据（本仓库当前工作树已全部移除）：

| 类别 | 曾包含内容 | 风险等级 |
|---|---|---|
| `backend/config/featured_docs.py` | 真实飞书文档 token、文档标题 | 高 |
| `backend/config/all_docs_content.json` | 内部文档完整正文 | 高 |
| `backend/config/team_roster.json` | 真实成员姓名、排班 | 中 |
| 历史 commit | 上述文件的历次版本 | 高 |

## 建议处置（需人工执行）

1. **旧仓库 `kswlt/Lark_vision`**：
   - 如不再对外公开，建议在 GitHub Settings 中 **Change visibility → private**，或 Archive。
   - 本文档不会主动删除旧仓库。
2. **飞书文档 token**：
   - 曾出现在历史中的 doc token 建议在飞书侧检查分享权限，必要时撤回/重置。
3. **飞书应用 Secret**：
   - 如曾在历史 commit 中出现，应在飞书开放平台 **重置 App Secret**。
4. **新仓库**：
   - 已通过 `.gitignore` 排除 `.env`、`team.yaml`、`featured_docs.py` 等真实配置。
   - CI 已接入 gitleaks 扫描新增 secret。

## 重要提醒

**已经在公网历史中出现过的数据，仅靠新建仓库不能视为撤回。** 上述旧仓库和飞书侧的处置需由仓库所有者人工完成。
