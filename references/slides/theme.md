# Deck theme

Every talk gets a new theme. The [samples](../../samples/README.md) show the level and the techniques. Never copy a sample: take its ideas, write new values.

## Pick the occasion

Take the date of the talk. If a holiday the audience celebrates falls within about three weeks, theme the deck around it: New Year, Lunar New Year or Tsagan Sar, Nauryz, March 8, Cosmonautics Day, Halloween and so on. If several fit, take the nearest. If none fits, build a mood from the topic, as the blueprint and ember samples do. Ask the author when the venue or audience suggests another occasion.

## Study the samples

Open two or three samples close to the occasion. Read each `README.md` and `theme.css`, and look at `original-cover.png`. Note the techniques, the signature and the lessons.

## Write deck-theme.css

`scaffold.py` creates an empty `deck-theme.css` and loads it after the shared theme. Write it in this order:

1. Fonts. Get Google Fonts with `scripts/fetch_font.py "<Family>" <project> --weights 400..700` (a static family takes `400;600`). It saves Latin and Cyrillic files to `fonts/` and prints the `@font-face` rules. Copy another font into `fonts/` only if its license allows it.
2. Roles. Set the `--craft-*` roles on `:root, :root[data-theme="light"]`: surfaces, text, lines, the four accent roles, data series and fonts. One mode is enough, so both selectors get the same values.
3. Cover. The cover is the poster of the theme. Replace the stock red fill and diagonal lanes on `.s-cover`.
4. One signature. One element carries the identity: a brand face on the hero line, a gradient title, a sheet number. Everything else stays plain.
5. Decor. Put it in `.slide::before` and `.slide::after` with `z-index: -1` and `pointer-events: none`: a grid, stars, snow, an ornament frame, a garland.

Rules:

- Decor is paint, never text. Emoji snowflakes or extra DOM nodes with characters count as text, and the checks report them as overlapping content.
- Animate decor freely. The deck stops all motion on `M` and for a static run. Do not write `prefers-reduced-motion`: the check rejects it.
- A brand or display face is for the hero line only. Body text uses a readable face with Cyrillic.
- Accent text needs contrast 4.5 against the background. Gold or yellow on light paper fails, so use it for marks and frames.
- Raw colors are allowed in `deck-theme.css`. The shared theme stays untouched.
- Keep the content zone readable: decor at the edges or at low opacity behind text.

## Harold

A talk by the author closes with the `harold` layout: a Harold picture in the deck's theme, two meme lines, the byline and one QR code.

Generate a new picture for each deck. Each sample has a `harold-prompt.txt`. Build the new prompt the same way:

- subject: the Hide the Pain Harold meme character with his strained smile;
- setting and costume from the occasion;
- style and palette from the deck theme;
- composition: the face in the middle, calm bands at the top and bottom for the meme lines;
- no text, letters or captions in the picture;
- landscape, about 3:2, at least 1600 px wide.

The `drawbridge` plugin turns a short brief into a prompt for the chosen image model. Save the result as `media/harold.webp` and pass it as `HAROLD_IMAGE`. The meme lines are text in the deck language; Russian words are in [material in Russian](../russian.md).

## Check

Run `check_project.py <project> --full`. Then look at the cover, a dense slide and the Harold slide yourself: the checks measure contrast, not taste.
