import type { ResearchRequest } from './types';

function sanitizeQueryTerm(value: string): string {
  return value.trim().replace(/\s+/g, ' ');
}

export function buildSearchQuery(request: ResearchRequest): string {
  const searchMode = request.searchMode ?? 'articles';
  const parts: string[] = [];

  if (searchMode === 'articles') {
    parts.push('url:x.com/i/article');
  }

  parts.push('-filter:replies');

  if (typeof request.minFaves === 'number' && request.minFaves > 0) {
    parts.push(`min_faves:${request.minFaves}`);
  }

  if (request.since) {
    parts.push(`since:${request.since}`);
  }

  if (request.until) {
    parts.push(`until:${request.until}`);
  }

  if (request.query) {
    parts.unshift(sanitizeQueryTerm(request.query));
  }

  return parts.join(' ').trim();
}
