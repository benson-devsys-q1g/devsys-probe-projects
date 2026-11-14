# DEVSYS-D3 local phase verification (LOCAL_ARTIFACT_ONLY, NOT_GIT_BACKED)

Task: DEVSYS-D3 local phase. Repo: benson-devsys-q1g/devsys-probe-projects (1452898408). Base (main): c95b4a0ae569c313690881880d01c3e57bec55f0. Intended ref: claude/d3-personal-profile-reference (absent at preflight). Source: DEVSYS_D2_Project_Instructions_v0.2.0.md, 10403 bytes, SHA-256 2e63b048d9acd04a40f0de8257c7dcfd868606dad1f278648e321b61cab2c3c9.

## Preflight (executed by writer, read-only)
- Attachment byte-preserving file: wc -c = 10403, sha256 matches approved value.
- Session environment_id (get_session): env_01Fk1cCTD3qJpds7NiKqZS8T (matches expected native ID). Display name devsys-v1-candidate was owner-verified earlier; not independently observed by writer.
- GitHub identity (get_me): bensonmcmoran (17336723).
- git ls-remote: main = c95b4a0ae569c313690881880d01c3e57bec55f0; refs/heads/claude/d3-personal-profile-reference absent; only other remote branch claude/fv1-2-20261111 (d7891ca).
- reference-maintenance/ absent at base (tree: .github/workflows/verify.yml, CLAUDE.md, README.md).
- Secret/credential scan of source: no matches. A first case-insensitive scan hit only the substring "sk-" inside "risk-proportionate"/"task-authorized" (false positives); final scan uses case-sensitive, anchored patterns.
- Content note: source names the public synthetic repo, its numeric ID and its owner-account login context; it contains no credentials, no cross-project data. Accepted as in-scope by writer; reviewer to confirm.
- Not observable by writer: other active workers (coordinator-side), repository permission level beyond read calls, environment display name.

## Tests executed (writer run, scratch dir; results.txt is the raw log)
| ID | Test | Result |
|---|---|---|
| T1 | copy sha256 == approved | PASS |
| T2 | cmp byte-identical to source | PASS |
| T3 | length 10403 | PASS |
| T4 | no CR bytes (LF only) | PASS |
| T5 | valid UTF-8 | PASS |
| N1 | one-byte mutation changes hash (detected) | PASS |
| N2 | appended trailing newline changes hash (detected) | PASS |
| N3 | CRLF conversion detected by CR check and hash | PASS |
| N4 | truncation detected by length and hash | PASS |
| N5 | secret scanner flags planted fake token (control) | PASS |
| T6 | secret scan on source: no matches (case-sensitive patterns) | PASS |
| T7 | no URLs or email addresses in source | PASS |

Negative controls N1-N5 operated on copies under neg/ (mutated copies kept as evidence). N5 proves the scanner can detect a planted fake token, so the T6 clean result is discriminating.

## Planned but not executed
- Reviewer independent re-hash and re-scan (reviewer phase).
- Post-assembly checks (JSON validity, manifest hash cross-check, total size under 32768 bytes) are run after this file is finalized and reported by the writer outside this file, since this file cannot contain its own hash.

## Limits
- No Git commit, push, PR, or remote write performed. Files are local scratch only; not available to a fresh session unless the reviewer shares the same filesystem (unverified).
