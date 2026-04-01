# Quickstart

## Goal

Get from zero to a usable `ID` starter profile in a few minutes.

## 1. Bootstrap A New Owner

```bash
make bootstrap-owner OWNER=<owner-id>
```

Optional alias:

```bash
make bootstrap-owner OWNER=<owner-id> OWNER_ALIAS=<owner-alias>
```

This creates:
- `profiles/<owner>/profile.minimal.md`
- `profiles/<owner>/handshake.md`
- `profiles/<owner>/privacy-policy.v1.json`

## 2. Fill The Minimal Profile

Edit:
- `profiles/<owner>/profile.minimal.md`

Keep it small:
- communication style
- task rules
- quality bar
- priority domains
- tool notes

## 3. Use The Handshake

Start a real task with:
- the minimal profile
- the handshake

The point is to test the profile in live work, not perfect it in isolation.

## 4. Validate The Repo

```bash
make validate
```

This checks:
- profile structure
- profile quality linting
- observed behavior evidence
- privacy policy
- generated artifacts
- benchmark/public metrics artifacts

## 5. Grow Only After Real Use

Recommended upgrade path:
1. start with `profile.minimal.md`
2. promote stable guidance into `profile.core.md`
3. add `profile.extended.md` only after repeated patterns are clear
4. use exports only when portability is needed

## 6. First Useful Commands

```bash
make bootstrap-owner OWNER=<owner-id>
make validate
make interop
make compact
make mcp
```
