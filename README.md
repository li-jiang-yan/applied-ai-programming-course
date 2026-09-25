# Applied AI Studio

A six-page, static course website built from the six supplied curriculum files. Module 1 is `index.html`; Modules 2–6 are `module-02.html` through `module-06.html`.

## Preview

Open `index.html` directly, or serve the workspace locally:

```powershell
python -m http.server 8000 --bind 127.0.0.1
```

Visit http://127.0.0.1:8000. No Node dependencies or build service are needed. Videos require internet access; local lecture text, diagrams, and code remain readable without it. The six pages are the course delivery artifact, not an enrollment/payment platform.

## Contents

Every module contains the original audience and prerequisites, verbatim learning objectives with lesson links, a two-day learning plan, original lecture text, an embedded YouTube video with a direct fallback link, illustrated lab steps with downloadable source, checks with answers, and a summary. Video bridge notes identify subjects that require the written material and lab. Twelve original SVG illustrations show lab data flows and diagnostic concepts; they are labelled illustrations, not product screenshots.

Each lab step links to an expandable worked solution. Every module's **Lab solutions** section includes reference-code links, expected behaviour, troubleshooting, and worked explanations for the lab and extension exercises. Illustrative outputs and metric examples are labelled separately from measured results. Learners can reveal answers individually; following a “Stuck?” link opens the corresponding answer automatically.

`labs.zip` contains the complete lab tree and fictional policy data. Each page embeds its scripts directly from the same source files during generation. The course offers small CPU-friendly exercises; fine-tuning can benefit from a GPU. Accounts and usage charges apply to optional hosted calls and deployment exercises. See `labs/README.md` for execution and validation limits.

## Maintain and rebuild

- Edit module teaching content in `content/module-XX.html`.
- Edit worked lab answers in `content/solutions-XX.html`.
- Edit runnable examples in `labs/`.
- Edit the layout, curriculum mapping, and diagram definitions in `build_site.py`.
- Edit shared appearance and interactions in `assets/style.css` and `assets/course.js`.
- Run `python build_site.py` to regenerate the six pages, SVGs, and ZIP.
- Run `python validate_site.py` to check local links, anchors, curriculum coverage, required sections, illustrations, video embeds, Python syntax, and offline lab behaviour.
- With the local server running, `python browser_check.py` checks desktop/mobile rendering and interactions using Playwright and Microsoft Edge. This optional check requires those tools installed.

The source curriculum and prompt remain unchanged. Deployment of this static site can use any static hosting service; publish the generated pages, assets, labs and ZIP together.

## Reference and validation policy

Technical references are linked beside the relevant teaching text. Official API/framework documentation and primary papers were consulted on 25 September 2026. YouTube IDs were found through search or official course embeds; playback permissions and captions can change and were not verified in a signed-in player. Older visual-tool videos are explicitly labelled as conceptual walkthroughs.

The lab dependency ranges are not a resolved, tested lockfile. Hosted APIs, visual-tool round trips, cloud deployment, and downloaded-model training require the learner's environment and were not executed during authoring. Record exact package versions after a successful classroom rehearsal. The included automated check verifies offline logic and site structure, not hosted model quality.

Authoring checks passed for all six pages on desktop and mobile widths, local images, saved completion state, the interactive retrieval slider, JavaScript syntax, Python syntax, local links/anchors, curriculum-objective presence, archive consistency, offline retrieval/agent examples, and the small review classifier's validation and threshold behaviour. External video network requests were excluded from browser smoke checks. Preview images are saved as `preview-desktop.png` and `preview-mobile.png`.
