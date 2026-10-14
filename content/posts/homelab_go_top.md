+++
title = 'The Go-Top Becomes a Homelab'
date = 2026-10-14T12:30:00Z
draft = true
tags = ["homelab", "devops", "nix", "docker", "tailscale"]
+++

### The laptop

For years I carried a laptop covered in Golang stickers everywhere I went. The go-top. It was ancient, and it only kept working because I lived in Neovim on NixOS, which asks very little of a machine. It's finally out of the backpack, and instead of recycling it I'm turning it into a homelab.

This is the first post in what I expect to be a long series, and I should say up front that there's no finished system here. There's a first commit, a mostly empty repo, and a list of things I want to learn.

### Why bother

The big one is DevOps practice. I want to learn SSH, Tailscale, Docker, Kubernetes, GitOps, CI/CD, and Argo for real, by running them somewhere nothing important breaks. Reading about GitOps and being the guy whose cluster stopped syncing are two very different experiences.

The easy first goal is hosting my personal websites on hardware I own. After that, I'd like our family photos and videos to live somewhere I control, instead of only inside someone else's subscription.

The most ambitious one is an AI agent that isn't rented. I use agents every day, and I'd like one running on my own hardware, where I can see what it's doing, and where I'm not feeding someone else's prompt injections and policies into my own life. It'll be limited by what a very old laptop can run, and honestly that's fine. Starting small is half the point.

And last, I help organize DevOps events in my city, and "here's what I built, what broke, and what I'd do differently" makes a better talk than a tour of someone else's tools.

### The plan, loosely

I'm not writing a roadmap with dates. Roughly in order:

1. Get the machine reachable and boring. NixOS on the laptop, SSH keys, Docker installed. Docker is mid-install over SSH as I write this, which has already taught me something about working on a machine from a distance.
1. Tailscale before exposing anything. I'd much rather reach the lab privately from anywhere than open ports and think about it later.
1. A first containerized site, a personal website behind a reverse proxy.
1. Kubernetes, then GitOps, with the cluster's desired state in git and Argo reconciling it.
1. CI/CD that deploys to the lab, so a push builds, tests, and rolls out.
1. Photo and video storage, with a backup plan that doesn't assume the laptop survives.
1. A local agent, once whatever's underneath it is something I trust.

The timing is nice here. I just rebuilt my NixOS and dotfiles setup around flakes (I wrote about it in [the previous post](/posts/nixos_flakes_dotfiles_one_command/)), so the lab should be one more host in that flake. Pinned, checked by CI, rebuildable from scratch. It gets a named entry in a repo, and when it breaks I can roll back.

### What I'm not sure about

Kubernetes on one old laptop is more machinery than a single node needs. I'm doing it because I want to learn it, and I'll say so here when I find out it was overkill.

Storage is the other worry. Family photos deserve better than "on the laptop," so I need to work out redundancy before I trust the lab with anything I can't replace. Security too. Running things at home makes me the entire security team, and Tailscale-first helps, but I want to understand what I'm exposing before I expose it. As for how capable a local agent can be on hardware this old, I have no idea yet.

### Next

Probably getting SSH and Tailscale into a state I trust, then the first containerized site, then the moment I decide whether k8s makes any sense here. If you run a homelab and have opinions on what I'm about to get wrong, I'd like to hear them.

<!-- TODO(jeff): no personal color yet. Say why the photos matter (kids? the second baby?), and what
the sticker laptop actually meant to you. Those are the sentences nobody else could have written. -->
