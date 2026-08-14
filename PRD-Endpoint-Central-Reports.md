# Product Requirements Document
## Endpoint Central — Reports Module

| Field | Value |
|---|---|
| **Product** | ManageEngine Endpoint Central — Reports & Dashboards |
| **Document type** | PRD (reverse-engineered from working prototype) |
| **Source artifact** | `index 4.html` — single-file React SPA build, 470 KB, all assets inlined |
| **Prototype date context** | Seed data uses Aug 2026 timestamps; "today" in-prototype ≈ Aug 1–5, 2026 |
| **Status** | Draft — for review |
| **Author** | Derived from prototype analysis |
| **Date** | Aug 13, 2026 |

---

## 1. Document purpose & method

This PRD was written by decompiling and analyzing a shipped click-through prototype (`index 4.html`). Every requirement below is traceable to behavior or data present in that build. Where the prototype is deliberately non-functional (mocked, stubbed, or hardcoded), it is called out explicitly in §11 rather than being silently promoted into a requirement.

**Two things this document is not:** it is not a record of an agreed-upon business case (no goals, metrics, or stakeholder inputs exist in the artifact — §3 states inferred goals as assumptions), and it is not a backend specification (the prototype has no server contract — §9 proposes one).

---

## 2. Product overview

### 2.1 What it is

A consolidated **Reports workspace** for Endpoint Central, an endpoint management platform. It is the single destination where an IT admin finds, runs, builds, schedules, and shares operational reporting across patching, vulnerabilities, compliance, inventory, Active Directory, device control, DLP, malware protection, BitLocker, USB, and MDM.

Product tagline present in the build:
> "All your endpoint reports, dashboards, and schedules — in one place."

### 2.2 The core proposition

Today's reporting surfaces in endpoint-management tools are fragmented: canned reports live in one place, custom builders in another, schedules in a third, and there is no way to extend the catalog. This module unifies them behind **one navigation spine, one search, and one visual language**, and adds two growth vectors:

1. **Extensions marketplace** — report/dashboard packs installable from ManageEngine and community authors.
2. **ZIA AI generation** — describe a report or dashboard in natural language and have it built.

### 2.3 Content surfaces (six)

| Surface | Nature | Prototype volume |
|---|---|---|
| Predefined Reports | Vendor-shipped, read-only catalog | 74 reports / 20 modules / 21 sub-categories |
| Predefined Dashboards | Vendor-shipped, read-only catalog | 23 dashboards / 7 modules / 2 categories |
| Custom Reports | User-owned, created 3 ways | 10 seeded |
| Custom Dashboards | User-owned, widget-based | 6 seeded |
| Query Reports | SQL-expression-driven | 6 seeded |
| Schedule Reports | Automated delivery jobs | 7 seeded |
| Extensions | Installable packs | 12 listed (4 installed) |

---

## 3. Goals, non-goals & success metrics

> ⚠️ **Assumption flag.** The artifact contains no stated business objectives. The goals below are inferred from the feature set and information architecture, and must be confirmed with product ownership before this section is treated as authoritative.

### 3.1 Product goals (inferred)

| # | Goal | Rationale visible in the build |
|---|---|---|
| G1 | Reduce time-to-answer for endpoint questions | Global ⌘K-style search spans all six surfaces; home surfaces recent activity |
| G2 | Make the report catalog discoverable at scale | Three-level taxonomy + per-module submenu with its own search field |
| G3 | Let admins self-serve custom reporting without SQL | AI-assisted builder + manual column/widget picker as peers |
| G4 | Turn reporting into an extensible platform | Marketplace with third-party/community authorship, ratings, install counts, versioning |
| G5 | Automate recurring compliance evidence | Schedule wizard with multi-format, multi-recipient, retention policy |
| G6 | Establish one visual system across all report surfaces | Single `ec-*` design token set applied uniformly |

### 3.2 Non-goals (for this module)

- Report **execution engine** and data warehouse — consumed, not owned, by this module.
- Endpoint agent management, patch deployment, remediation actions.
- Identity/RBAC administration (this module consumes roles; it does not define them).
- Mail server configuration (linked out to, not owned — see the "Configure Mail Server Settings" link).
- Export-security / data-masking configuration (linked out to as "Export Setting to secure personal data").

### 3.3 Proposed success metrics

| Metric | Target hypothesis |
|---|---|
| Median time from landing → report rendered | < 20 s |
| % of sessions using global search | > 40% |
| Custom reports created via AI vs manual | Establish baseline; AI ≥ 30% within 2 quarters |
| Extension install rate per active tenant | ≥ 1.5 packs |
| Scheduled reports with ≥ 1 successful delivery in 30 days | > 90% |
| Schedule failure rate | < 2% (prototype seeds 1 failed of 7 — 14% — as a UI state, not a target) |

---

## 4. Users & personas

Derived from the `createdBy`, `recipients`, and `sharedWith` fields in the seed data.

| Persona | Evidence in build | Primary jobs |
|---|---|---|
| **IT Administrator** (primary) | `createdBy: "Bharath"`, `"Admin"`, `admin@acme.com` | Run predefined reports, build custom ones, manage schedules, install extensions |
| **Security Analyst / CISO** | `security@acme.com`, `ciso@acme.com`, `sharedWith: ["CISO","Security Team"]` | Threat & vulnerability dashboards, patch SLA, ransomware and Zero Trust posture |
| **Compliance / Audit** | `audit@acme.com`, `sharedWith: ["Auditors"]`, "Q2 Compliance Audit" | Scheduled evidence packs (HIPAA/GDPR/PCI-DSS), retention policy, PDF export |
| **IT Operations** | `it-ops@acme.com` | Inventory, disk space, endpoint health, hardware refresh planning |
| **Finance / SAM** | `finance@acme.com`, `sharedWith: ["Finance"]` | License compliance, software metering, cost reclamation |
| **Power user / analyst** | `John D.`, `Sarah K.` on query reports | Direct SQL-expression reports |

---

## 5. Information architecture & navigation

### 5.1 Route map

| Route | Screen | Notes |
|---|---|---|
| `/` | Home | Stat tiles, recent activity, newly added |
| `/predefined-reports` | Predefined Reports catalog | Defaults to first module |
| `/predefined-reports/:moduleId` | Module-scoped catalog | 20 module IDs |
| `/predefined-dashboard` | Predefined Dashboards catalog | Defaults to first module |
| `/predefined-dashboard/:moduleId` | Module-scoped catalog | `sec-patch`, `sec-threats`, `sec-compliance`, `ep-health`, `ep-inventory`, `ep-users`, `ep-mdm` |
| `/custom-reports` | Custom Reports list | Also the 404 fallback (`path: "*"`) |
| `/custom-dashboards` | Custom Dashboards list | |
| `/query-reports` | Query Reports list | |
| `/schedule-reports` | Schedule Reports list | |
| `/extensions` | Extensions Marketplace | |
| `/create-report` | Report creation (full-shell takeover) | Accepts `?prompt=` deep link |
| `/create-dashboard` | Dashboard creation (full-shell takeover) | Accepts `?prompt=` deep link |
| `/create-query-report` | Query builder | |
| `/create-schedule-report` | Schedule wizard | |
| `/ask-zia` | **Feature-flagged off** → redirects to `/` | `featureFlags.askZia.enabled = false` |

All list routes also accept `?search=<term>` to arrive pre-filtered — this is how global search navigates.

### 5.2 Left rail (72 px icon rail, collapsible)

```
[Logo → /]
Home
Predefined Report      ▸ hover submenu (20 modules, 2 groups, searchable)
Predefined Dashboard   ▸ hover submenu (7 modules, 2 groups, searchable)
──────────────
Custom Report
Custom Dashboard
Query Report
Schedule Report
Ask ZIA  [AI badge]    ← hidden by feature flag
```

**Requirements**

- **NAV-1** Rail collapses to 0 px and expands to 72 px with a 300 ms ease-in-out transition; state persists for the session.
- **NAV-2** Below `lg`, the rail becomes an overlay drawer (`fixed`, `z-50`, translate-X) dismissed on item selection.
- **NAV-3** Active state = 2 px left accent bar + primary color + tinted background. Active detection includes creation routes (e.g. `/create-report` marks *Custom Report* active).
- **NAV-4** Predefined submenus open on hover (200 ms close delay to survive pointer travel) and on click; each contains its own type-ahead filter over module labels.
- **NAV-5** Items with a `featureKey` render only when that flag is enabled.

### 5.3 Global search

- **SRCH-1** Single search field in the app header queries a flattened index over **all** predefined reports, predefined dashboards, custom reports, custom dashboards, query reports, schedule reports, and extensions.
- **SRCH-2** Matching is case-insensitive substring across `name`, `description`, and `category`.
- **SRCH-3** Results group by type in fixed order: Predefined Report → Predefined Dashboard → Custom Report → Custom Dashboard → Query Report → Schedule Report → Extension.
- **SRCH-4** A type filter chip restricts results to one type and, when set, shows that type's full list on an empty query.
- **SRCH-5** Recent searches persist in `localStorage` under `ec_recent_searches`, capped at **6** entries, most-recent-first, de-duplicated.
- **SRCH-6** Empty-query panel shows Recent Searches, Recent Report Activity (with live status icon), and Newly Added.
- **SRCH-7** Selecting a result navigates to `{path}?search={encodeURIComponent(name)}`, pre-filtering the destination list.
- **SRCH-8** Dismissal: `Escape` key, outside click.
- **SRCH-9** ⌘K affordance is displayed on Home. **Gap:** no keyboard handler is bound in the prototype (§11, GAP-3).

---

## 6. Screen-by-screen functional requirements

### 6.1 Home (`/`)

Six clickable stat tiles in a responsive grid (2 / 3 / 6 columns):

| Tile | Value source | Navigates to |
|---|---|---|
| Total Reports | computed from custom reports | `/custom-reports` |
| Dashboards | computed from custom dashboards | `/custom-dashboards` |
| Predefined Reports | **hardcoded "23"** (actual catalog: 74) | `/predefined-reports` |
| Predefined Dashboards | **hardcoded "14"** (actual catalog: 23) | `/predefined-dashboard` |
| Scheduled | computed (`status === "Scheduled"`) | `/schedule-reports` |
| Extensions | computed (`isInstalled`) | `/extensions` |

- **HOME-1** All six tiles must derive counts from live data. The two hardcoded values are a defect (§11, GAP-1).
- **HOME-2** Predefined tiles carry a "+2 New" hover-peek popover listing recently added items, deep-linking to the owning module.
- **HOME-3** "Create new" dropdown offers four entry points: Custom Report, Custom Dashboard, Query Report, Schedule Report — each with description and colored icon.
- **HOME-4** "Recent Report Activity" lists recent items with live status (Ready / Running / Scheduled / Failed) and a "View all" link.
- **HOME-5** "All Sections" strip provides jump links to each surface.

### 6.2 Predefined Reports (`/predefined-reports[/:moduleId]`)

**Taxonomy** — three levels: Category → Module → Sub-category → Report.

- **Active Directory** (6 modules): User Reports (5 sub-categories: General, Password Based, Account Status, Privileged, Logon Based), Computer Reports, Group Reports, OU Reports, Domain Reports, GPO Reports.
- **Other Reports** (14 modules): User Logon, Power Management, Configuration, Threats & Patches, Self Service Portal, Inventory, Browser, Device Control, DLP, Malware Protection, Application Control, BitLocker, USB, Custom Groups, MDM.

**Requirements**

- **PDR-1** Each report record carries `id`, `name`, `description`, `type` ∈ {Table, Chart, KPI}.
- **PDR-2** Filters: sub-category chips (derived from the active module), type filter (All / Table / Chart / KPI), free-text search over name + description.
- **PDR-3** Dual view mode — grid (cards with SVG type-preview thumbnail) and table — toggled and remembered.
- **PDR-4** Table columns: Name, Description, Type, Actions. Sortable by name/type, ascending default, with direction toggle and a sort indicator.
- **PDR-5** Grid groups by sub-category with collapsible section headers.
- **PDR-6** Row actions: **Run**, **Export**.
- **PDR-7** Pagination with a "Rows per page" control.
- **PDR-8** Empty states distinguish *no results for filters* ("No reports match your filters.") from *no results for search* ("No reports found / Try a different search term").
- **PDR-9** On mount, `?search=` from the URL seeds the search field and resets collapsed groups.

### 6.3 Predefined Dashboards (`/predefined-dashboard[/:moduleId]`)

Two categories:
- **Security** — Patch Management (Overview, Detailed Views), Threat & Vulnerability (Overview, Malware Protection), Compliance (Overview).
- **Endpoint Management** — Endpoint Health (Overview, Performance), Inventory (Hardware, Software), User Activity, MDM.

- **PDD-1** Each dashboard carries `name`, `description`, `widgets` (count), `lastViewed` (relative time), accent `color`, `icon`.
- **PDD-2** Same filter / dual-view / sort / pagination / empty-state contract as §6.2.
- **PDD-3** Cards render a color-tinted SVG preview thumbnail derived from the dashboard's accent color.
- **PDD-4** Table rows are click-through to the dashboard.

### 6.4 Custom Reports (`/custom-reports`)

**Data contract per report:** `name`, `description`, `category`, `source`, `type`, `schedule`, `lastRun`, `lastModified`, `createdBy`, `status`, `remarks`, `installedFrom`.

**Provenance (`source`) — a first-class concept:**

| Source | Label | Color | Meaning |
|---|---|---|---|
| `manual` | Manual | `#475569` | Hand-built in the report builder |
| `extension` | Extension | `#1a5dc6` | Came from an installed pack; `installedFrom` names the pack |
| `zia` | ZIA AI | `#7c3aed` | Generated from a natural-language prompt |

**Status vocabulary:** Ready (green, "Active") · Running (blue) · Scheduled (amber) · Failed (red).

- **CR-1** Filter by source (All / Manual / Extension / ZIA (AI)), by category, and by free text over name + description.
- **CR-2** Sortable table — default sort `lastModified` descending. Columns: Name, Category, Type, Source, Schedule, Last Run, Created By, Status, Remarks, Action.
- **CR-3** Grid cards show source badge, type badge, status pill, schedule, and a type-appropriate SVG preview.
- **CR-4** Row actions include **Copy link**; grid cards expose a "More" overflow.
- **CR-5** Extension-sourced reports must visibly attribute their originating pack.
- **CR-6** "Create Report" CTA routes to `/create-report`.

### 6.5 Custom Dashboards (`/custom-dashboards`)

Same list contract as §6.4, with dashboard-specific fields: `widgets` (count) and `sharedWith` (array of groups: IT Team, CISO, Security Team, Finance, Auditors).

- **CD-1** Table columns: Name, Category, Source, Widgets, Shared With, Last Modified, Created By, Action.
- **CD-2** `sharedWith` renders as chips; overflow collapses to a "+N" indicator.
- **CD-3** Category accent colors: Patch (green), Vulnerability (red), Compliance (amber), Inventory (purple), Security, Software, USB.

### 6.6 Report / Dashboard creation (`/create-report`, `/create-dashboard`)

This screen takes over the full shell (no page chrome) and offers **two peer modes**.

#### Mode A — ZIA AI (conversational)

- **AI-1** Chat transcript with user/AI turns, each timestamped `HH:MM`.
- **AI-2** Type-appropriate starter suggestions, e.g. for reports: *"Show all endpoints missing critical patches from the last 30 days"*, *"List endpoints with unauthorized software installed"*, *"Generate a USB device usage report for this month"*, HIPAA compliance.
- **AI-3** AI responses are **structured specifications**, not prose — they enumerate Data source, Filter, Columns, Group by, Sort, and closing guidance. Dashboard responses enumerate numbered widgets and refresh behavior.
- **AI-4** A generating state with a spinner is shown while the response is pending (prototype: fixed 2 s).
- **AI-5** `Enter` sends; the input is disabled while generating.
- **AI-6** Accepts an `initialPrompt` from `?prompt=` for deep-linked generation.
- **AI-7** Switching modes with content present raises a **"Discard & Switch"** confirmation.

#### Mode B — Manual builder

- **MB-1** Fields: Name, Description, Category (Patch / Vulnerability / Compliance / Inventory / Security / Browser / Software), Output Format (PDF / XLSX / CSV / HTML), Refresh Interval (Real-time / Every 5 min / Every 15 min / Hourly), Schedule (On-demand / Daily / Weekly / Monthly).
- **MB-2** **Reports:** multi-select column chips — Endpoint Name, IP Address, OS, User, Department, Patch ID, Severity, Status, Last Seen, Agent Version, MAC Address, Location.
- **MB-3** **Dashboards:** multi-select widget chips — Donut Chart, Bar Chart, Line Chart, KPI Card, Data Table, Heatmap, Gauge, Pie Chart, World Map, Stacked Bar, Trend Line, Alert List.
- **MB-4** Selected chips render in the primary fill; unselected are outlined.
- **MB-5** Primary action is labelled contextually ("Create Report" / "Create Dashboard"); Cancel returns to the owning list.

### 6.7 Query Reports (`/query-reports`, `/create-query-report`)

**List**

- **QR-1** Records carry `name`, `query` (SQL string, rendered monospace), `description`, `lastRun`, `duration`, `rowCount`, `status`, `createdBy`, `category`.
- **QR-2** Status vocabulary: Success (green) · Running (blue, animated) · Failed (red) · Never Run (grey).
- **QR-3** Filter by status and category; sort default `lastRun` descending.
- **QR-4** Row actions: Run, Download, Copy link, More.

**Builder**

- **QR-5** Fields: report name, query expression (textarea), Records per page (25 / 50 / 100 / 200 / 500, default 100).
- **QR-6** Actions: **Run Report** (execute without persisting), **Run & Save**, **Reset**.

### 6.8 Schedule Reports (`/schedule-reports`, `/create-schedule-report`)

**List**

- **SR-1** Records carry `reportName`, `frequency` (Daily / Weekly / Monthly / Once), `nextRun`, `lastRun`, `recipients[]`, `format` (PDF / Excel / CSV), `status`, `category`.
- **SR-2** Status vocabulary: Active · Paused · Failed · Completed. Frequency has its own color coding.
- **SR-3** Row actions: **Pause** / **Resume** (mutually exclusive on status), **Delete**, Copy link, More.
- **SR-4** **Report Retention Period** is a list-level setting: "Maintain last **N** Days / Reports", with Save / Cancel.
- **SR-5** Recipients render as an email chip list with overflow.
- **SR-6** Grid card preview visualizes the frequency as a calendar heat-grid tinted by status; paused/failed schedules render desaturated.

**Wizard (`/create-schedule-report`)** — four fielded sections, ManageEngine classic form styling:

1. **Create Scheduled Reports** — Scheduler Name (**required**), Description.
2. **Select Reports** — dual-pane picker. Left: expandable report tree (Active Directory, User Logon, Power Management, Patch [Missing Patches / Patch Status Summary / Patch Compliance], Vulnerability, Inventory [Hardware / Software / Disk Space], USB, Application Control, Device Control, BitLocker). Right: "Selected Reports (N)" with per-item removal and an illustrated empty state.
3. **Specify Delivery Format and Recipients**
   - Export settings — links out to secure-personal-data configuration.
   - Report Formats — multi-check PDF / XLSX / CSV (default CSV).
   - "Receive emails even when no data is available" — Yes / No radio (default Yes).
   - Action — *Send each report as an attachment* (default) / *Send reports as a zipped file* / *Publish reports on the Central server and send the URL*.
   - **Size-threshold override:** if total size exceeds **N MB** (default 5), publish to the server and send a URL regardless of the option above.
   - To (**required**, comma-separated), CC, Subject (**required**), Content.
   - Inline link to Mail Server Settings.
4. **Specify the Frequency** — links to the scheduler configuration; renders "Scheduler has not been configured yet." until set.
5. **User Consent** — explicit consent checkbox.

- **SR-7 (validation)** The **Schedule** action stays disabled until Scheduler Name is non-empty **AND** To is non-empty **AND** User Consent is checked.

### 6.9 Extensions Marketplace (`/extensions`)

**Data contract:** `name`, `description`, `category`, `author` (ManageEngine | Community), `version` (semver), `rating` (0–5), `installs`, `tags[]`, `isInstalled`, `type` (report | dashboard), `lastUpdated`, `size`, `thumbnailColor`, `thumbnailIcon`.

**Catalog (12):** USB Security Audit Pack · Browser Security Toolkit · Compliance Trend Pack · License Compliance Pack *(installed)* · Ransomware Defense Report · Remote Work Endpoint Health · Patch SLA Tracker · Privileged Account Activity · Software Metering Dashboard · Mobile Device Compliance · Endpoint Performance Index · Zero Trust Readiness Report.

- **EXT-1** Filter by type and category; search over name and tags.
- **EXT-2** Sort by **Most Installed** (default) / **Highest Rated** / **Recently Updated**.
- **EXT-3** Cards show icon, rating, install count, author, version, and an install/installed state.
- **EXT-4** **Details** opens a modal with full description, tags, version, size, last-updated, author, and the install action.
- **EXT-5** Install shows a progress state (prototype: 1.8 s) then flips to installed; the installed pack's reports/dashboards appear in Custom Reports/Dashboards with `source: extension` and `installedFrom` set.
- **EXT-6** A "How Extensions Work" explainer and a "NEW" badge are present on the page.
- **EXT-7** Empty state: "No extensions found / Try adjusting your filters or search query."

---

## 7. Cross-cutting requirements

### 7.1 List behavior contract (applies to all six list surfaces)

Every list surface implements the same contract. This is the module's strongest consistency asset and must be preserved.

- **LIST-1** Free-text search with a "Clear filter" affordance.
- **LIST-2** "Filter By :" chip row, always including a category or status dimension.
- **LIST-3** Grid ⇄ Table toggle, both fully featured.
- **LIST-4** Column sort with three-state indicator (unsorted 30% opacity / asc / desc) and click-to-toggle direction.
- **LIST-5** Pagination with configurable rows per page.
- **LIST-6** Distinct empty states for *no data*, *no filter match*, and *no search match*.
- **LIST-7** URL `?search=` parameter seeds the search field on mount.
- **LIST-8** Row hover reveals actions; actions never occupy layout space when idle.

### 7.2 Status & badge system

A single status vocabulary is reused across surfaces with fixed colors — Success/Ready/Active `#16a34a`, Running/In-progress `#1a5dc6`, Scheduled/Paused `#d97706`, Failed `#dc2626`, Never Run/Completed `#6b7280`.

- **BADGE-1** Every status pill = icon + label + tinted background; never color alone (accessibility).
- **BADGE-2** Running states animate (spin) to signal liveness.

### 7.3 Preview thumbnails

- **THUMB-1** Grid cards render inline SVG previews (120 × 72 viewBox) synthesized per item type — table previews draw header + rows, chart previews draw bars, KPI previews draw stat blocks, dashboard previews tint to the item's accent color.
- **THUMB-2** No raster assets; previews must remain resolution-independent and zero-network.

---

## 8. Design system

### 8.1 Tokens

| Token | Value | Use |
|---|---|---|
| `ec-primary` | `rgb(26, 93, 198)` — `#1a5dc6` | Brand, active state, links, primary buttons |
| `ec-primary-light` | `#e8f1fd` | Active backgrounds, tinted chips |
| `ec-bg` | `rgb(244, 246, 249)` — `#f4f6f9` | App canvas |
| `ec-surface` | `#ffffff` | Cards, panels, rails |
| `ec-border` / `ec-border-strong` | greys | Hairlines, hover borders |
| `ec-text` / `ec-text-muted` / `ec-text-subtle` | 3-step hierarchy | Body / secondary / label |
| `ec-success` `#16a34a` · `ec-error` `#dc2626` · `ec-purple` `#7c3aed` | + `-light` tints | Semantic states |
| `shadow-ec-card` | `0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04)` | Resting card |
| `shadow-ec-hover` | elevated | Hover card |

**Category accents:** Patch `#16a34a` · Vulnerability `#dc2626` · Compliance `#d97706` · Inventory `#7c3aed` · Security · Software `#9333ea` · USB · Browser `#0ea5e9` · Performance `#0891b2`.

### 8.2 Typography & shape

- Font: **Inter** (400/500/600/700), Google Fonts with `preconnect`; fallback `system-ui, -apple-system, sans-serif`. Monospace stack reserved for query expressions.
- Scale is deliberately dense: `text-[10px]` nav labels, `text-xs` (12 px) table/form body, `text-sm` (14 px) controls, `text-base` page titles, `text-2xl` stat values.
- Radii: `rounded-xl` cards, `rounded-lg` icon tiles/buttons, `rounded-md` small chips, `rounded-full` status pills.
- Icons: **lucide-react** v0.453.0 throughout; standard sizes 3.5 / 4 / 5 / 9 units.

### 8.3 Motion

Five keyframe families — `fade`, `scale`, `slide`, `spin`, `pulse`. Rail transition 300 ms ease-in-out; hover/color transitions ~200 ms; cards use `active:scale-[0.98]` for press feedback; hover submenus use a 120–200 ms close delay to tolerate pointer travel.

### 8.4 Two coexisting visual idioms — **a decision this PRD flags**

The build contains **two** form languages:
- **Modern** — rounded cards, soft shadows, generous spacing (all list, catalog, home, marketplace screens).
- **Classic ManageEngine** — square-cornered bordered sections, 208 px left-aligned labels, dense 12 px fields (the schedule wizard only, at §6.8).

The schedule wizard also uses raw `blue-50/blue-600/gray-*` Tailwind utilities in its submenu instead of `ec-*` tokens.

> **Open decision (D1):** Is the classic idiom intentional — preserving muscle memory for admins migrating from the existing product — or is it unmigrated legacy? Resolve before build; it changes the wizard's entire implementation.

### 8.5 Responsive

- Breakpoint spine at Tailwind `lg` (1024 px): rail becomes an overlay drawer below it.
- Home stat grid: 2 → 3 → 6 columns at `sm` / `lg`.
- Long text truncates rather than wraps in dense rows; icon-only buttons carry `title` tooltips.

---

## 9. Data model (proposed backend contract)

The prototype has no server. The following contract is derived from the shapes it consumes.

```ts
type Source   = 'manual' | 'extension' | 'zia';
type ItemType = 'Table' | 'Chart' | 'KPI';
type Status   = 'Ready' | 'Running' | 'Scheduled' | 'Failed';

interface PredefinedReport {
  id: string; name: string; description: string; type: ItemType;
  // parent chain: category → module → subCategory
}

interface CustomReport {
  id: string; name: string; description: string;
  category: string; source: Source; type: ItemType;
  schedule: 'On-demand' | 'Daily' | 'Weekly' | 'Monthly';
  lastRun: string;        // ISO datetime
  lastModified: string;   // ISO datetime
  createdBy: string; status: Status; remarks: string;
  installedFrom?: string; // extension pack name; required when source === 'extension'
}

interface CustomDashboard {
  id: string; name: string; description: string;
  category: string; source: Source;
  widgets: number; lastModified: string; createdBy: string;
  sharedWith: string[]; installedFrom?: string;
}

interface QueryReport {
  id: string; name: string; query: string; description: string;
  lastRun: string; duration: string; rowCount: number;
  status: 'Success' | 'Running' | 'Failed' | 'Never Run';
  createdBy: string; category: string;
}

interface ScheduledReport {
  id: string; reportName: string;
  frequency: 'Daily' | 'Weekly' | 'Monthly' | 'Once';
  nextRun: string; lastRun: string;
  recipients: string[]; format: 'PDF' | 'Excel' | 'CSV';
  status: 'Active' | 'Paused' | 'Failed' | 'Completed';
  category: string;
}

interface Extension {
  id: string; name: string; description: string; category: string;
  author: 'ManageEngine' | 'Community' | string;
  version: string; rating: number; installs: number;
  tags: string[]; isInstalled: boolean;
  type: 'report' | 'dashboard';
  lastUpdated: string; size: string;
  thumbnailColor: string; thumbnailIcon: string;
}
```

### 9.1 Required API surface (to be built)

| Area | Endpoints |
|---|---|
| Catalog | `GET /predefined/reports`, `GET /predefined/dashboards` (taxonomy-shaped) |
| Custom | full CRUD on `/reports` and `/dashboards`; `POST /reports/:id/run`, `POST /reports/:id/export` |
| Query | CRUD; `POST /queries/run` (ad-hoc), `POST /queries/:id/run` |
| Schedules | CRUD; `POST /schedules/:id/pause` · `/resume` · `/run-now`; `GET/PUT /schedules/retention` |
| Extensions | `GET /extensions`, `POST /extensions/:id/install`, `DELETE /extensions/:id` |
| AI | `POST /zia/generate` `{ type, prompt, history[] }` → structured report/dashboard spec |
| Search | `GET /search?q=&type=` — cross-surface index |

---

## 10. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-1 | **Bundle** — the prototype ships as one self-contained 470 KB HTML file with zero runtime network dependency except the Inter webfont. Production must code-split per route; target < 200 KB initial JS gzipped. |
| NFR-2 | **Font resilience** — Inter is fetched from Google Fonts. Air-gapped and China-region deployments are common for endpoint management; the font must be self-hosted with a system fallback. |
| NFR-3 | **Catalog scale** — the flattened search index spans 74 + 23 predefined items plus all user content. At enterprise volume (thousands of custom reports), search and list filtering must move server-side with debounced querying. |
| NFR-4 | **Accessibility** — status is never conveyed by color alone (already satisfied via icon+label). Outstanding: focus-visible rings on all interactive elements, keyboard operation of hover submenus, `aria-expanded`/`aria-controls` on disclosures, `aria-sort` on sortable headers, and contrast verification of muted text at 10–12 px. Target WCAG 2.1 AA. |
| NFR-5 | **Localization** — all strings are currently hardcoded English. Externalize before GA; note that the 72 px rail assumes short two-line labels that will overflow in German/Finnish. |
| NFR-6 | **Performance** — list virtualization required beyond ~200 rows; the prototype renders all rows. |
| NFR-7 | **RBAC** — `sharedWith` and `createdBy` exist as display fields with no enforcement. Production must enforce read/edit/share/schedule permissions per role. |
| NFR-8 | **Multi-tenancy** — seed data uses one tenant (`acme.com`). Tenant scoping is unmodeled. |
| NFR-9 | **Browser support** — modern evergreen (ES2020 modules, CSS custom properties, `:has`-free). |

---

## 11. Prototype gaps & defects

Everything in this section is a **known limitation of the artifact**, not a product requirement. These are the items that must be closed to move from prototype to shippable.

| ID | Severity | Finding |
|---|---|---|
| GAP-1 | **Defect** | Home "Predefined Reports" tile is hardcoded to **23** and "Predefined Dashboards" to **14**; the actual catalogs contain **74** and **23**. Both must be computed. |
| GAP-2 | High | **No persistence.** All data lives in in-memory JS arrays. Creating, editing, pausing, deleting, or installing anything is lost on refresh. Only `ec_recent_searches` survives, via `localStorage`. |
| GAP-3 | Medium | **⌘K is decorative.** The Home surface advertises a ⌘K shortcut, but no `keydown` listener is registered for it — only `Escape` (close) is bound. Either implement it or remove the affordance. |
| GAP-4 | Medium | **ZIA is fully simulated.** Responses are drawn round-robin from a fixed pool of 4 report and 4 dashboard canned answers on a 2 s `setTimeout`, cycling by index and ignoring the user's actual prompt. |
| GAP-5 | Medium | **Extension install is cosmetic.** A 1.8 s `setTimeout` flips `isInstalled`; no content is actually added to any catalog. |
| GAP-6 | Medium | **Run / Export / Download / Copy link are inert.** No report ever renders output; there is no report *viewer* screen at all in the build. |
| GAP-7 | Medium | **`/ask-zia` is dead.** The nav entry is filtered out by `featureFlags.askZia.enabled = false` and the route redirects to `/`. Its intended scope is undefined. |
| GAP-8 | Low | **404 handling.** The wildcard route silently renders Custom Reports instead of a not-found state. |
| GAP-9 | Low | **Design inconsistency.** The schedule wizard uses raw Tailwind palette utilities (`blue-50`, `gray-600`) rather than `ec-*` tokens — see §8.4/D1. |
| GAP-10 | Low | **Query builder has no SQL affordances** — no syntax highlighting, validation, autocomplete, or result grid. |
| GAP-11 | Low | **Schedule wizard frequency section is a stub** — "Scheduler has not been configured yet" with a link, but no actual scheduler UI. |
| GAP-12 | Low | **No dashboard canvas.** Dashboards are only ever listed; there is no widget layout, drag-drop, or rendering surface. |

---

## 12. Open questions

| # | Question | Owner |
|---|---|---|
| D1 | Is the classic-form idiom in the schedule wizard intentional (migration muscle memory) or legacy to be migrated? | Design |
| D2 | What is `/ask-zia` meant to be — a standalone conversational analytics surface distinct from in-builder generation? Why is it flagged off? | Product |
| D3 | Can users author or publish extensions, or is the marketplace curated? What governs "Community" authorship? | Product |
| D4 | Are ZIA-generated reports editable afterward, or regenerate-only? Is the generating prompt retained as provenance? | Product |
| D5 | Does `sharedWith` imply real sharing/permission grants, or is it descriptive metadata? | Product / Security |
| D6 | What is the report **viewer** experience? It is the single largest missing surface. | Product / Design |
| D7 | Is the retention policy per-schedule or global? The prototype places it at the list level, implying global. | Product |
| D8 | Should predefined reports be favoritable / pinnable? 74 items with no personalization is a lot to navigate. | Design |
| D9 | Do custom reports support drill-down or cross-report linking? | Product |
| D10 | Is the `?prompt=` deep link into AI creation an intended integration point for other product areas? | Engineering |

---

## 13. Phased scope recommendation

| Phase | Scope | Rationale |
|---|---|---|
| **P0 — Foundation** | Predefined Reports + Dashboards catalogs, list contract (§7.1), global search, home, **report viewer**, run/export | The catalog is worthless without a viewer (GAP-6); this is the minimum coherent product |
| **P1 — Authoring** | Manual report + dashboard builders, dashboard canvas, custom lists, persistence layer | Closes GAP-2 and GAP-12 |
| **P2 — Automation** | Schedule wizard, schedule list, retention, mail integration, query reports | Compliance-evidence use case unblocked |
| **P3 — Platform** | Extensions marketplace, install pipeline, versioning/updates | Growth vector; depends on P1's content model |
| **P4 — Intelligence** | ZIA generation (real), `/ask-zia` surface | Highest uncertainty (D2, D4); depends on a stable report spec format from P1 |

---

## 14. Appendix — technology inventory

| Layer | Technology |
|---|---|
| Framework | React 18 (production build, `StrictMode`) |
| Routing | React Router v6 (`BrowserRouter`, `useNavigate`, `useLocation`, `useParams`, `useSearchParams`) |
| Styling | Tailwind CSS (compiled, inlined) + custom `ec-*` token layer |
| Icons | lucide-react v0.453.0 (ISC) |
| Build | Vite (module preload polyfill present), single-file inline output |
| State | React local state only — no Redux/Zustand/Context store; no data-fetching library |
| Persistence | `localStorage` (`ec_recent_searches`, cap 6) |
| Backend | **None** — all data is hardcoded module-scope arrays |
