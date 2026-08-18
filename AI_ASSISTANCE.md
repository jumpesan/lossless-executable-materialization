# AI Assistance Disclosure

This research has been conducted with **extensive use of AI assistants**, primarily through general-purpose ChatGPT/LLM environments.

AI assistance is not incidental to this project. It has been used as part of the research and engineering workflow for activities including:

- architecture exploration and hypothesis generation;
- critique and refinement of proposed responsibility and trust boundaries;
- experiment planning and black-box test design;
- drafting and refactoring code, descriptors, scripts, and documentation;
- analyzing experimental outputs and comparing competing explanations;
- prior-art search support and terminology expansion;
- technical writing, editing, translation, and repository preparation.

The project also uses LLMs as an **experimental runtime/host under study**, which is a separate role from their use as research assistants.

## Evidence policy

AI-generated text, code, interpretation, or confidence is **not treated as experimental evidence by itself**.

Claims in this repository are intended to be grounded in inspectable or reproducible evidence such as:

```text
canonical artifact identities
cryptographic hashes
Git blob identities
published representation units
machine decode/materialization results
compile and execution results
structured outputs
negative controls
fresh-session black-box observations
independent post-run artifact verification
```

Where an AI assistant proposes an explanation, architecture, or protocol rule, that proposal remains a hypothesis until supported by the relevant experiment or artifact evidence.

## Responsibility

AI systems are not listed as authors or accountable researchers.

The human researcher retains responsibility for:

- deciding the research direction;
- selecting what is tested;
- accepting or rejecting AI-generated proposals;
- defining what counts as authoritative evidence;
- interpreting limitations and uncertainty;
- deciding what claims are published;
- correcting errors in this repository.

## Why this is disclosed

The broader research question itself concerns software architectures in which Context, deterministic Scripts, and general-purpose LLM hosts interact closely. Hiding the degree of AI involvement in the research process would make the methodology less transparent.

This disclosure is therefore intentionally explicit: **AI was used heavily both as a research/engineering assistant and, in controlled experiments, as part of the system being studied.**

The distinction between those roles should be preserved when interpreting results.
