import { draftJsToMarkdown } from './draftjs-to-markdown';
import { classifyProfileLanguage } from './language';
import { buildSearchQuery } from './query-builder';
import { renderMarkdownReport } from './report';
import { getArticleDetail, searchTweets } from './socialdata-client';
import type {
  ArticleDetailResponse,
  DraftJsBlock,
  NormalizedArticle,
  ResearchReport,
  ResearchRequest,
  SearchTweetHit,
} from './types';

function normalizeComparableText(value: string): string {
  return value
    .replace(/\s+/g, ' ')
    .replace(/[*#>`_-]/g, '')
    .trim()
    .toLowerCase();
}

function stripDuplicatedSummary(markdown: string, summaryText: string): string {
  if (!markdown || !summaryText) {
    return markdown;
  }

  const normalizedMarkdown = normalizeComparableText(markdown);
  const normalizedSummary = normalizeComparableText(summaryText);

  if (!normalizedSummary || !normalizedMarkdown.startsWith(normalizedSummary)) {
    return markdown;
  }

  const summaryLines = summaryText.split(/\r?\n/).length;
  const markdownLines = markdown.split(/\r?\n/);
  return markdownLines.slice(summaryLines).join('\n').trim();
}

function articleBlocks(detail: ArticleDetailResponse): DraftJsBlock[] | string | undefined {
  const article = detail.article;
  if (!article) return detail.full_text ?? undefined;
  if (Array.isArray(article.blocks)) return article.blocks;
  if (article.draft_js) return article.draft_js;
  if (article.content_state) return article.content_state;
  if (article.content) return article.content;
  return detail.full_text ?? undefined;
}

function buildNormalizedArticle(hit: SearchTweetHit, detail: ArticleDetailResponse): NormalizedArticle {
  const languageBucket = classifyProfileLanguage(hit.user);
  const rawMarkdown = draftJsToMarkdown(articleBlocks(detail));
  const hasArticlePayload = Boolean(detail.article);
  const title = detail.article?.title?.trim() || hit.full_text.trim().slice(0, 100) || '(untitled)';
  const author = detail.article?.author?.trim() || hit.user.name?.trim() || 'Unknown author';
  const authorHandle = hit.user.screen_name?.trim() || 'unknown';
  const summaryText =
    detail.article?.description?.trim() ||
    detail.article?.preview_text?.trim() ||
    detail.article?.subtitle?.trim() ||
    '';
  const markdown = stripDuplicatedSummary(rawMarkdown, summaryText);
  const favoriteCount = detail.favorite_count ?? hit.favorite_count ?? 0;
  const retweetCount = detail.retweet_count ?? hit.retweet_count ?? 0;
  const replyCount = detail.reply_count ?? hit.reply_count ?? 0;
  const quoteCount = detail.quote_count ?? hit.quote_count ?? 0;
  const bookmarkCount = detail.bookmark_count ?? hit.bookmark_count ?? 0;
  const viewsCount = detail.views_count ?? hit.views_count ?? 0;

  return {
    id: hit.id_str,
    sourceType: hasArticlePayload ? 'articles' : 'posts',
    title,
    subtitle: detail.article?.subtitle?.trim(),
    author,
    authorHandle,
    languageBucket,
    summaryText,
    markdown,
    tweetText: hit.full_text,
    createdAt: detail.tweet_created_at ?? hit.tweet_created_at,
    favoriteCount,
    retweetCount,
    replyCount,
    quoteCount,
    bookmarkCount,
    viewsCount,
    engagementScore: favoriteCount + retweetCount + replyCount + quoteCount + bookmarkCount,
    url: `https://x.com/${authorHandle}/status/${hit.id_str}`,
  };
}

export function dedupeAndSortArticles(articles: NormalizedArticle[]): NormalizedArticle[] {
  const deduped = new Map<string, NormalizedArticle>();

  for (const article of articles) {
    const key = `${article.title.toLowerCase()}::${article.author.toLowerCase()}`;
    const previous = deduped.get(key);
    if (!previous || article.favoriteCount > previous.favoriteCount) {
      deduped.set(key, article);
    }
  }

  return Array.from(deduped.values()).sort((a, b) => {
    if (b.engagementScore !== a.engagementScore) {
      return b.engagementScore - a.engagementScore;
    }
    return b.favoriteCount - a.favoriteCount;
  });
}

export async function runResearch(rawRequest: ResearchRequest): Promise<ResearchReport> {
  const request: Required<Pick<ResearchRequest, 'outputFormat' | 'fetchFullArticle' | 'languageFilter'>> & ResearchRequest = {
    outputFormat: rawRequest.outputFormat ?? 'markdown',
    fetchFullArticle: rawRequest.fetchFullArticle ?? true,
    languageFilter: rawRequest.languageFilter ?? 'all',
    searchMode: rawRequest.searchMode ?? 'articles',
    ...rawRequest,
  };

  const query = buildSearchQuery(request);
  const maxPages = Math.max(1, Math.min(request.maxPages ?? 5, 20));
  const maxItems = Math.max(1, request.maxItems ?? 50);

  const hits: SearchTweetHit[] = [];
  let cursor: string | undefined;

  for (let page = 0; page < maxPages; page += 1) {
    const response = await searchTweets({ query, cursor, type: request.type ?? 'Latest' });
    if (Array.isArray(response.tweets)) {
      hits.push(...response.tweets);
    }

    cursor = response.next_cursor;
    if (!cursor || hits.length >= maxItems) {
      break;
    }
  }

  const uniqueHits = Array.from(new Map(hits.map((hit) => [hit.id_str, hit])).values()).slice(0, maxItems);

  const languageFilteredHits = request.languageFilter === 'all'
    ? uniqueHits
    : uniqueHits.filter((hit) => classifyProfileLanguage(hit.user) === request.languageFilter);

  const articles: NormalizedArticle[] = [];
  let articleDetailsFetched = 0;
  let articleDetailsFromCache = 0;

  for (const hit of languageFilteredHits) {
    if (!request.fetchFullArticle || request.searchMode === 'posts') {
      articles.push(buildNormalizedArticle(hit, { full_text: hit.full_text, user: hit.user }));
      continue;
    }

    const { data, fromCache } = await getArticleDetail(hit.id_str);
    if (fromCache) {
      articleDetailsFromCache += 1;
    } else {
      articleDetailsFetched += 1;
    }
    articles.push(buildNormalizedArticle(hit, data));
  }

  const dedupedArticles = dedupeAndSortArticles(articles);
  const version = '1';
  const generatedAt = new Date().toISOString();

  const reportWithoutMarkdown = {
    version,
    generatedAt,
    request,
    query,
    stats: {
      totalSearchHits: uniqueHits.length,
      afterLanguageFilter: languageFilteredHits.length,
      articleDetailsFetched,
      articleDetailsFromCache,
      dedupedArticles: dedupedArticles.length,
    },
    articles: dedupedArticles,
  };

  return {
    ...reportWithoutMarkdown,
    markdown: renderMarkdownReport(reportWithoutMarkdown),
  };
}
