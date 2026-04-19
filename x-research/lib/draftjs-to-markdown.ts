import type { DraftJsBlock, DraftJsContent } from './types';

function normalizeBlocks(input: DraftJsContent | DraftJsBlock[] | string | undefined): DraftJsBlock[] {
  if (!input) return [];
  if (typeof input === 'string') {
    return input
      .split(/\r?\n/)
      .map((line) => ({ text: line, type: 'unstyled' }));
  }
  if (Array.isArray(input)) {
    return input;
  }
  return Array.isArray(input.blocks) ? input.blocks : [];
}

function normalizeEntityMap(entityMap: DraftJsContent['entityMap']): Record<string, Record<string, unknown>> {
  if (!entityMap) {
    return {};
  }

  if (Array.isArray(entityMap)) {
    return Object.fromEntries(
      entityMap
        .filter((entry) => entry.key && entry.value)
        .map((entry) => [String(entry.key), entry.value as Record<string, unknown>]),
    );
  }

  return entityMap as Record<string, Record<string, unknown>>;
}

function applyInlineStyles(block: DraftJsBlock): string {
  const text = block.text ?? '';
  const ranges = [...(block.inlineStyleRanges ?? [])]
    .filter((range) => typeof range.offset === 'number' && typeof range.length === 'number' && range.length > 0)
    .sort((a, b) => (b.offset ?? 0) - (a.offset ?? 0));

  let output = text;
  for (const range of ranges) {
    const offset = range.offset ?? 0;
    const length = range.length ?? 0;
    const marker = range.style === 'Bold' ? '**' : range.style === 'ITALIC' ? '*' : '';
    if (!marker) {
      continue;
    }
    const before = output.slice(0, offset);
    const middle = output.slice(offset, offset + length);
    const after = output.slice(offset + length);
    output = `${before}${marker}${middle}${marker}${after}`;
  }

  return output.trimEnd();
}

function renderAtomicMarkdown(block: DraftJsBlock, entities: Record<string, Record<string, unknown>>): string {
  const entityKey = block.entityRanges?.[0]?.key;
  if (entityKey === undefined) {
    return '';
  }

  const entity = entities[String(entityKey)];
  const markdown = entity?.data && typeof entity.data === 'object'
    ? (entity.data as Record<string, unknown>).markdown
    : undefined;

  return typeof markdown === 'string' ? markdown.trim() : '';
}

function renderBlock(block: DraftJsBlock, entities: Record<string, Record<string, unknown>>): string {
  const text = applyInlineStyles(block);
  const depth = block.depth ?? 0;

  switch (block.type) {
    case 'header-one':
      return text ? `# ${text}` : '';
    case 'header-two':
      return text ? `## ${text}` : '';
    case 'header-three':
      return text ? `### ${text}` : '';
    case 'unordered-list-item':
      return `${'  '.repeat(depth)}- ${text}`.trimEnd();
    case 'ordered-list-item':
      return `${'  '.repeat(depth)}1. ${text}`.trimEnd();
    case 'blockquote':
      return text ? `> ${text}` : '>';
    case 'code-block':
      return text ? ['```', text, '```'].join('\n') : '';
    case 'atomic':
      return renderAtomicMarkdown(block, entities);
    default:
      return text;
  }
}

export function draftJsToMarkdown(input: DraftJsContent | DraftJsBlock[] | string | undefined): string {
  const entities = !input || typeof input === 'string' || Array.isArray(input)
    ? {}
    : normalizeEntityMap(input.entityMap);

  const rendered = normalizeBlocks(input)
    .map((block) => renderBlock(block, entities))
    .filter((line) => line.length > 0);

  return rendered.join('\n\n').trim();
}
