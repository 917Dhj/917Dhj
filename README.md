<!-- GitHub profile README. Proof over adjectives. -->
<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/px-scale-dark.gif" /><img src="./assets/px-scale.gif" width="860" alt="" /></picture>

# <img src="./assets/hj-pixel.gif" alt="A small pixel robot, blinking" width="76" align="left" /><br/>Hey, I'm HJ Ding 👋

**AI Engineer · Open-Source Builder**<br/>
Long-video Understanding / Multimodal Agents / Agentic RL

I build agent tooling that researchers run every day, and study how AI understands people in long video.

🎓 M.S. in Computer Science, **Shenzhen University**<br/>
Graduating 2028 · looking for **engineering internships** in agents, developer tooling and applied AI.

<a href="https://github.com/917Dhj/DeepPaperNote"><img src="https://img.shields.io/github/stars/917Dhj/DeepPaperNote?style=flat-square&label=DeepPaperNote&color=D97757&logo=github&logoColor=white" alt="DeepPaperNote stars" height="20" /></a>
<a href="https://pypi.org/project/dkitchen/"><img src="https://img.shields.io/pypi/v/dkitchen?style=flat-square&label=dkitchen&color=2B8FFF&logo=pypi&logoColor=white" alt="dkitchen on PyPI" height="20" /></a>
<a href="https://github.com/917Dhj/DraftBar/releases/latest"><img src="https://img.shields.io/github/v/release/917Dhj/DraftBar?style=flat-square&label=DraftBar&color=C8923A&logo=apple&logoColor=white" alt="DraftBar latest release" height="20" /></a>

✉️ <a href="mailto:2510813014@mails.szu.edu.cn">Email</a> · <a href="https://www.linkedin.com/in/%E6%B3%93%E6%99%AF-%E4%B8%81-b014a23ba/">LinkedIn</a> · <a href="https://x.com/dahuoji09">X</a> · <a href="https://917dhj.github.io/DeepPaperNote/">DeepPaperNote site</a>

## <img src="./assets/px-mark.gif" width="12" height="12" alt="" />&nbsp;&nbsp;What I ship

<img src="./assets/deeppapernote-project.png" width="24" alt="" />&nbsp;**<a href="https://github.com/917Dhj/DeepPaperNote">DeepPaperNote</a>** &nbsp;<a href="https://github.com/917Dhj/DeepPaperNote/stargazers"><img src="https://img.shields.io/github/stars/917Dhj/DeepPaperNote?style=flat-square&label=stars&color=D97757&logo=github&logoColor=white" alt="DeepPaperNote GitHub stars" height="20" align="absmiddle" /></a> &nbsp;<sub>MIT · Obsidian + Zotero</sub>

*The single-paper ingestion layer for an LLM-maintained academic wiki.*

Most paper-reading agents hand you a prettier summary. DeepPaperNote keeps the evidence — the research question, the method chain, the formulas, the figure context, and the boundary of what the paper actually showed — and writes it as an Obsidian page a human will reopen and an agent can reuse. It ships as one plugin across Claude Code, Codex, Cursor, Copilot and Gemini CLI.

<sub><code>claude plugin marketplace add 917Dhj/DeepPaperNote</code></sub> · <a href="https://917dhj.github.io/DeepPaperNote/">Website</a> · <a href="https://github.com/917Dhj/DeepPaperNote">Repository</a> · <a href="https://github.com/917Dhj/DeepPaperNote/releases">Releases</a>

<img src="./assets/dkitchen-project.png" width="24" alt="" />&nbsp;**<a href="https://github.com/917Dhj/dkitchen">dkitchen</a>** &nbsp;<sub>PyPI 0.5.8 · 17 releases · MIT</sub>

*Your agents run the kitchen; you stay the head chef.*

The bottleneck in agent-run research is not execution — it is that you become the message bus. dkitchen gives every session a station, routes work through GitHub issues as tickets, puts a verifier between a plan and the GPU bill, and wakes a session back up when its long job finishes (`ding`). Nothing moves without your approval, in your own words.

<sub><code>pip install dkitchen</code></sub> · <a href="https://pypi.org/project/dkitchen/">PyPI</a> · <a href="https://github.com/917Dhj/dkitchen">Repository</a> · <a href="https://github.com/917Dhj/dkitchen/blob/main/docs/ding.md">Docs</a>

<img src="./assets/diverter-project.png" width="24" alt="" />&nbsp;**<a href="https://github.com/GML-MMGroup/Diverter">Diverter</a>** &nbsp;<sub>Codex plugin · MIT · GML-MMGroup</sub>

*One task in. The right subagents out.*

A coding agent does better on a big task when it hands pieces to specialist subagents, but Codex only plans that split for you in its Ultra mode. Diverter brings the same planning to everyday sessions: it decides when a task can split, routes each piece to the right specialist role, keeps the main thread on the critical path, and steps aside whenever Codex is already delegating on its own. Backed by 60+ automated tests and real subagent-lifecycle runs.

<a href="https://github.com/GML-MMGroup/Diverter">Repository</a>

<img src="./assets/draftbar-project.png" width="24" alt="" />&nbsp;**<a href="https://github.com/917Dhj/DraftBar">DraftBar</a>** &nbsp;<sub>macOS · Swift + SwiftUI · v2.0.3 · MIT</sub>

*The note you would otherwise lose between two apps.*

A native menu-bar scratchpad: pull it out, type, and the draft lands in a plain `note.md` on disk. No Electron, no account, no sync ceremony — the constraint is the feature.

<a href="https://github.com/917Dhj/DraftBar/releases/latest">Download</a> · <a href="https://github.com/917Dhj/DraftBar">Repository</a>

<sub>Also: <a href="https://github.com/917Dhj/DeepPaperNote-Connector">DeepPaperNote Connector</a> — a Chrome extension that drops paper PDFs into your Obsidian library, so the source and the note stay together.</sub>

## <img src="./assets/px-mark.gif" width="12" height="12" alt="" />&nbsp;&nbsp;Toolbox

**Day to day** &nbsp;Python · PyTorch · Claude Code · Codex · MCP<br/>
**Depth** &nbsp;agent orchestration · retrieval pipelines · plugin and skill packaging<br/>
**Also ship in** &nbsp;Swift / SwiftUI · TypeScript · Java<br/>
**Ops** &nbsp;Linux + GPU boxes · GitHub Actions · PyPI and release engineering

## <img src="./assets/px-mark.gif" width="12" height="12" alt="" />&nbsp;&nbsp;Open to

**Engineering internships in agents, developer tooling and applied AI.** The part I like is turning agent ideas into tools people run every day: orchestration, retrieval, packaging, and the plumbing that keeps long jobs moving without a human playing message bus. If your team is hiring for that, [email me](mailto:2510813014@mails.szu.edu.cn) or find me on [LinkedIn](https://www.linkedin.com/in/%E6%B3%93%E6%99%AF-%E4%B8%81-b014a23ba/).

Also glad to argue about how agent sessions should hand off work, or to hear where [DeepPaperNote](https://917dhj.github.io/DeepPaperNote/) got your field wrong.

<p><code>&gt;</code>&nbsp;<img src="./assets/px-caret.gif" width="7" height="14" alt="" /></p>
