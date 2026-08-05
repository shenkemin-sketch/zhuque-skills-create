# zhuque-skills-create

> 保留真正有用的方法，把重复工作流整理成精简、自然、可验证的 Codex Skill。

`zhuque-skills-create` 是朱雀 AI 的 Skill 创建与改造工具。它不会为了换品牌而清空一套已经有效的方法，而是先判断什么值得保留，再做适应性改造。

它分三层处理：

1. **价值层**：保留研究、意图澄清、触发边界、证据分级、测试和发布门禁。
2. **朱雀 AI 层**：改造项目身份、中文表达、决策收束方式和默认交付风格。
3. **法律层**：把必要的第三方声明隔离在法律文件中，不让它进入 Skill 的运行人格和品牌表达。

项目不会覆盖 Codex 内置的 `$skill-creator`。安装后使用独立名称调用：

```text
$zhuque-skills-create
```

## 安装

```bash
npx skills add shenkemin-sketch/zhuque-skills-create \
  --skill zhuque-skills-create --agent codex --yes
```

验证 Codex 安装入口：

```bash
test -f "${CODEX_HOME:-$HOME/.codex}/skills/zhuque-skills-create/SKILL.md"
```

## 你可以直接这样说

- “把这套重复工作流整理成一个 Codex Skill。”
- “先保留这个旧 Skill 里真正有用的能力，再改造成朱雀 AI 版本。”
- “审计这个 Skill 的触发边界和输出证据，先不要改文件。”
- “给这个 Skill 补齐测试、发布门禁和安装验证。”
- “把这个 Skill 作为开源项目发布，但不要直接推送默认分支。”

## 它会做什么

- 判断一次请求是否真的值得沉淀为 Skill。
- 改造旧 Skill 时先做 `keep / adapt / remove / add` 分类，避免把有用能力误删。
- 从工作流、Prompt、SOP、对话、文档、脚本或旧 Skill 提炼重复任务。
- 在重大改造时搜索同类 Skill，并记录 `keep / adapt / reject / invent`。
- 使用官方 `init_skill.py` 创建 Codex 原生目录。
- 生成并校验 `agents/openai.yaml`。
- 区分静态校验、真实前向测试、输出评测和人工证据。
- 对中文任务默认使用更自然、清楚、能直接执行的简体中文。
- 把发散想法收束成优先级、最小完整交付和一个明确下一步。
- 在明确授权后执行可选的 GitHub PR、Release 和安装验证。

## 生成的本地 Skill

默认只生成运行所需内容：

```text
skill-name/
├── SKILL.md
├── agents/openai.yaml
├── scripts/       # 按需
├── references/    # 按需
└── assets/        # 按需
```

README、Manifest、研究报告和发布素材不会被强制塞进每个本地 Skill；只有团队共享或公开发布时才按需添加。

## 前置条件

- [ ] 已安装 Codex，并确认当前版本可用。
- [ ] 已安装 Node.js 与 `npx`：`node --version && npx --version`。
- [ ] 已安装 Python 3：`python3 --version`。
- [ ] 若要发布到 GitHub，已安装并登录 GitHub CLI：`gh auth status`。
- [ ] 已阅读目标 Skill 可能执行的脚本、网络访问和外部写入边界。

## 本地验证

```bash
python3 scripts/quick_validate.py .
python3 scripts/validate_skill.py .
python3 scripts/trigger_eval.py . --cases evals/trigger_cases.json
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Troubleshooting

| 问题 | 常见原因 | 处理方式 |
|---|---|---|
| `No valid skills found` | `SKILL.md` frontmatter 无效 | 运行 `python3 scripts/quick_validate.py .` 并修复错误 |
| Codex 找不到 Skill | 安装目标或 Skill 名不一致 | 检查 `${CODEX_HOME:-$HOME/.codex}/skills/zhuque-skills-create` |
| `short_description must be 25-64 characters` | `agents/openai.yaml` 摘要长度不合规 | 调整 `interface.short_description` 后重新校验 |
| GitHub 发布被阻断 | 分支、版本、密钥或报告门禁未通过 | 先运行 `python3 scripts/publish_skill.py . --dry-run` |
| 触发评估通过但 Codex 没有自动调用 | 静态关键词评估不等于真实激活 | 用真实对话做前向测试，并把结果标为独立证据 |

## 安装前状态

当前仓库是独立本地项目。本阶段未自动安装到 Codex，也未创建或修改任何远程仓库。

## 来源与许可证

项目归属朱雀 AI。依法需要保留的方法来源、原始版权和第三方许可证统一记录在 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)，不会进入生成 Skill 的运行内容或产品品牌表达。

Upstream inspiration: See THIRD_PARTY_NOTICES.md.

## License

Copyright (c) 2026 朱雀 AI。项目主体采用 MIT；第三方文件继续适用其各自许可证。
