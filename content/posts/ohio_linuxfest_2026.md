+++
title = "Presenting at OLF! How it Went"
date = 2026-11-23T12:00:00Z
draft = false
tags = ["talks", "nix", "homelab", "radio", "ai"]
+++

I spoke at Ohio LinuxFest on Saturday, and I expected 5 to 10 people. About 55 showed up. The talk was "One Config, Any Machine," about managing your dotfiles and your whole machine from git, with Stow and NixOS. It's the story from [my flake post](/posts/nixos_flakes_dotfiles_one_command/), and I think it's the best presentation I've put together.

### The room

My room was a lot smaller than the main conference space. You took an elevator up, walked down a couple of halls, and hoped you'd read the signs right. It was not a place you'd stumble into.

The talk right before mine was on hardening agentic processes with AI, and a lot of people wanted to see it. It was in my room. When it ended there wasn't a better place for them to go, so they stayed. Every seat was taken, people stood along the back, and some stood in the hall. That's several times my usual audience.

I'd love to say they came for the NixOS, but it was the schedule.

### The talk

It starts with a laptop at 15.6 of 16 GB of RAM, because at my new job I was running Teams, Outlook, Chrome and VS Code on Windows. That's how I ended up in Neovim, and from there to a dotfiles setup I never pushed anywhere. Then comes the day I deleted it. I thought `rm -r` on a symlink only removed the link, and the trailing slash made it follow the link and delete my real files. I stopped on that slide and let the room read it. Plenty of people in there had typed the same command.

From there I went through why you'd want a declarative setup, where you describe the end state and the tool works out the steps, and then six ways people handle it today. The last one is mine: git for history, Stow to link the dotfiles into place, NixOS for the whole machine. The point I cared about most is that you don't need all three. Git alone takes about 15 minutes and pays for itself.

I got a lot of laughs and had a lot of fun. The biggest thing I'd change is the deck, which was words and diagrams with no real photos or screenshots. The other is rehearsal, because I didn't do enough of it. It's a big confidence boost for the next one.

### After the talk

I'd known someone in my area loosely for a while, and I finally had a real conversation with them in a quiet prep room. They're into radio, and we covered radio, how to live more privately online, raising kids, and city versus farm. There's a radio enthusiast meetup near Polaris, and I plan to go to the next one.

I also learned about Meshtastic. It's a mesh network built from cheap radios, so people can message each other with no internet and no cell service. I'd only half understood it before. It got me more excited about radio and about my homelab at the same time.

All of it is pushing me to take my own data more seriously than I have so far. In the homelab, that means real backups of the family photos and videos. At home, it means finally getting Windows off my personal machines. On my phone, it's GrapheneOS on my Pixel 9. None of it is done yet.

### Projects since the last post

The [homelab](/posts/homelab_go_top/) hasn't moved. The repo is still a to-do list, plus a half-built Tailscale explainer page I haven't committed. Tailscale is first, now that the talk is behind me.

The [manga machine](/posts/wdu_11_02_2026/) did move in early November. I switched the writing step to Sonnet, tried training a LoRA (a small add-on model) for each character, and made every scene keep one shared record of its lighting, props and wardrobe. A panel that runs too long gets re-asked and then cut instead of killing the whole book. The first full baseline run still failed QA, with 20 of 50 pictures usable, so the pipeline got sturdier and the art didn't get better.

### Next

I'll put the slides here once I have somewhere to host them.
