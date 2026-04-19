import { formatOutput } from '../lib/report';
import { runResearch } from '../lib/research';
import type { OutputFormat, ResearchRequest, SearchMode } from '../lib/types';

function parseArgs(argv: string[]): ResearchRequest {
  const request: ResearchRequest = {};

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];

    switch (arg) {
      case '--query':
        request.query = next;
        index += 1;
        break;
      case '--min-faves':
        request.minFaves = Number(next);
        index += 1;
        break;
      case '--since':
        request.since = next;
        index += 1;
        break;
      case '--until':
        request.until = next;
        index += 1;
        break;
      case '--language-filter':
        if (next === 'ja' || next === 'other' || next === 'all') {
          request.languageFilter = next;
        }
        index += 1;
        break;
      case '--output-format':
        if (next === 'markdown' || next === 'json' || next === 'both') {
          request.outputFormat = next as OutputFormat;
        }
        index += 1;
        break;
      case '--search-mode':
        if (next === 'articles' || next === 'posts') {
          request.searchMode = next as SearchMode;
        }
        index += 1;
        break;
      case '--max-pages':
        request.maxPages = Number(next);
        index += 1;
        break;
      case '--max-items':
        request.maxItems = Number(next);
        index += 1;
        break;
      case '--type':
        if (next === 'Latest' || next === 'Top') {
          request.type = next;
        }
        index += 1;
        break;
      case '--skip-full-article':
        request.fetchFullArticle = false;
        break;
      default:
        break;
    }
  }

  return request;
}

async function main(): Promise<void> {
  const request = parseArgs(process.argv.slice(2));
  const report = await runResearch(request);
  console.log(formatOutput(report));
}

await main();
