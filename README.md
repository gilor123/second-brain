# Second Brain

Turn your documents and everyday work into a personal knowledge folder you can ask questions about.

## Start

1. Upload `second-brain-0.2.1.zip` through Claude's custom plugin upload option.
2. Start a file-capable task and say **“Set up my second brain”**, or run `/second-brain:setup`.
3. Choose your folder and add the documents or links you want it to learn from.
4. Try a question. Setup then connects your available work apps and tests the automatic tasks.

English is the default. Setup handles the collection settings and schedule times for you. It uses connected Slack activity, email, Zoom transcripts and accessible Claude work conversations; you can request narrower collection at any time. Installation alone does not access your accounts or start tasks.

Slack includes your sent messages, mentions and DMs where you participated, not every company channel. Email covers all accessible messages in the daily window except spam, trash and drafts, without relying on labels. Zoom includes all accessible transcripts. Claude conversations exclude the Second Brain's own automated runs and other pure-refresh logs. Drive is available for initial document import, not continuous mirroring.

Setup runs every scheduled task once to catch access prompts before finishing. If Claude needs your approval, follow its native prompt. If setup cannot run tasks for you, it will show the tasks to run from Scheduled and check their results afterward. Future permission changes can still require attention.

## Use your brain

Open a task with your brain folder available and ask your question. Add new documents to `raw/sources/` when you want the brain to learn more. Change or pause automatic tasks through Claude's Scheduled controls.

Your source documents stay in `raw/`, the knowledge built from them lives in `wiki/`, and `maintenance/` holds working files and recoverable copies. Setup resumes without replacing your documents or customizations. Existing explicit collection preferences are preserved.

## Availability

The plugin contains one setup skill, nine workflows and a Slack coverage helper. Slack needs Python 3. Connectors, full Claude conversation access and native scheduling depend on your Claude account and environment. No credentials or connector installers are bundled.

Version 0.2.1 has local package and instruction tests; the updated experience still needs a run in your Claude account. Setup checks real account access and keeps any remaining action clear. It never labels an unfinished or failed automatic task as working.

[Claude plugin help](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) · [Scheduled task help](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)

## Author and license

Created by [Gil Or](https://github.com/gilor123). Released under the [MIT License](LICENSE).
