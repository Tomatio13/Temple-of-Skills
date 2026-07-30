#!/bin/bash
# gh-stars-activity: GitHubスター付きリポジトリの更新状況をJST日時付きで一覧表示
# Usage: stars_activity.sh [日付(YYYY-MM-DD)] [--json] [--limit=N|--limit N] [--releases-only]
set -euo pipefail

# Defaults
SINCE=""
JSON_MODE=false
LIMIT=0
RELEASES_ONLY=false

# Parse arguments
while [ "$#" -gt 0 ]; do
	arg="$1"
	case "$arg" in
	--json) JSON_MODE=true ;;
	--releases-only) RELEASES_ONLY=true ;;
	--limit=*) LIMIT="${arg#--limit=}" ;;
	--limit)
		shift
		if [ "$#" -eq 0 ] || ! [[ "$1" =~ ^[0-9]+$ ]]; then
			echo "Error: --limit requires a numeric value." >&2
			exit 1
		fi
		LIMIT="$1"
		;;
	*)
		if [[ "$arg" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
			SINCE="$arg"
		else
			echo "Error: Unknown argument: $arg" >&2
			exit 1
		fi
		;;
	esac
	shift
done

if ! [[ "$LIMIT" =~ ^[0-9]+$ ]]; then
	echo "Error: --limit must be a non-negative integer." >&2
	exit 1
fi

# Default: 2 days ago in JST
SINCE="${SINCE:-$(TZ=Asia/Tokyo date -d '2 days ago' +"%Y-%m-%d")}"

if ! command -v gh &>/dev/null; then
	echo "Error: gh (GitHub CLI) is required. Install from https://cli.github.com/" >&2
	exit 1
fi

if ! gh auth status &>/dev/null; then
	echo "Error: Not authenticated. Run 'gh auth login' first." >&2
	exit 1
fi

fetch_commits() {
	local repo="$1" branch="$2"
	gh api "repos/$repo/commits?sha=$branch&per_page=3" \
		-q '.[] | "\(.sha[:7])\t\(.commit.message | split("\n")[0])"' ||
		echo "Warning: Failed to fetch commits for $repo." >&2
}

fetch_release() {
	local repo="$1" since="$2"
	gh api "repos/$repo/releases?per_page=1" \
		-q ".[0] | select(.published_at >= \"${since}\") | .tag_name" ||
		echo "Warning: Failed to fetch release for $repo." >&2
}

fetch_release_body() {
	local repo="$1" since="$2"
	gh api "repos/$repo/releases?per_page=1" \
		-q ".[0] | select(.published_at >= \"${since}\") | \"\(.tag_name)\t\(.body // \"\")\"" ||
		echo "Warning: Failed to fetch release body for $repo." >&2
}

fetch_starred_repos() {
	gh api user/starred --paginate \
		-q '.[] | select(.pushed_at[:10] >= "'"$SINCE"'") | "\(.pushed_at)|\(.full_name)|\(.default_branch)"' |
		sort -t'|' -k1 -r
}

if $RELEASES_ONLY; then
	# Fetch all starred repos updated since SINCE, then filter to those with recent releases
	if ! REPOS=$(fetch_starred_repos); then
		echo "Error: Failed to fetch starred repositories. Check GitHub API access, rate limits, or network connectivity." >&2
		exit 1
	fi

	if [ -z "$REPOS" ]; then
		echo "$SINCE 以降に更新されたスター付きリポジトリはありません。"
		exit 0
	fi

	# Filter: only repos with a recent release
	FILTERED=""
	while IFS='|' read -r pushed repo branch; do
		[ -z "$repo" ] && continue
		release=$(fetch_release "$repo" "$SINCE")
		if [ -n "$release" ]; then
			FILTERED="${FILTERED}${pushed}|${repo}|${branch}|${release}"$'\n'
		fi
	done < <(echo "$REPOS")
	FILTERED=$(echo "$FILTERED" | sed '/^$/d')

	if [ -z "$FILTERED" ]; then
		echo "$SINCE 以降にリリースのあったスター付きリポジトリはありません。"
		exit 0
	fi

	# Apply limit
	if [ "$LIMIT" -gt 0 ]; then
		FILTERED=$(echo "$FILTERED" | head -n "$LIMIT")
	fi

	count=0

	if $JSON_MODE; then
		echo "["
		first=true
		while IFS='|' read -r pushed repo branch release; do
			[ -z "$repo" ] && continue
			count=$((count + 1))
			jst=$(TZ=Asia/Tokyo date -d "$pushed" +"%Y/%m/%d %H:%M" 2>/dev/null || echo "$pushed")

			$first || echo ","
			first=false
			release_escaped=$(echo "$release" | sed 's/"/\\"/g')
			printf '  {"datetime":"%s","repo":"%s","release":"%s"}' "$jst" "$repo" "$release_escaped"
		done < <(echo "$FILTERED")
		echo ""
		echo "]"
	else
		while IFS='|' read -r pushed repo branch release; do
			[ -z "$repo" ] && continue
			count=$((count + 1))
			jst=$(TZ=Asia/Tokyo date -d "$pushed" +"%Y/%m/%d %H:%M" 2>/dev/null || echo "$pushed")

			# Fetch release body for changelog excerpt
			body_raw=$(fetch_release_body "$repo" "$SINCE")
			body_text=""
			if [ -n "$body_raw" ]; then
				body_text=$(echo "$body_raw" | cut -f2- | head -5 | sed 's/^/  /')
			fi

			printf "\n%s  %s [%s]\n" "$jst" "$repo" "$release"
			if [ -n "$body_text" ]; then
				echo "$body_text"
			fi
		done < <(echo "$FILTERED")
		echo ""
		echo "---"
		echo "合計: $count 件 ($SINCE 以降のリリース、JST)"
	fi
else
	# Default mode: show all updated repos
	if ! REPOS=$(fetch_starred_repos); then
		echo "Error: Failed to fetch starred repositories. Check GitHub API access, rate limits, or network connectivity." >&2
		exit 1
	fi

	if [ -z "$REPOS" ]; then
		echo "$SINCE 以降に更新されたスター付きリポジトリはありません。"
		exit 0
	fi

	# Apply limit if specified
	if [ "$LIMIT" -gt 0 ]; then
		REPOS=$(echo "$REPOS" | head -n "$LIMIT")
	fi

	count=0

	if $JSON_MODE; then
		echo "["
		first=true
		while IFS='|' read -r pushed repo branch; do
			[ -z "$repo" ] && continue
			count=$((count + 1))
			jst=$(TZ=Asia/Tokyo date -d "$pushed" +"%Y/%m/%d %H:%M" 2>/dev/null || echo "$pushed")
			release=$(fetch_release "$repo" "$SINCE")
			commits_raw=$(fetch_commits "$repo" "$branch")

			commits_json=""
			while IFS=$'\t' read -r sha subject; do
				[ -z "$sha" ] && continue
				escaped=$(echo "$subject" | sed 's/"/\\"/g')
				[ -n "$commits_json" ] && commits_json+=","
				commits_json+="{\"sha\":\"$sha\",\"subject\":\"$escaped\"}"
			done <<<"$commits_raw"

			release_json="null"
			[ -n "$release" ] && release_json="\"$release\""

			$first || echo ","
			first=false
			printf '  {"datetime":"%s","repo":"%s","release":%s,"commits":[%s]}' \
				"$jst" "$repo" "$release_json" "$commits_json"
		done < <(echo "$REPOS")
		echo ""
		echo "]"
	else
		while IFS='|' read -r pushed repo branch; do
			[ -z "$repo" ] && continue
			count=$((count + 1))
			jst=$(TZ=Asia/Tokyo date -d "$pushed" +"%Y/%m/%d %H:%M" 2>/dev/null || echo "$pushed")
			release=$(fetch_release "$repo" "$SINCE")
			[ -n "$release" ] && release_label=" [$release]" || release_label=""

			commits_raw=$(fetch_commits "$repo" "$branch")

			printf "\n%s  %s%s\n" "$jst" "$repo" "$release_label"
			if [ -n "$commits_raw" ]; then
				while IFS=$'\t' read -r sha subject; do
					[ -z "$sha" ] && continue
					echo "  - $subject"
				done <<<"$commits_raw"
			else
				echo "  - (取得できませんでした)"
			fi
		done < <(echo "$REPOS")
		echo ""
		echo "---"
		echo "合計: $count 件 ($SINCE 以降、JST)"
	fi
fi
