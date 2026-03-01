# Tales of the Super Nintendo

A collection of very important websites about very important things — hockey legends, animated guys, and hidden easter eggs.

## Directory Structure

```
.
├── index.html                  # Main hub page (starfield, links to sub-sites)
├── anthony.html                # Hidden easter egg page (click the title 3x)
├── scalabrini-site/
│   ├── style.css               # Shared CSS for Celebrini pages
│   ├── index.html              # Celebrini main page
│   ├── les-ratages.html        # The 3 legendary missed chances
│   └── hommage.html            # Official tribute & awards
├── two-guys/
│   └── index.html              # Two animated SVG characters
└── README.md
```

## Sub-sites

- **Celebrini** — A humorous tribute (in Quebec French) to a hockey player who dominated the shots but couldn't score in the Canada vs USA final. Three pages covering his stats, his three legendary missed chances, and an official mock-tribute.
- **Two Guys!** — A fun animated page with two SVG characters bouncing, waving, and chatting with speech bubbles. Features confetti and clouds.
- **Anthony** — A hidden easter egg page (unlocked by clicking the main title 3 times) dedicated to the friend who introduced the creator to Claude.

## Technologies

- HTML5, CSS3 (no frameworks)
- Vanilla JavaScript (animations, easter egg, confetti)
- Inline SVG characters (Two Guys page)
- CSS animations & keyframes throughout
- GitHub Pages for hosting

## Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/<username>/talesofthesupernintendo.git
   ```
2. Open `index.html` in any browser — no build step or server required.

   Alternatively, use a local server:
   ```bash
   npx serve .
   ```

## Browser Support

- Chrome / Edge 90+
- Firefox 90+
- Safari 15+
- Mobile browsers (responsive design included)
- Respects `prefers-reduced-motion` for users who prefer reduced animations
