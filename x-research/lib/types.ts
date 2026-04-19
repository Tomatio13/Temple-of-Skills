export type OutputFormat = 'markdown' | 'json' | 'both';
export type LanguageBucket = 'ja' | 'other';
export type SearchMode = 'articles' | 'posts';

export interface ResearchRequest {
  minFaves?: number;
  since?: string;
  until?: string;
  query?: string;
  outputFormat?: OutputFormat;
  searchMode?: SearchMode;
  maxPages?: number;
  maxItems?: number;
  languageFilter?: LanguageBucket | 'all';
  fetchFullArticle?: boolean;
  type?: 'Latest' | 'Top';
}

export interface SearchUser {
  id_str?: string;
  name?: string;
  screen_name?: string;
  description?: string;
  location?: string;
  followers_count?: number;
}

export interface SearchTweetHit {
  id_str: string;
  full_text: string;
  favorite_count: number;
  retweet_count: number;
  reply_count: number;
  quote_count: number;
  bookmark_count?: number;
  views_count?: number;
  lang?: string;
  tweet_created_at?: string;
  user: SearchUser;
}

export interface DraftJsBlock {
  key?: string;
  text?: string;
  type?: string;
  depth?: number;
  inlineStyleRanges?: Array<{
    offset?: number;
    length?: number;
    style?: string;
  }>;
  entityRanges?: Array<{
    offset?: number;
    length?: number;
    key?: number | string;
  }>;
  data?: Record<string, unknown>;
}

export interface DraftJsContent {
  blocks?: DraftJsBlock[];
  entityMap?: Record<string, unknown> | Array<{
    key?: string;
    value?: Record<string, unknown>;
  }>;
}

export interface ArticlePayload {
  title?: string;
  subtitle?: string;
  author?: string;
  description?: string;
  preview_text?: string;
  blocks?: DraftJsBlock[];
  draft_js?: DraftJsContent;
  content_state?: DraftJsContent;
  content?: DraftJsContent | DraftJsBlock[] | string;
}

export interface ArticleDetailResponse {
  id_str?: string;
  full_text?: string | null;
  article?: ArticlePayload | null;
  user?: SearchUser;
  favorite_count?: number;
  retweet_count?: number;
  reply_count?: number;
  quote_count?: number;
  bookmark_count?: number;
  views_count?: number;
  tweet_created_at?: string;
}

export interface NormalizedArticle {
  id: string;
  sourceType: SearchMode;
  title: string;
  subtitle?: string;
  author: string;
  authorHandle: string;
  languageBucket: LanguageBucket;
  summaryText: string;
  markdown: string;
  tweetText: string;
  createdAt?: string;
  favoriteCount: number;
  retweetCount: number;
  replyCount: number;
  quoteCount: number;
  bookmarkCount: number;
  viewsCount: number;
  engagementScore: number;
  url: string;
}

export interface ResearchReport {
  version: string;
  generatedAt: string;
  request: Required<Pick<ResearchRequest, 'outputFormat' | 'fetchFullArticle' | 'languageFilter'>> & ResearchRequest;
  query: string;
  stats: {
    totalSearchHits: number;
    afterLanguageFilter: number;
    articleDetailsFetched: number;
    articleDetailsFromCache: number;
    dedupedArticles: number;
  };
  articles: NormalizedArticle[];
  markdown: string;
}
