import subprocess
import json

script = """
const cast = document.getElementById('cast');
const rect = cast.getBoundingClientRect();
const cards = Array.from(document.querySelectorAll('.race-card')).map(c => {
    const r = c.getBoundingClientRect();
    const name = c.querySelector('.race-card__name')?.innerText;
    return { name, top: r.top + window.scrollY, bottom: r.bottom + window.scrollY, left: r.left, right: r.right };
});
console.log(JSON.stringify({ castTop: rect.top + window.scrollY, castBottom: rect.bottom + window.scrollY, cards }));
"""

# Let's inspect via node or python with a headless chrome evaluate or similar
