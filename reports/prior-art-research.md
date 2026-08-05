# Prior-Art Research

Research date: 2026-08-05
Target: `zhuque-skills-create` 0.2.0

## Sources verified

| Source | Verified snapshot | Role in this project |
|---|---|---|
| Upstream meta-skill | release `v2.8.1`, commit `9d9eafe` | Method and release-discipline baseline |
| OpenAI Codex built-in `skill-creator` | Codex CLI `0.147.0-alpha.1.2`, matching `openai/codex` commit `2707dfc` | Canonical Codex package contract and helper scripts |
| Anthropic official `skill-creator` | Claude Code `2.1.216`, matching official plugin commit `87c11d` | Evaluation and evidence-boundary comparison |

Exact sources and licenses are recorded in `THIRD_PARTY_NOTICES.md`.

## Keep

- Repeated-work test before creating a Skill.
- Proportional Scaffold / Production / Library / Governed modes.
- Prior-art research with source verification and separate metrics.
- Trigger boundary cases, output evaluation, evidence labeling, secret scan, feature-branch publication, immutable releases, and clean-install verification.
- `keep / adapt / reject / invent` synthesis and concise creation handoff.

## Adapt

- Replace the cross-platform `agents/interface.yaml` contract with Codex-native `agents/openai.yaml`.
- Use OpenAI's current `init_skill.py`, `generate_openai_yaml.py`, `quick_validate.py`, and `openai_yaml.md` unchanged under Apache-2.0.
- Make `SKILL.md` the only mandatory runtime file; README, manifest, eval reports, and release artifacts belong only to authoring or distribution work.
- Route local installation and backup paths through `$CODEX_HOME`, defaulting to `~/.codex`.
- Describe heuristic trigger scoring as static lint, not actual Codex invocation evidence.

## Reject

- Personal profile, social links, QR assets, promotional copy, default personal copyright, and forced naming prefixes.
- Mandatory cross-platform adapter metadata for a Codex-targeted project.
- Automatic installation, remote creation, or publication without an explicit user request.
- Claims that local tests prove real activation, model output quality, adoption, or business results.

## Invent

No unrelated product surface was added. The only original layer is the 朱雀 AI adaptation policy and its regression guards.

## 朱雀 AI adaptation decision

- Preserve the upstream method where it improves repeatability, evidence quality, and release safety.
- Adapt project identity, Chinese communication, value-preserving migrations, decision convergence, and default ownership for 朱雀 AI.
- Keep legal lineage isolated in `LICENSE`, `licenses/`, and `THIRD_PARTY_NOTICES.md`; do not turn it into runtime identity.
- Do not add social accounts, QR codes, personal profiles, or marketing claims without supplied and verified 朱雀 AI source material.

## Missing evidence

- No live Codex activation study has been run yet.
- No provider-backed with-skill versus baseline output evaluation has been run yet.
- No GitHub publication, Release, or clean remote install has been authorized or attempted.
