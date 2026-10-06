with open("/opt/side/bravesoul-game/web/js/awwwards.js", "r", encoding="utf-8") as f:
    content = f.read()

target = "setTension(0, false);"
replacement = """setTension(0, false);

    // Automation helpers for testing & QA verification
    window.testWindFull = function () {
      setTension(MAX_TENSION, true);
    };
    window.testRelease = function () {
      releaseKey();
    };"""

if target in content and "window.testWindFull" not in content:
    content = content.replace(target, replacement, 1)
    with open("/opt/side/bravesoul-game/web/js/awwwards.js", "w", encoding="utf-8") as f:
        f.write(content)
    print("Injected testWindFull successfully!")
else:
    print("Already injected or target not found")
