# Contributing

Thanks for helping improve the LAMPY TouchOSC templates. Every change follows the same path: **issue → agreement → pull request linked to the issue → review → merge**.

## 1. Open an issue first

Use one of the issue forms:

- **Bug report** – a control sends the wrong command, a label does not update, a layout problem on a specific device.
- **Feature request** – a new page or control, support for another LAMPY model, a design change.

Blank issues are disabled. Questions about the console itself belong to Showtec support (link in the issue chooser).

## 2. Wait for agreement

A maintainer adds a label (`bug`, `enhancement`, `accepted`) and confirms the change. Please don't open a pull request for work that has not been accepted, because two people editing the same `.tosc` file cannot be merged automatically.

## 3. Make the change

- Fork the repository and create a branch named after the issue: `<issue number>-<short-description>`.
- Edit the templates in the TouchOSC editor with the grid set to **8 px**.
- Keep both templates in sync when the change applies to both consoles.
- Use only OSC addresses documented in the LAMPY manual, or explain in the pull request where an undocumented address comes from.
- Don't save show-specific names in the labels that receive names from the console.

You can run the same validation as the CI locally:

```bash
python3 scripts/validate_tosc.py templates/*.tosc
```

## 4. Open the pull request

- Fill in the pull request template.
- Write `Closes #<issue number>` (or `Fixes` / `Resolves`) in the description. The *PR links an issue* check fails without it.
- Attach a screenshot of every changed page and say which console you tested on, if any.

## 5. Review and merge

The `main` branch is protected: changes only land through a reviewed pull request with passing checks. Merging closes the linked issue automatically.
