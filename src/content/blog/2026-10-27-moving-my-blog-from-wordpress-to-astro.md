---
title: "I let Claude move my blog from WordPress.com to Astro on GitHub Pages"
date: 2026-10-27T12:00:00+01:00
description: "The prompt I used, and how Claude moved my five-year-old WordPress.com blog to Astro on GitHub Pages in one morning: exporting the posts, keeping the old URLs, the deploy workflow and the DNS switch."
tags: ["GitHub", "GitHub Pages", "Astro"]
---
This blog sat untouched on WordPress.com from March 2021 until this morning. I was paying for a plan to host a site I wasn't updating, and I had a few hours before flying to GitHub Universe.

So I handed the whole job to [Claude](https://claude.ai). To be clear: **Claude did the work.** It audited the old site, built the new one, migrated the posts, wrote the deploy workflow, switched the DNS and drafted this post. My part was the starting prompt, a few decisions along the way (GitHub Pages, then Astro, what to share about me and what not), and reviewing screenshots before anything was pushed.

This is the prompt I started with, typos included:

> I have my website mohamedsahbi.com that is hosted in wordpress. It is outdated, I want to update the theme and stuff or moved to github pages. You are a pro. I have few hours before flying to San francisco for GitHub unvierse tomorrow and would love to have quick fix and refresh. Also you can visit my github profile github.com/mohamedsahbi. I want to create new blog posts and I can attach few scripts that are useful if you want to inspire for additional blog posts, no fiction, just my work.

After that, I mostly answered questions, uploaded the WordPress export, my LinkedIn profile and a photo, and said "push" when I liked what I saw. A handful of steps needed me, because they involve my accounts and settings (more on those below). Everything else was Claude.

![The project thread in Claude: a preview of this post on the left, the conversation with Claude on the right](/images/posts/website-move-claude-thread.jpg)
*Reviewing this post in the Claude app before it went live, in the lounge at London Heathrow while I waited for my flight.*

## 1. Get the content out

WordPress.com can export everything as a single XML file: **Tools → Export → Export all**. That gave me 15 published posts, the pages, and a list of 87 media attachments.

Claude converted each published post to Markdown with a short Python script using [`markdownify`](https://pypi.org/project/markdownify/). It strips the Gutenberg block comments (`<!-- wp:paragraph -->`), turns `[code]` shortcodes into fenced code blocks, and writes the title, date, tags and an excerpt into the front matter.

The automatic conversion wasn't perfect. Image credits ("Source: pixabay.com") ended up at the start of a few excerpts, so it cleaned those up afterwards.

## 2. Keep the old URLs

WordPress used `/YYYY/MM/DD/slug/` URLs, and those links are out there in old tweets and Stack Overflow answers. Every post file is named `YYYY-MM-DD-slug.md`, and a single Astro route rebuilds the old path from the file name:

```ts
// src/pages/[year]/[month]/[day]/[slug].astro
export async function getStaticPaths() {
  const posts = await getPosts();
  return posts.map((post) => {
    const { year, month, day, slug } = postPath(post);
    return { params: { year, month, day, slug }, props: { post } };
  });
}
```

The old `/posts/` page now redirects to `/blog/`. The RSS feed moved from `/feed/` to `/feed.xml`.

## 3. Pick a stack

Claude's first version used Jekyll, because it's what GitHub Pages builds by default. It worked, but I wanted something more modern, so it rebuilt the site with [Astro](https://astro.build): content collections for the posts, Shiki for code highlighting with light and dark themes, plus a sitemap and RSS. It's plain HTML and CSS, with no JavaScript shipped to the browser.

## 4. Deploy with GitHub Actions

A short workflow builds the site and deploys it to Pages on every push to `main`:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

## 5. Switch the domain

The domain is registered at WordPress.com, so DNS stays there. Through the WordPress.com connector, Claude replaced the default apex A records with GitHub Pages' four IPv4 and four IPv6 addresses, pointed `www` at `mohamedsahbi.github.io`, and I set the custom domain in the repository's Pages settings. Mail records stayed untouched.

## What I had to do myself

Claude can't sign in to my accounts or click through settings pages, so these steps were mine:

- **Create the repository** `mohamedsahbi.github.io` on GitHub.
- **Connect GitHub to Claude** and install the Claude GitHub App on that repository, so it could push.
- **Connect the WordPress.com connector**, which Claude used to read the site and update the DNS records.
- **Export the WordPress content** (Tools → Export) and upload the file, because Claude's environment couldn't reach WordPress.com directly.
- **In the repository's Pages settings:** switch the source to GitHub Actions, add `mohamedsahbi.com` as the custom domain, and tick **Enforce HTTPS** once the certificate was ready.
- **Turn off auto-renew** on the WordPress.com plan, while keeping the domain registration.
- **Create the gists** linked from my posts.

Each one took a minute or two. The rest was reviewing screenshots and answering questions.

## How long it took, and what it cost

- **About 30 minutes** from my first prompt to the new Astro site running on GitHub Pages.
- **About 50 minutes** until it was live on mohamedsahbi.com, with the DNS switched and two new posts published.
- **About 5 minutes** to move the 37 old images off WordPress later that morning, once I came back to it.

The usage report for the whole Claude session, including follow-up fixes later the same day, shows about **124,000 input and 131,000 output tokens**, plus **39 million cached tokens read**. Long agent sessions re-read the same context over and over, so the cache does most of the work. At API prices that adds up to roughly **$15**. I ran it on my **Claude Pro** subscription, so I didn't pay per token.

## What didn't go smoothly

- **`username.github.io` repositories go live on their own.** GitHub turns on Pages with the classic Jekyll build as soon as you push to that repository. Claude pushed a first draft before I'd reviewed it, and it was public on github.io right away. After that, the rule was screenshots first, push second. Set the Pages source to **GitHub Actions** before your first push if you want to stay in control.
- **Check the Node version.** The first deploy failed at the build step. The current Astro major needs Node 22.22 or newer, and the action Claude started with ran an older Node. Calling `setup-node` with Node 24 explicitly fixed it.
- **Two builds at once.** Until the Pages source is switched to Actions, the classic Jekyll build keeps running next to your workflow and fails on every push, because there's no Jekyll site anymore.
- **Images were the last thing to move.** Claude's environment couldn't reach WordPress.com, so it wrote a one-off GitHub Actions job that downloaded the 37 images from the old posts into the repository. Its first attempt used the wrong WordPress address, so the old images were broken for about an hour after the DNS switch.

## A confession

Moving this blog had been on my to-do list for years. Every time I looked into it, I found a reason to wait. DNS changes can take up to 72 hours, the posts had to be moved, the theme needed rebuilding... so it stayed on my desk.

Then, with a flight to catch, I wrote one prompt. Less than 30 minutes later, the first version of the new site was online. The first time I saw how steps 2 to 5 actually worked (the URL routing, the Astro setup, the deploy workflow and the DNS switch) was while reviewing the draft of this post. All I knew was that I'd picked the stack. 😃

I've been coding with AI since GitHub Copilot's technical preview in 2021, and this still blows my mind. A project I'd been putting off because of the hours it would take just... happened. What a time to be alive.

## What's next

The point of all this was to write again, and to share what I build. Next up: practical notes from running GitHub Copilot and Azure DevOps at enterprise scale, starting with [pulling Copilot usage metrics with a GitHub App](/2026/10/27/copilot-usage-metrics-with-a-github-app/) instead of a personal access token. I'm also open-sourcing what I build at work: a [GitHub Copilot enterprise usage metrics portal](https://github.com/MohamedSahbi/github-copilot-enterprise-usage-metrics) and an [AI toolkit](https://github.com/MohamedSahbi/ai-toolkit) of reusable skills and prompts.
