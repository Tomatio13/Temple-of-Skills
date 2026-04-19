import type { NormalizedArticle, ResearchReport } from './types';

function renderArticle(article: NormalizedArticle, index: number): string {
  const parts = [
    `### ${index + 1}. ${article.title}`,
    `- Source type: ${article.sourceType}`,
    `- Author: ${article.author} (@${article.authorHandle})`,
    `- Language: ${article.languageBucket}`,
    `- Likes: ${article.favoriteCount} | Retweets: ${article.retweetCount} | Replies: ${article.replyCount} | Quotes: ${article.quoteCount} | Bookmarks: ${article.bookmarkCount} | Views: ${article.viewsCount}`,
    `- URL: ${article.url}`,
  ];

  if (article.subtitle) {
    parts.push(`- Subtitle: ${article.subtitle}`);
  }

  if (article.summaryText) {
    parts.push('', article.summaryText);
  }

  if (article.markdown) {
    parts.push('', article.markdown);
  }

  return parts.join('\n');
}

export function renderMarkdownReport(report: Omit<ResearchReport, 'markdown'>): string {
  const header = [
    '# SocialData X Article Research Report',
    '',
    `- Generated at: ${report.generatedAt}`,
    `- Version: ${report.version}`,
    `- Query: \`${report.query}\``,
    `- Search hits: ${report.stats.totalSearchHits}`,
    `- After language filter: ${report.stats.afterLanguageFilter}`,
    `- Article details fetched: ${report.stats.articleDetailsFetched}`,
    `- Article details from cache: ${report.stats.articleDetailsFromCache}`,
    `- Deduped articles: ${report.stats.dedupedArticles}`,
    '',
    '## Articles',
    '',
  ].join('\n');

  const body = report.articles.length > 0
    ? report.articles.map(renderArticle).join('\n\n')
    : '_No matching articles found._';

  return `${header}${body}`.trim();
}

export function formatOutput(report: ResearchReport): string {
  switch (report.request.outputFormat) {
    case 'json':
      return JSON.stringify(report, null, 2);
    case 'both':
      return [
        '## Markdown Report',
        '',
        report.markdown,
        '',
        '## JSON Payload',
        '',
        '```json',
        JSON.stringify(report, null, 2),
        '```',
      ].join('\n');
    case 'markdown':
    default:
      return report.markdown;
  }
}
