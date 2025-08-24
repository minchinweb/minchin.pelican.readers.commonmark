---
Category: test
date: 2025-08-23 14:55
---

# Issue 2


The current rendering has *italics* and **bold** and `code` HTML tags on
individual lines, which breaks if followed by a **comma**, *etc*. resulting in
an extra space after formatted text.

One theory is this is only encounted when the Title has to be pulled from the
(Markdown) body's first `<h1>` tag.

Check the raw HTML for this one...
