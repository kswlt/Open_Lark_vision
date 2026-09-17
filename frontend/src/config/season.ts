export interface SeasonMilestone {
  id: string
  name: string
  date: string
  note?: string
}

// 赛季节点已移至 backend/config/team.yaml 的 milestones，
// 前端通过 /api/meta 读取，不再在源码中硬编码日期。
