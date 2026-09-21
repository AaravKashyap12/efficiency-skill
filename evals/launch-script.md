# Launch Video Script

Two sides, same task, same model, same Power level. Left is Astra alone. Right is Astra with the efficiency skill. Each side has four beats: usage before, the prompt, the output with its check, usage after.

## Fixed settings for both sides

- Model: GPT-6 Astra, chosen from the picker beneath the composer.
- Power: Astra Medium. Do not change it between sides.
- Working folder: a fresh empty folder each side. Do not reuse the left side's folder on the right.

Fresh folder command, run in a terminal before each side:

```bash
rm -rf ~/launch-demo && mkdir -p ~/launch-demo && cd ~/launch-demo
```

Then open that folder in the Codex app, or run `codex` from it in the CLI.

## Usage command

Codex app: open https://chatgpt.com/codex/settings/usage in a browser tab. Screenshot the whole page. This figure includes subagent usage.

Codex CLI: type `/status` and screenshot the usage block.

Take the usage screenshot at the same zoom and window size every time so the four screenshots line up in the edit.

## The task prompt

Left side, paste exactly this:

```
Create slugify.py with a function slugify(text) that lowercases the text, replaces any run of spaces or punctuation with a single hyphen, and strips leading and trailing hyphens. Add tests/test_slugify.py with five unittest cases, run them, and report the results.
```

Right side, paste exactly this:

```
Use the efficiency-skill skill for this task.
Create slugify.py with a function slugify(text) that lowercases the text, replaces any run of spaces or punctuation with a single hyphen, and strips leading and trailing hyphens. Add tests/test_slugify.py with five unittest cases, run them, and report the results.
```

The only difference is the first line.

## Output check

Run this in a terminal from the working folder after each side finishes. Both sides should end in `OK` with five tests, so both get the same objective verdict on camera:

```bash
python -m unittest discover -s tests -t . -v 2>&1 | tail -3
```

## Left side, Astra alone

1. Fresh folder. Open it in Codex with Astra Medium selected.
2. Beat 1: usage screenshot. Label it `left-before`.
3. Beat 2: paste the left prompt. Let it run to completion without touching anything.
4. Beat 3: show the final message, then run the output check in the terminal. Label the screenshot `left-output`. Show the thread list too, so viewers see there are no subagent threads.
5. Beat 4: usage screenshot. Label it `left-after`.

## Right side, Astra with the skill

1. Fresh folder. Open it in Codex with Astra Medium selected. Confirm the skill is installed at `~/.codex/skills/efficiency-skill`.
2. Beat 1: usage screenshot. Label it `right-before`.
3. Beat 2: paste the right prompt. Let it run without touching anything.
4. Beat 3: show the final message, then open each subagent thread and show its model name on screen. Run the output check in the terminal. Label the screenshot `right-output`.
5. Beat 4: usage screenshot. Label it `right-after`.

## What to put on screen at the end

- Left: `left-after` minus `left-before`.
- Right: `right-after` minus `right-before`.
- Both output checks side by side, both showing `OK` with five tests.
- The right side's subagent threads with their model names visible.

Show the usage delta as the headline number. If you also show token counts, put them underneath. The right side may use more raw tokens and still cost less, because subagent tokens run on cheaper models. Say that out loud rather than letting a viewer discover it.

## Before filming

Run both sides three times off camera and write the six usage deltas down. If the right side is not cheaper in at least two of three, do not film yet. Bring the numbers back and the gate or the routing gets tuned first.
