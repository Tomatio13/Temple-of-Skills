import type { SearchUser, LanguageBucket } from './types';

const JAPANESE_CHAR_REGEX = /[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff66-\uff9f]/;

export function classifyProfileLanguage(user: SearchUser | undefined): LanguageBucket {
  const samples = [
    user?.name,
    user?.description,
    user?.location,
  ].filter((value): value is string => Boolean(value && value.trim()));

  return samples.some((value) => JAPANESE_CHAR_REGEX.test(value)) ? 'ja' : 'other';
}
