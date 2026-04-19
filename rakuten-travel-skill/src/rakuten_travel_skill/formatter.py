"""User-facing formatting helpers."""

from __future__ import annotations

from .vacant_search import VacancySearchResponse, summarize_hotels


def format_search_response(response: VacancySearchResponse) -> str:
    request = response.request
    resolved = response.resolved_area
    summarized = summarize_hotels(response.plans, limit=10)
    paging = {}
    if response.raw_payload:
        paging = response.raw_payload.get("pagingInfo") or {}
    lines = [
        "検索条件の確認",
        f"- 場所: {request.location}",
        (
            f"- 解決した地区: {resolved.large_class_name} / {resolved.middle_class_name} / "
            f"{resolved.small_class_name} / {resolved.detail_class_name}"
        ),
        f"- 日程: {request.checkin_date.isoformat()} から {request.checkout_date.isoformat()}",
        f"- 人数: {request.adult_count}名 / {request.room_num}室",
    ]
    if response.search_scope != "detail":
        lines.append(f"- 検索範囲: 0件だったため {response.search_scope} 単位まで広げて再検索")
    if request.min_charge is not None or request.max_charge is not None:
        lines.append(
            f"- 料金帯: {request.min_charge or 0}円 から "
            f"{request.max_charge or '上限なし'}円"
        )
    if request.squeeze_conditions:
        lines.append(f"- 条件: {', '.join(request.squeeze_conditions)}")

    lines.append("")
    lines.append("件数情報")
    lines.append(f"- API総件数: {response.total_count if response.total_count is not None else '不明'}件")
    lines.append(f"- 表示件数: {len(summarized)}件")
    if paging:
        lines.append(
            f"- ページ: {paging.get('page', '?')} / {paging.get('pageCount', '?')} "
            f"(API取得範囲 {paging.get('first', '?')} - {paging.get('last', '?')})"
        )
    lines.append(f"- 取得ページ数: {response.pages_fetched}ページ")

    lines.append("")
    lines.append("候補ホテル一覧")
    if not response.plans:
        lines.append("- 空室は見つかりませんでした。条件を緩めるか、場所を絞り直してください。")
    else:
        for index, plan in enumerate(summarized, start=1):
            lines.append(
                f"{index}. {plan.hotel_name}"
                + (f" | {plan.plan_name}" if plan.plan_name else "")
            )
            lines.append(f"   料金: {_format_charge(plan)} / 評価: {plan.review_average or '未評価'}")
            address = "".join(filter(None, [plan.address1, plan.address2])) or "住所不明"
            lines.append(f"   住所: {address}")
            lines.append(f"   詳細: {plan.hotel_information_url or 'URL不明'}")

    lines.append("")
    lines.append("注意事項")
    lines.append("- 最終的な空室状況と料金は楽天トラベル画面で再確認してください。")
    lines.append("- 地区コードの解決結果が意図と違う場合は、地名をより具体的に指定してください。")
    return "\n".join(lines)


def format_error(message: str, *, retryable: bool) -> str:
    lines = [
        "空室検索に失敗しました。",
        f"- 詳細: {message}",
        f"- 再試行可否: {'可能' if retryable else '入力修正が必要'}",
    ]
    return "\n".join(lines)


def _format_charge(plan) -> str:
    if plan.charge is None and plan.total_charge is None:
        return "不明"
    if plan.charge_flag == 0:
        if plan.total_charge is not None and plan.charge is not None:
            return f"{plan.charge}円/人 (合計 {plan.total_charge}円)"
        if plan.charge is not None:
            return f"{plan.charge}円/人"
    if plan.charge_flag == 1:
        if plan.total_charge is not None:
            return f"{plan.total_charge}円/室"
        if plan.charge is not None:
            return f"{plan.charge}円/室"
    if plan.total_charge is not None:
        return f"{plan.total_charge}円"
    return f"{plan.charge}円"
