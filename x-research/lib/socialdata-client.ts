import { readJsonCache, writeJsonCache } from './cache';
import type { ArticleDetailResponse, SearchTweetHit } from './types';

export interface SearchResponse {
  tweets?: SearchTweetHit[];
  next_cursor?: string;
  status?: string;
  message?: string;
}

function getApiKey(): string {
  const apiKey = process.env.SOCIALDATA_API_KEY;
  if (!apiKey || !apiKey.trim()) {
    throw new Error('SOCIALDATA_API_KEY is not set');
  }
  return apiKey.trim();
}

async function getJson<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${getApiKey()}`,
      Accept: 'application/json',
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`SocialData API ${response.status}: ${body.slice(0, 400)}`);
  }

  return (await response.json()) as T;
}

export async function searchTweets(params: {
  query: string;
  cursor?: string;
  type?: 'Latest' | 'Top';
}): Promise<SearchResponse> {
  const url = new URL('https://api.socialdata.tools/twitter/search');
  url.searchParams.set('query', params.query);
  url.searchParams.set('type', params.type ?? 'Latest');
  if (params.cursor) {
    url.searchParams.set('cursor', params.cursor);
  }

  return getJson<SearchResponse>(url.toString());
}

export async function getArticleDetail(articleId: string): Promise<{
  data: ArticleDetailResponse;
  fromCache: boolean;
}> {
  const cached = readJsonCache<ArticleDetailResponse>('article-detail', articleId);
  if (cached) {
    return { data: cached, fromCache: true };
  }

  const url = `https://api.socialdata.tools/twitter/article/${articleId}`;
  const data = await getJson<ArticleDetailResponse>(url);
  writeJsonCache('article-detail', articleId, data);
  return { data, fromCache: false };
}
