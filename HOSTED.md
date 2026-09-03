# Hosted links

Every standalone page in this repository is published as a private Claude artifact.
Start at the index — it links to all of them:

**Index — https://claude.ai/code/artifact/497d6873-6def-42da-a3ce-cd72b901ac0e**

| Page | Link |
| --- | --- |
| `PRD-Endpoint-Central-Reports.md` | https://claude.ai/code/artifact/0e874034-4fc4-49c0-a70e-328406bbc8ef |
| `reports-home.html` | https://claude.ai/code/artifact/de75b4c5-0149-42b5-9639-fd27b6b6b6f9 |
| `reports-home-variations.html` | https://claude.ai/code/artifact/30905aaf-da28-4211-b9bd-d44e1a84ed6c |
| `reports-home-export.html` | https://claude.ai/code/artifact/bc698640-4070-41e8-bd76-a4bce3388eb1 |
| `reports-home-live-export.html` | https://claude.ai/code/artifact/06bcddcd-19d2-4a3c-b4b6-55d33b38334c |
| `reports-search-home.html` | https://claude.ai/code/artifact/b7ad0c4c-60ff-40cb-83a9-8ea0343fc019 |
| `reports-search-variations.html` | https://claude.ai/code/artifact/0456e5ee-9209-4f55-9f38-caca74b0be3c |
| `reports-search-variations-2.html` | https://claude.ai/code/artifact/f98ec113-5270-446c-a4ee-0f4a8b0cc618 |
| `reports-search-hub-export.html` | https://claude.ai/code/artifact/3b2e7f0c-adc3-4496-a5db-5fa3cd2564d6 |
| `reports-catalog-variations.html` | https://claude.ai/code/artifact/262a82ec-0771-4d6a-978c-1e9609a5e918 |
| `reports-dashboard.html` | https://claude.ai/code/artifact/79c93b9d-b541-4083-995b-2e94f8d7c95b |
| `reports-custom-revamp.html` | https://claude.ai/code/artifact/0a96e4fc-38fd-48dc-8c14-2506a9078a33 |
| `reports-module-revamp.html` | https://claude.ai/code/artifact/561880e4-2495-455a-b391-20efffb09bec |
| `settings-search-home.html` | https://claude.ai/code/artifact/acacb10b-c86b-4d75-a897-f9e1a54f3893 |
| `incidents-home.html` | https://claude.ai/code/artifact/299a27f0-ab85-4d5c-b38b-6cac8a157515 |
| `incident-edr-security.html` | https://claude.ai/code/artifact/3adc9913-54ab-4efb-b237-82eb84045461 |

The flow diagrams were published earlier and are linked from the index as well:
`agent-installation-flow.svg`, `agent-refresh-policy-flow.svg`, `ds-approval-flow.svg`,
`ds-replication-flow.svg`. The 26 `cluster-*.svg` icon studies are inlined in the index page.

## Notes

- Artifacts are private by default; share each page from its own share menu.
- `hosted-index.html` is the source of the index page. Republishing it to the same
  URL keeps the link stable.
- `hosted-prd.html` is the rendered PRD. Regenerate it after editing the markdown with
  `pip install markdown && python3 tools/build-prd-page.py`, then republish it to the
  same URL.
- The two `*-live-export.html` pages carried a full `<!doctype html>` wrapper. The
  hosted copies have that wrapper unwrapped (the artifact host supplies its own),
  with the original `data-theme` and `body` class re-applied by a small inline script.
  The repository files are unchanged.
