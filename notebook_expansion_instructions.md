# Notebook Expansion: Bonus Exercises

Reusable instructions for adding **two extra "bonus" exercises** to a chapter notebook
in this project. Hand this file to the assistant with a target notebook (e.g. *"Apply
`notebook_expansion_instructions.md` to `6_Community_Detection.ipynb`"*).

This adds *only* the two bonus exercises — it does not restructure the chapter or touch
its existing in-class "Your turn" exercises or its homework.

---

## 0. Why — the goal

A lesson sometimes runs **short**: the planned material finishes and there is still
class time on the clock. Rather than dismiss students early, you want a couple of
substantial problems on hand to keep the engaged ones working.

So: add **exactly two** bonus exercises that are each **slightly larger and more
open-ended than the chapter's in-class meaty "Your turn"** (~10 min) — aim **~15–25
minutes** apiece. They are **optional buffer material**, clearly marked as such, so no
student feels they missed required content.

---

## 1. Where they go

- Insert a short section **after `## Summary` and *before* the
  `## Chapter N — … · Homework`** section. (The bonuses are warm, in-class extensions;
  the homework stays the formal take-home.)
- Section header, then two subsections — make the **bonus** status unmistakable:
  ```markdown
  ## 🌶️ Bonus exercises (only if time remains)

  These are optional extensions for the end of class — pick whichever looks fun.

  ### 🌶️ Bonus 1 — <one-line task>
  ...
  ### 🌶️ Bonus 2 — <one-line task>
  ```
  (The 🌶️ "spicy" marker is a suggestion — anything that visibly reads *bonus /
  optional* works, as long as it's distinct from the 🖐️ used by the in-class
  exercises. Keep the *"only if time remains"* qualifier.)
- **Do not** modify the existing "Your turn" exercises or the homework — these are
  purely additional.

---

## 2. What makes a good bonus exercise

- **Bigger than the in-class meaty one.** Combine **two or more ideas** from the
  chapter, or push a single idea further — a small **parameter sweep**, an **A-vs-B
  comparison with a verdict**, a **mini-investigation**, or **apply the method to a
  new slice of data**.
- **Open-ended, with a concrete goal and a deliverable.** Frame it as a question to
  *answer* — "find X and explain why", "compare A and B and decide which wins" — not a
  one-line fill-in. Ask for a sentence of interpretation.
- **Extend, don't repeat.** It should feel like *the next question a curious student
  would ask* after the lesson — distinct from both the in-class exercises and the
  homework parts.
- **Self-contained and fast.** Reuse the data, variables, and helpers the chapter
  already loaded; no new heavy downloads, nothing that takes minutes to compute. A
  quick student should finish inside the lesson.
- **Make the two differ in kind.** Pair, say, one **quantitative** exercise (sweep /
  measure / compare) with one **interpretive or visual** one (read a result, apply to
  new data, draw and explain). Order them **easier → harder** so a student who only
  reaches the first still gets value.

---

## 3. Shape of each bonus (matches the chapter's meaty exercises)

Two cells per bonus:

1. A `### 🌶️ Bonus N — …` **markdown** heading + 1–3 sentences framing the task and the
   expected deliverable.
2. A **starter code cell that executes cleanly as shipped** but leaves the work undone:
   - any **setup** lines (so the cell runs), then
   - a `# TODO` that **describes the task in words** — *never* the commented-out
     solution — plus a one-line hint or the expected shape of the answer.

Then, because each bonus is meaty, a **collapsible solution** in the *next* markdown
cell so a self-study reader can check themselves:

````markdown
<details><summary>Solution</summary>

```python
...solution code...
```

One or two sentences interpreting the result, citing the real number you got.
</details>
````

**Run the solution yourself first** and put the actual figure into the interpretation
(e.g. "AUC climbs from 0.81 to 0.88"), so the answer key is correct, not guessed.

---

## 4. Two short templates (adapt to the chapter)

*Quantitative sweep / comparison:*
> **🌶️ Bonus 1 — How far can you push it?** Re-run the chapter's main method across a
> range of one parameter, collect the headline metric for each, and plot metric vs.
> parameter. Where is the sweet spot, and what breaks past it? Answer in a sentence.

*Apply to new data / interpret:*
> **🌶️ Bonus 2 — Does it hold on a different graph?** Take the method to a second
> dataset the book has already used, run it, and compare the result with what you saw
> in this chapter. What's the same, what's different, and why?

---

## 5. Verification

- The starter cells must keep the notebook running **top-to-bottom with zero errors**
  (they're scaffold/comment cells — execute the whole notebook to confirm).
- Solution code lives inside `<details>` markdown, so it is **not executed** by the
  notebook — but you still run it once yourself to get the real numbers.
- Validate the notebook JSON, ship the executed copy, and rely on git as the safety
  net (the pre-edit state should be committed before you start).

---

## 6. Definition of done

- [ ] Exactly **two** bonus exercises, in a clearly-labelled bonus section placed
      **between Summary and Homework**.
- [ ] Each is **larger / more open-ended** than the in-class meaty "Your turn", and the
      two **differ in kind** (not two takes on the same task).
- [ ] Each has a **runnable descriptive scaffold** (no commented-out solution) **and** a
      **collapsible `<details>` solution** whose interpretation cites a real number.
- [ ] Self-contained: reuses existing data/helpers, fast to run.
- [ ] Notebook still executes top-to-bottom with **zero errors**; JSON validates.
- [ ] Existing in-class exercises and homework left **untouched**.
