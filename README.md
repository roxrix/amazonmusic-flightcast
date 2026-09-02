# Amazon Music × Flightcast creator deck

A private, static browser slide deck about the four Amazon Music marketing programmes available to selected Flightcast creators: the Times Square billboard, an Amazon Music app feature, an audio ad swap, and social ads paid for by Amazon.

## Files

- **`index.html`** is the rebuilt 12-slide, 16:9 browser presentation. It uses plain HTML, CSS, and JavaScript with no framework or build step.
- **`amazonmusic-flightcast-deck.pdf`** is the rebuilt 12-page, 16:9 static deck for sending or presenting offline.
- **`source-original.html`** preserves the original self-contained 8-page document exactly as the source for copy and image order.
- **`assets/images/`** contains the 22 source images referenced by the deck.
- **`assets/fonts/`** contains local Geist font files.
- **`onepager.pdf`** is the original 8-page A4 PDF for reference and emailing.
- **`scripts/verify_deck.py`** checks slide structure, required copy and links, asset references, navigation hooks, reduced motion, print support, and the no-em-dash rule.

## Preview and verify

Nothing needs to be built. Open `index.html` directly, or run a private local server:

```sh
npm run serve
```

Then visit `http://127.0.0.1:8080`. Do not bind the server to a public interface.

Run the content and structure checks after every change:

```sh
npm run verify
```

Navigation supports the visible previous and next buttons, Arrow keys, Page Up, Page Down, Home, End, and direct URLs such as `#slide-6`. The deck uses vertical scroll snapping and prints one 16:9 slide per page.

## Keep this repository private

The document contains material that is not ours to publish:

- Screenshots from Amazon's paid media deck, which is marked CONFIDENTIAL on every slide.
- Photographs of other people's shows: Hoda Kotb, Jon Stewart, Dax Shepard, Keke Palmer, Zach Sang, Malcolm Gladwell, Oprah Winfrey, Chrissy Teigen, and the hosts of Chicks in the Office and Watch What Crappens.
- The Amazon Music wordmark, used under our partnership rather than a public licence.

Clear the deck screenshots with Amazon before this goes to creators, and do not switch on GitHub Pages or any public hosting for it.

## Changing the deck

Edit `index.html` locally. Keep these rules:

- Every number in the document is sourced from Amazon's own text or from Rox's confirmation on how video reaches Amazon Music. Do not round or estimate.
- Preserve all substantive copy, outbound links, names, captions, and source images.
- No em dashes, per house style.
- After any change, check the last bullet of the longest list is still there: "A tagline, 40 characters or less", on the billboard requirements slide. It is the first thing to disappear if a slide overflows.
- Run `npm run verify` before sharing the files.
