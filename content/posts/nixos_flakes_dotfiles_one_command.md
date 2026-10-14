+++
title = 'Rebuilding My NixOS Machine With One Command'
date = 2026-10-14T12:00:00Z
draft = true
tags = ["nix", "nixos", "dotfiles", "devops"]
+++

I moved to a new machine recently and it went badly. A few things were missing, a few things were slightly different, and I spent more time trying to remember what I had configured than I did working. Which is a little embarrassing, since the entire sales pitch of NixOS is that this shouldn't happen. So I spent about a week making sure it doesn't happen again, and this is what came out of it.

### How I got here

My setup was 'declarative' if you squint. I had a `configuration.nix`, a dotfiles repo, and a whole lot of stuff living in my head. Nothing was pinned, so my config just said "give me nixpkgs," and nixpkgs moves. Two machines built a month apart were not the same machine. I also run NixOS on a native desktop and inside WSL, and the shared settings and the machine-specific ones were all tangled into one file. The dotfiles repo was a pile of symlinks I'd made by hand, which is fine right up until a real file is sitting where a link needs to go. And secrets, SSH keys, API keys, logins, lived outside all of it, so they were the part I had to rebuild by hand and the part I was most likely to forget.

### Flakes

I resisted flakes for a long time, mostly because I didn't get how the same Nix config could come out different on different machines. Once it clicked it was almost anticlimactic: it can't, as long as everything is pinned. `flake.lock` records the exact nixpkgs revision, so the same commit of my repo builds the same system today or next year. Each host is just a named entry in `flake.nix`, and `nixos-rebuild switch` picks the one matching the hostname.

The layout is intentionally boring:

```
flake.nix              inputs + one nixosConfigurations entry per host
flake.lock             pins nixpkgs, nixpkgs-unstable, nixos-wsl
modules/common.nix     every machine: packages, user, programs
modules/zsh.nix        shell
modules/desktop-hyprland.nix   native desktop only
hosts/<hostname>/      per-machine: bootloader or WSL settings, hardware
```

The one rule that made it pleasant is that every option gets defined in exactly one place. I had `time.timeZone` set in two modules, and changing one of them quietly broke the native host. Shared things go in `common.nix`, and only genuinely machine-specific things go under `hosts/`.

### Trimming the global system

I'd been installing every toolchain system-wide. Terraform, the cloud CLIs, clang, gdb, Zig, Postgres, all of it. I moved those into per-repo dev shells with direnv and nix-direnv, which dropped about 4 GiB off the global system, and now each repo declares what it needs:

```sh
nix flake init -t ~/nixos#devshell   # new repo
direnv allow
```

I also wrote a small script that tells me when each declared package was last used, by digging through shell history, agent transcripts, and config references. "Should I keep this?" used to be a feeling and now it's a lookup.

### Checks before I'm allowed to break things

This is the part I like most. A `check` script runs before any switch. It runs `nix flake check`, builds every host (including the one I'm not on), and does an `nvd diff` between the running system and the new build so I can see exactly what's about to change. `nixos-switch` wraps that: check, show the diff, ask y/N, then switch.

On top of that there's a pre-commit hook that runs `nixfmt` and refuses the commit if any host stops evaluating, CI that builds both hosts on every push, and a weekly job that opens a pull request bumping `flake.lock` with the `nvd` diff attached. Nothing changes on my machine unless I decide it does.

### Dotfiles

The dotfiles repo is GNU Stow underneath, with one big change. A `packages` manifest is the only list of what gets linked, and nothing ever runs `stow *`. Each line says whether a package is for a native machine, WSL, or both.

There are two scripts that go with it. `bootstrap.sh` is idempotent, and if a real file is in the way it lists every conflict up front instead of dying on the first one. `dot-doctor` tells me what's missing, what's stale, and which new config files in `~` aren't tracked yet, because the real danger with dotfiles is that they drift and you don't notice.

### Secrets

I didn't want to log into a dozen services every time I set up a machine. The dotfiles repo is private, so my first thought was to just keep secrets in there. I ended up encrypting them instead. They live in an age-encrypted bundle committed to the dotfiles repo, with one passphrase to unlock it. `secrets-backup` writes it, `bootstrap.sh` restores it, and `dot-doctor` complains if the bundle has gone stale. The nixos repo is public, so nothing secret goes in there at all.

### The new-machine path

Before, getting a new machine meant about ten steps and a lot of remembering. Now it's install NixOS (or NixOS-WSL), run one `install.sh` line, log in to GitHub once, type the secrets passphrase once, and wait for `dot-doctor: clean`.

The dotfiles repo even has a VM test that boots the desktop config, runs `bootstrap.sh` in an empty `$HOME`, and checks that `dot-doctor` finishes clean. It runs weekly, so whether I can still rebuild from scratch gets answered by a green check mark and not by me panicking on a Saturday.

### Summary

If you're starting out, pin everything first, flakes are worth it for the lock file alone. Test your new-machine path in CI, because a document in a repo rots and a failing job at least yells at you. Encrypt your secrets and automate the restore. And use dev shells instead of installing everything globally.

None of this is clever, it's a pile of small guarantees. Which is what I want out of a system I'm going to rebuild a lot more times.

<!-- TODO(jeff): this reads too frictionless for a week of work. Add one real thing that broke, e.g. the
time.timeZone mess (how long did it take to find?), or a stow conflict that bit you during testing. -->
