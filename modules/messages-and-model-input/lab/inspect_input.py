"""Inspect actual local tokenization/template rendering; no inference or tools run."""
import argparse
import json
from pathlib import Path

from jinja2.sandbox import ImmutableSandboxedEnvironment
from tokenizers import Tokenizer

from assets import HERE, MANIFEST, checked_assets


def load(directory: Path | None = None) -> tuple[Tokenizer, str]:
    """Load hash-checked tokenizer data and original, unmodified chat template."""
    path = checked_assets() if directory is None else checked_assets(directory)
    tokenizer = Tokenizer.from_file(str(path / 'tokenizer.json'))
    config = json.loads((path / 'tokenizer_config.json').read_text(encoding='utf-8'))
    return tokenizer, config['chat_template']


def encode(tokenizer: Tokenizer, text: str) -> dict:
    """Expose IDs, vocabulary pieces and offsets; keep special tokens on decode."""
    value = tokenizer.encode(text, add_special_tokens=False)
    return {'text':text, 'count':len(value.ids), 'ids':value.ids,
            'pieces':value.tokens, 'offsets':value.offsets,
            'decoded':tokenizer.decode(value.ids, skip_special_tokens=False)}


def render(template: str, messages: list[dict], tools: list[dict], generation: bool = True) -> str:
    """Render the pinned Qwen template for supplied synthetic text-only fixtures.

    This deliberately narrow Jinja invocation is not Transformers.apply_chat_template
    or a universal provider renderer. No downloaded Python code is executed.
    """
    environment = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)
    # Qwen uses JSON for function schemas/arguments. Preserve insertion order.
    environment.filters['tojson'] = lambda value: json.dumps(value, ensure_ascii=False)
    return environment.from_string(template).render(messages=messages, tools=tools,
                                                    add_generation_prompt=generation)


def inspect(variant: str = 'tool', generation: bool = True, text: str | None = None) -> dict:
    tokenizer, template = load()
    fixture = json.loads((HERE / 'fixtures.json').read_text(encoding='utf-8'))
    messages = fixture['messages']
    tools = fixture['tools']
    if variant in {'plain', 'omitted'}:
        # Omit the entire call/result exchange together, retaining system + user.
        messages = messages[:2]
    if variant == 'plain':
        tools = []
    rendered = render(template, messages, tools, generation)
    texts = fixture['texts'] if text is None else {'custom':text}
    return {'mode':'local-input-inspection; no inference', 'model':MANIFEST['repository'],
            'revision':MANIFEST['revision'], 'variant':variant,
            'texts':{name:encode(tokenizer, value) for name,value in texts.items()},
            'messages':messages, 'tools':tools, 'rendered':encode(tokenizer, rendered),
            'special_ids':{marker:tokenizer.token_to_id(marker)
                           for marker in ('<|im_start|>','<|im_end|>','<|endoftext|>')}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=['plain','tool','omitted'], default='tool')
    parser.add_argument('--no-generation-prompt', action='store_true')
    parser.add_argument('--text', help='Inspect one synthetic text instead of all text fixtures')
    args = parser.parse_args()
    print(json.dumps(inspect(args.variant, not args.no_generation_prompt, args.text),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
