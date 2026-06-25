# Notebook Cleanup & Improvement Playbook

Reusable instructions for bringing any chapter notebook in this project up to the
standard set by `1_Introduction_to_Graphs_and_Networks.ipynb`,
`6_Community_Detection.ipynb`, and
`7_Introduction_to_Machine_Learning_on_Graphs.ipynb`. Hand this file to the
assistant together with the target notebook (e.g. *"Apply
`notebook_cleanup_instruction.md` to `2_Basic_Network_Properties.ipynb`"*).

**Run one notebook per clean chat, in reading order — not batched into one
conversation, and not concurrently.** Do the remaining chapters in sequence (2 → 3 →
4 → 5, then 9 → … → 15) so each can cross-reference the ones already cleaned. A single
chat can't hold the whole book at quality, and verification shares one kernel — so a
fresh chat per chapter is the workflow. Open each chat by pointing at the
already-cleaned neighbours as the reference (e.g. chapters 1, 6, 7), and commit each
chapter once its checklist is green (a clear message like `Restructure Chapter N …`)
to match the existing git history.

---

## 0. Keep the WHOLE BOOK in mind (read this first)

**A chapter is one link in a sequence, not a standalone document.** Before changing
anything:

1. **Skim every other notebook's section headings** (`1_*.ipynb` … `15_*.ipynb`) to
   learn what came before and what comes after. A quick way:
   ```bash
   for f in [0-9]*.ipynb; do
     echo "### $f"
     python3 -c "import json,sys; nb=json.load(open('$f'));
   [print(l) for c in nb['cells'] for l in ''.join(c['source']).split(chr(10))
    if l.lstrip().startswith('#') and not l.lstrip().startswith('#!')]"
   done
   ```
   Exclude `*BACKUP*` and `*_exec*` copies from this glob (there's a stray
   `9_..._BACKUP.ipynb`) — they pollute the heading skim and you can end up editing the
   wrong file. Resolve any backup or executed copy before touching that chapter.
2. **Respect the running order.** Do not teach a concept this chapter is supposed to
   *receive* from an earlier one, and do not duplicate something a later chapter
   owns. If the target is "Intro to GNNs", a GCN should be *motivated* here but
   *explained in depth* in its own later chapter — link forward instead of
   re-deriving (e.g. *"covered in depth in Chapter 10"*).
3. **Reuse names and datasets the book already established.** If earlier chapters
   built `G_college`, used Cora, or defined a helper, match those choices and call
   back to them ("the CollegeMsg graph from §6.3"). Cross-reference with `§x.y`.
4. **Match the house style** of the two reference notebooks (below), so a student
   moving between chapters feels one consistent voice.
5. When you finish, **state how this chapter connects** to its neighbors (a sentence
   in the intro pointing back, a sentence at the end pointing forward).

---

## 1. Target structure (what "good" looks like)

Use `1_Introduction_to_Graphs_and_Networks.ipynb`, `6_Community_Detection.ipynb`,
and `7_*.ipynb` as the gold standard — plus any later chapter already brought to this
standard. (Skip chapters still under active development as references.)

- **One H1 title:** `# Chapter N — <Title>`, followed by a short intro that states
  the chapter's **spine** — the single through-line question the chapter answers.
- **Numbered sections:** `## N.1 <Title Case Statement or Question>`,
  `## N.2 …`. Subsections use `### sentence-style` headings.
- **Each section follows a beat:** motivating prose → small/toy example → real
  example → an explicit **takeaway** (often a `>` blockquote).
- **Balance toy and real.** Introduce a mechanism on a tiny, controllable example,
  then show it on real data. (Ch. 6: toy modularity graph → CollegeMsg → Karate →
  email-Eu-core. Ch. 7: toy 3-tasks graph → Cora.)
- **An escalating arc**, not a list of disconnected demos. Ch. 6: *no structure →
  exact match → partial match*. Ch. 7: *structure → content → GCN*. Find the
  target chapter's natural escalation and make it the spine.
- **Sprinkle "Your turn" in-class exercises** through the chapter so students touch
  the code, not just read it. Mark each with a clear heading
  (`### 🖐️ Your turn: <one-line task>`) right after the concept it exercises.
  - **Several should be nearly trivial (1–4 min):** change a parameter and re-run,
    read a value off a plot, swap a node/threshold, predict the next line's output.
    These keep the room active and confirm the basics landed.
  - **At least one should be meatier (up to ~10 min):** combine two ideas from the
    section, write a short helper, or interpret a result and justify it in a
    sentence. Pose it as a small open-ended question, not a fill-in-the-blank.
  - Give each one a **starter cell that executes cleanly as shipped** but leaves the
    real work undone:
    - The `# TODO` **states the task in words** — *never* the commented-out solution.
      A `# TODO: <exact code>` a student only un-comments is not an exercise. Provide
      the setup line(s) and a one-line hint or the expected shape of the answer.
    - **Trivial** exercises end there — the answer is short enough to just do.
    - **Meaty** exercises additionally get a **collapsible solution** in the *next*
      markdown cell, so self-study readers can check themselves without it being in
      their face (renders collapsed in Jupyter/VS Code/nbviewer/GitHub):

      ````markdown
      <details><summary>Solution</summary>

      ```python
      ...solution code...
      ```

      One sentence interpreting the result.
      </details>
      ````
- **Close with `## Summary`** (bullets tying the arc together) and a
  **`## Chapter N — <Title> · Homework`** with `### Part A/B/C` (each part graded on
  a sentence or two of interpretation). **If the notebook has no homework, add one** —
  the homework is mandatory; build it from the chapter's spine so each part extends
  (not repeats) the in-class work.

## 2. Prose style

- **Intuition first, jargon second.** Lead with the idea in plain words, then name
  it. Define every term the first time it appears.
- **Bold the key term** on first use; use em-dashes for asides; keep paragraphs
  short.
- **Blockquote the one-line lesson** of a section: `> **Detectability is a property
  of the graph, not the algorithm.**`
- **Be honest.** Add explicit *caveats* where a result is illustrative rather than
  rigorous (e.g. "this is a benchmark built from X, not X itself"; "the jump mixes
  two changes at once"). Honesty is a feature, not a hedge.
- **Cite real numbers** produced by the notebook (AUCs, NMI, counts), not vague
  claims. Round sensibly and make sure the prose matches the executed output.

## 3. Things to actively remove / fix

- **Template boilerplate:** generic `#### Objectives / Code Examples /
  Observations & Explanations / Quiz / Key Concepts` scaffolding. Replace with real
  connective prose, or delete.
- **Stale copy-paste cruft:** dataset names that don't match the actual data
  (Ch. 7 still said "Brightkite" while using Cora), "the code above…" referring to
  code that isn't above, leftover headings with no content.
- **Jumbled order:** loading/setup dumped before the title; unnumbered sections;
  "Section 1/2/3" mixed with un-numbered `##`.
- **Thin cells:** code with no explanation, or three empty code cells in a row.
- **Redundancy:** two graphs/datasets where one will do (Ch. 7 dropped a confusing
  subset/full split and used a single giant component throughout).

## 4. Code hygiene (improve, don't gratuitously rewrite)

- **Keep working code working.** Prefer reordering + re-narrating over rewriting
  analysis. Only change code for clarity, reproducibility, or to remove confusion.
- **Reproducibility:** set `random_state` / `seed` on splits and models; `stratify`
  classification splits; `print` the headline metric (don't bury it only in a plot
  legend).
- **Small connective code is welcome:** a toy-graph illustration, a reusable helper
  (e.g. a single `plot_roc(curves, title, ax=None)`), a noise/random-feature
  baseline.
- **Comment density** should match the surrounding code and the reference notebooks
  (brief, purposeful `#` notes).
- **Generated assets, only when they earn their place.** If a chapter genuinely needs
  a hand-made diagram or a synthetic dataset, keep the generator in the repo (a small
  committed `<nb>_*.py` script) writing to `figures/` or a data dir, referenced by
  relative path — reproducible, not an orphaned binary. Don't add a generator for its
  own sake; reach for one only when an existing figure or dataset won't do the job.

## 5. Verification (do NOT skip)

A chapter is not done until it **executes top-to-bottom with no errors**.

1. **Find a kernel that has the chapter's dependencies.** Some notebooks need
   `torch` / `torch_geometric` / `seaborn`. Check the conda envs:
   ```bash
   for e in $(conda env list | awk 'NR>2{print $1}'); do
     py=$(conda run -n "$e" which python 2>/dev/null) || continue
     "$py" -c "import torch_geometric" 2>/dev/null && echo "$e has PyG"
   done
   ```
   In this project the **`sna`** env has the full stack (torch, torch_geometric,
   seaborn, sklearn, networkx, nbconvert). Register it once as a kernel:
   ```bash
   /Users/boris/miniconda3/envs/sna/bin/python -m ipykernel install --user \
     --name sna --display-name "Python (sna)"
   ```
2. **Execute end-to-end and inspect outputs:**
   ```bash
   /Users/boris/miniconda3/envs/sna/bin/python -m jupyter nbconvert \
     --to notebook --execute --ExecutePreprocessor.kernel_name=sna \
     --ExecutePreprocessor.timeout=320 \
     --output /tmp/<nb>_exec.ipynb "<nb>.ipynb"
   ```
   Then confirm figures rendered, no `error` outputs, and the printed numbers match
   the prose.
3. **Ship the executed copy** (with outputs) so the notebook opens complete, but
   **restore the original `kernelspec`** for portability:
   ```python
   nb["metadata"]["kernelspec"] = {"display_name": "sna", "language": "python", "name": "python3"}
   ```
4. **Validate JSON:** `import nbformat; nbformat.validate(nb)` before writing.
5. **Git is the safety net** — make sure the chapter's pre-edit state is committed (or
   stashed) before editing, so you can `git diff` and revert. No separate file copy.

## 6. Mechanics & gotchas (how to edit safely)

- **Edit the JSON directly with a small Python script** (load with `json`, rebuild
  cells, `nbformat.validate`, dump with `indent=1, ensure_ascii=False`). This is
  more reliable than hand-patching and avoids reading a multi-MB notebook into
  context.
- **Cell helpers:** store `source` as a list of lines each ending in `\n` (last line
  may have no trailing newline). Give markdown cells `{"cell_type":"markdown"}` and
  code cells `{"cell_type":"code","execution_count":None,"outputs":[]}` plus a short
  unique `id`.
- **Docstring trap:** if you build code-cell strings with `r"""…"""`, a `"""`
  docstring inside will terminate the string early. Delimit those cell strings with
  `r'''…'''` instead.
- **IDE save conflicts:** editing the `.ipynb` on disk while it's open in the IDE
  triggers a *"content is newer — Overwrite / Revert"* prompt. Tell the user to click
  **Revert** (load the assistant's on-disk version); **Overwrite** would clobber the
  on-disk edits. Better: have the user close the tab while edits happen, or pause
  disk edits while they review.
- **Markdown-only edits don't need re-execution**; code edits do.

## 7. Definition of done

- [ ] Read the rest of the book; chapter fits the sequence and cross-references it.
- [ ] Numbered sections, clear spine, toy+real balance, Summary + Homework.
- [ ] Several trivial (1–4 min) "Your turn" exercises plus one meatier (~10 min) one;
      homework present (added if it was missing).
- [ ] "Your turn" starters **describe** the task (no commented-out solution); trivial
      ones are runnable scaffolds, meaty ones have a collapsible `<details>` solution.
- [ ] Boilerplate, stale names, and jumbled order removed.
- [ ] Prose is intuition-first, honest, and cites real numbers.
- [ ] Executes top-to-bottom in a capable kernel with zero errors; figures render.
- [ ] Prose numbers match executed outputs; JSON validates.
- [ ] Pre-edit state was in git; chapter committed with a clear message
      (e.g. `Restructure Chapter N …`).
- [ ] Intro points back to the previous chapter; ending points forward to the next.
