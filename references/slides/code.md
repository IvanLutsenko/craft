# Code on a slide

`code-highlight.js` highlights `<pre class="code" data-language="..." data-highlight-lines="2-3">`. Do not hand-write syntax `<span>`s. To move focus, add a next slide with new `data-highlight-lines`. For a typed command, use `.code-run` and list the command lines in `data-run-commands`.

Commands and listings people will copy go in a window: `<figure class="code-window">` with a `<figcaption class="code-window-bar"><i></i><i></i><i></i><span>Claude Code</span></figcaption>` over the `pre.code`. A long line wraps under itself instead of shrinking the font. Several windows stack in `.code-windows`; with `data-reveal-items="each"` on the deck they appear one per click.

Two versions of one thing (a bot thread and a human one, an old and a new config) use the `pair` layout: `.code-windows--pair`, the right window on the next click. Prose in a window goes in `<div class="window-text">` with paragraphs.
