---
name: zhuque-skills-create
description: Research, create, improve, migrate, validate, and optionally publish Codex-native skills from workflows, prompts, transcripts, documents, SOPs, scripts, notes, or existing skills. Use when a reusable Codex skill should be created or materially updated, when useful mechanisms must be preserved during identity or workflow adaptation, when trigger and output boundaries need evaluation, or when a skill needs Codex metadata, release gates, or installation verification. Exclude one-off summaries, translations, ordinary documentation, non-skill package publishing, and requests that explicitly should not become a skill.
---

# 朱雀 AI Skills Create

Create lean, Codex-native skills with proportional research, evidence, release discipline, and a clear bias toward useful work over ceremony.

## Routing Rules

- Route by the frontmatter `description` before reading the body.
- Once selected, act as the single skill-authoring authority. Do not invoke another creator unless the user explicitly requests a comparison or this skill cannot complete the task.
- Keep audit, evaluation, and diagnosis requests read-only. Edit only for create, update, migrate, or package requests. Publish only after an explicit publish request.
- Reject one-off summaries, translations, explanations, and brainstorming as skill candidates unless a stable repeated workflow is demonstrated.
- Keep exactly one discoverable root `SKILL.md`. Name embedded examples `SKILL.example.md` and test fixtures `SKILL.fixture.md`.
- For migration or rebranding, classify existing parts as `keep`, `adapt`, `remove`, or `add` before editing. Never equate debranding with deleting useful mechanisms.
- Use the 朱雀 AI identity only for 朱雀 AI-owned or explicitly branded output. Do not inject social links, QR codes, profile assets, or naming prefixes without supplied source material.

## 朱雀 AI Adaptation

- Preserve what already works before changing names, tone, structure, or tooling.
- For Chinese users, default to concise Simplified Chinese with natural phrasing; retain English only for technical identifiers, commands, paths, and source names.
- Turn divergent ideas into a visible priority, the smallest complete deliverable, and one concrete next action without flattening the user's creativity.
- Apply the principle “用 AI 享受工作，降低内耗，快乐生活”: reduce repeated decisions and empty ceremony while keeping evidence, safety, and user control.
- Separate three layers: runtime behavior, project-facing 朱雀 AI identity, and legally required third-party lineage. Legal lineage must not become runtime branding.
- Keep publication, installation, account access, and other external mutations explicit-only.

## Codex-Native Contract

Generate skills with this structure:

```text
skill-name/
├── SKILL.md                 # required: name, description, instructions
├── agents/openai.yaml       # recommended Codex UI and invocation metadata
├── scripts/                 # optional deterministic helpers
├── references/              # optional on-demand guidance
└── assets/                  # optional output resources
```

- Keep generated `SKILL.md` focused and under 500 lines.
- Put trigger conditions in `description`; the body loads only after activation.
- Put long guidance in one-level `references/`, repeatable actions in `scripts/`, and output resources in `assets/`.
- Do not create README, manifest, reports, examples, or ceremonial directories for a local runtime skill unless the selected mode or publication target earns them.
- Read [OpenAI YAML](references/openai_yaml.md) before creating or updating `agents/openai.yaml`.
- Ask for the destination before initializing. Default to `$CODEX_HOME/skills`; when unset, use `~/.codex/skills`.

## Modes

- `Scaffold`: personal experiment; create the smallest useful runtime skill.
- `Production`: repeated team use; add clear boundaries, validation, and realistic cases.
- `Library`: shared infrastructure; add portability, ownership, review cadence, and durable evidence.
- `Governed`: public or high-trust work; add permission, rollback, secret, release, and public-claim gates.

Choose the lightest valid mode using [Operating Modes](references/operating-modes.md), [Gate Selection](references/gate-selection.md), and [QA Ladder](references/qa-ladder.md).

## Prior-Art Research

For a new skill or material redesign, research similar skills when it will change the design:

```bash
python3 scripts/research_prior_art.py "<query 1>" "<query 2>" \
  --summary --output <authoring-workspace>/prior-art-candidates.json
```

Use skills.sh, SkillsMP, and canonical GitHub source without installing candidate skills. Keep installation counts, repository stars, source authority, maintenance, security, and license evidence separate. Inspect relevant source before adoption.

Synthesize four buckets:

- `keep`: retain the mechanism in principle.
- `adapt`: change it for Codex, the user, or the risk level.
- `reject`: omit it with a concrete reason.
- `invent`: add an original mechanism tied to the output contract.

Record unavailable sources and unsupported claims as `missing evidence`. See [Prior-Art Research](references/prior-art-research.md).

## Creation Workflow

1. Decide whether the request represents a stable repeated job. If not, answer directly and create no skill.
2. For an existing Skill, inventory its useful mechanisms and classify them as `keep`, `adapt`, `remove`, or `add` before changing files.
3. Capture the recurring job, target users, real inputs, finished output, exclusions, permissions, existing assets, destination, brand scope, and publication intent.
4. Collect two or three realistic examples and at least one near-neighbor that should not trigger.
5. Choose the lightest valid mode.
6. Research prior art when the design is new, material, public, or high-risk; otherwise record why it is unnecessary.
7. Plan only the reusable scripts, references, and assets earned by the examples.
8. For a new skill, run the bundled Codex initializer:

```bash
python3 scripts/init_skill.py <skill-name> --path <destination> \
  --resources scripts,references \
  --interface display_name="<display name>" \
  --interface short_description="<25-64 character summary>" \
  --interface default_prompt="Use $<skill-name> to <example task>."
```

9. Replace all TODOs, remove unused placeholders and directories, and implement the smallest complete workflow.
10. Test every added script by running it. Test a representative sample only when many scripts are mechanically similar.
11. Run the official Codex quick validator and the extended project validator:

```bash
python3 scripts/quick_validate.py <skill-directory>
python3 scripts/validate_skill.py <skill-directory>
```

12. For Production or higher, add realistic should-trigger, should-not-trigger, and near-neighbor cases. Treat `trigger_eval.py` as static lint, not proof of real Codex activation.
13. Forward-test complex skills on realistic tasks with fresh context. Pass raw inputs and the skill, not the intended answer, diagnosis, or expected fix.
14. Add with-skill versus baseline output evaluation only when correctness, safety, persuasion, or repeatability justifies it.
15. Produce a concise handoff with preserved value, 朱雀 AI adaptations, reference skills studied, candidate-specific lessons, design advantages, validated advantages, hypotheses, and missing evidence.

## Evidence Rules

- Static validation proves package shape, not output quality.
- Recorded fixtures prove reproducibility, not provider-backed model performance.
- Static trigger lint proves description/case alignment, not real Codex invocation accuracy.
- Human blind review counts only when the reviewer, time, decision, rubric reason, and answer isolation are recorded.
- Preview, generated files, successful commands, PR creation, merge, Release, and clean installation are distinct states.

Use [Eval Playbook](references/eval-playbook.md), [Output Eval](references/output-eval-method.md), and [Review and Release Gates](references/review-release-gates.md).

## Publication

Publication is optional and outside normal local skill creation.

1. Start with a read-only audit:

```bash
python3 scripts/publish_skill.py <skill-directory> --dry-run
```

2. Run the full publisher only after explicit authorization. It may prepare repository documentation, create or reuse a GitHub repository, push a `codex/` feature branch, create and inspect a PR, merge, create a versioned Release, verify discovery, and perform an isolated install.
3. Never push directly to `main` or `master`, reuse a released version, publish secrets, or report completion before remote and install evidence exists.

Read [Publishing](references/publishing.md) before any external mutation.

## Output Contract

For a local runtime skill, return:

1. a working skill directory with one root `SKILL.md`
2. an aligned `agents/openai.yaml`
3. only the scripts, references, and assets needed by the workflow
4. validation results and any realistic test evidence
5. explicit missing evidence and permission boundaries

Keep research reports, temporary evaluation outputs, and comparison artifacts in a sibling authoring workspace unless the user explicitly wants them packaged. Add README, LICENSE, manifest, release reports, or public assets only for an authorized distribution project.

## Reference Map

- Design: [Skill Engineering Method](references/skill-engineering-method.md), [Intent Dialogue](references/intent-dialogue.md), [Resource Boundaries](references/resource-boundaries.md)
- Evidence: [Eval Playbook](references/eval-playbook.md), [Output Eval](references/output-eval-method.md), [Skill IR](references/skill-ir-method.md), [Governance](references/governance.md)
- Release: [Publishing](references/publishing.md), [Review and Release Gates](references/review-release-gates.md), [GitHub README](references/github-readme-playbook.md), [SkillOps](references/skillops-loop.md)
