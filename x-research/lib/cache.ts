import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';

const CACHE_ROOT = join(process.cwd(), '.cache', 'socialdata-x-research');

function buildPath(scope: string, key: string): string {
  const hash = createHash('sha1').update(key).digest('hex');
  return join(CACHE_ROOT, scope, `${hash}.json`);
}

export function readJsonCache<T>(scope: string, key: string): T | null {
  const filePath = buildPath(scope, key);
  if (!existsSync(filePath)) {
    return null;
  }

  try {
    return JSON.parse(readFileSync(filePath, 'utf8')) as T;
  } catch {
    return null;
  }
}

export function writeJsonCache(scope: string, key: string, value: unknown): void {
  const filePath = buildPath(scope, key);
  mkdirSync(dirname(filePath), { recursive: true });
  writeFileSync(filePath, JSON.stringify(value, null, 2));
}
