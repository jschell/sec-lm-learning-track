# Citation and source policy

Applies to all project-authored instructional content and adaptations.

## Cite where the concept appears

Use ordinary Markdown links to the original source beside the explanation, example, or claim. End each module with a small source table. The central [register](../reference/sources.md) supplements these local citations.

Example: “This lesson adapts the inference/tool-feedback progression from [Geoffrey Huntley's workshop](https://ghuntley.com/agent/). The fixture and Python implementation are original to this project.”

Do not cite a source for a claim it does not make. Label recommendations and exercise design as project judgments. A source's benchmark is not evidence that our implementation achieves it.

## Preferred sources

Original author/video, original research, official protocol/runtime documentation, and upstream repository source. Use secondary explanations only when they add something specific; still cite the original for the underlying claim.

For videos, give author, exact title, URL, relevant topic, and verified chapter/time range when available. Omit unverified timestamps. Required local explanations must not depend on watching the video.

## Record provenance

| Material | Record |
| --- | --- |
| Article or video | Author/organization, title, canonical URL, publication date if verified, date checked |
| Code adaptation | Repository, source path, immutable commit, applicable license and retained notices |
| Runtime/API behavior | Official page, package/runtime version tested, date checked |
| Research result | Original paper and applicable experimental conditions |
| Dataset/fixture | Origin, transformation, rights/restrictions, version/hash; label synthetic data |

Current source-register entries are concept references. Code commit and tested-version fields must be added when implementation actually uses them.

## Reuse and verification

Write original explanations. Do not mirror articles, transcripts, or source repositories. Verify license terms before copying or adapting; attribution alone is not a license. Keep quotes short, explicit, and necessary.

Record what was checked: source existence/topic is different from reproducing code or verifying a result. Preserve historical references as historical. Recheck mutable API details when authoring executable lessons.

For broken links, preserve attribution and seek an official replacement. If only a secondary copy remains, state that limitation rather than silently changing the author or source.
