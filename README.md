# Paper Notes Blog

A lightweight Jekyll site for summarizing research papers and hosting the notes on GitHub Pages.

## Getting started

1. **Set the site URL.** Edit `_config.yml` and set `url` to your real domain (for example `https://yourname.github.io`). If the repo name is not `<username>.github.io`, set `baseurl` to `"/<repo>"`; otherwise leave it blank.
2. **Install Jekyll locally (optional).**
   ```bash
   gem install bundler
   bundle install
   bundle exec jekyll serve
   ```
   Then visit `http://localhost:4000` to preview changes.
3. **Publish.** Commit the `blog` directory into a GitHub repository and enable GitHub Pages (prefer the `main` branch or `gh-pages` branch with `/` as the site root).

## Create a new paper note

Use the scaffolding script to create a pre-filled Markdown file:

```bash
python scripts/new_post.py \
  --title "FlashAttention 2" \
  --paper-title "FlashAttention-2" \
  --authors "Tri Dao, Dan Fu, Chris Re" \
  --venue ICML \
  --year 2024 \
  --paper-link https://arxiv.org/abs/2307.08691 \
  --paper-pdf https://arxiv.org/pdf/2307.08691 \
  --paper-code https://github.com/Dao-AILab/flash-attention \
  --tags transformers, attention, efficiency
```

The script creates a file in `_posts/` named `YYYY-MM-DD-slug.md` with placeholders for takeaways and section headers. Update those sections with your notes before publishing.

If you prefer to write posts manually, copy `_posts/2025-10-30-attention-is-all-you-need.md` and adjust the front matter fields:

- `paper_title`
- `paper_authors`
- `paper_venue`
- `paper_year`
- `paper_link`, `paper_pdf`, `paper_code`
- `paper_tags` (YAML list)
- `read_time` (optional integer)

## Folder layout

```
blog/
|-- _config.yml             # Global site settings and navigation links
|-- _layouts/               # HTML templates shared by the site
|   |-- default.html        # Base layout with header and footer
|   `-- paper.html          # Paper-specific layout that surfaces metadata
|-- _posts/                 # Markdown posts named YYYY-MM-DD-title.md
|   `-- 2025-10-30-attention-is-all-you-need.md
|-- assets/css/style.css    # Custom styling
|-- scripts/new_post.py     # Helper script to scaffold new posts
|-- about.md                # About page
|-- index.html              # Homepage that lists recent notes
|-- Gemfile                 # Dependencies for local preview with GitHub Pages
`-- README.md               # This guide
```

## Customize the look

- Update colors or spacing in `assets/css/style.css`.
- Modify navigation links via the `nav_links` array in `_config.yml`.
- Add more sections to `paper.html` if you want per-post checklists (for example, replication status or dataset links).

## Deploying on GitHub Pages

1. Create a public repository (for example `paper-notes`).
2. Copy the contents of this `blog` directory into the root of that repository.
3. Push to GitHub and enable Pages under **Settings -> Pages**, choosing the `main` branch and `/ (root)` folder.
4. After Pages builds, your notes will be live at `https://<username>.github.io` (user/org site) or `https://<username>.github.io/<repo>` (project site), matching how you set `url` and `baseurl`.

## Next steps

- Add real posts as you read papers.
- Create tag archive pages if you need per-topic views.
- Automate publishing by adding a GitHub Actions workflow that runs `jekyll build` and deploys to Pages.
