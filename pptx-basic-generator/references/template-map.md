# Template Map (basic_generator.py)

Use this as a quick schema reference when editing `SLIDE_CONTENT`.

## Slide ID -> Template

- `1: cover`
- `2: list`
- `3: chart_left_text_right`
- `4: text_left_chart_right`
- `5: table_left_text_right`
- `6: text_left_chart_right`
- `7: card_grid`
- `8: text_left_image_right`
- `9: three_points_circle`
- `10: point_list_compact`
- `11: point_list_large`
- `12: timeline`

## Core Rules

- `SLIDES_TO_USE` controls output order.
- `SLIDE_CONTENT` keys are output index (`1..N`), not template ID.
- Data is merged: `SLIDE_TEMPLATES[slide_id].default_data` <- `SLIDE_CONTENT[output_index]`.

## Template IDs

1. `cover`
- Keys: `title`, `subtitle`, `credit`

2. `list`
- Keys: `title`, `subtitle`, `items[]`

3. `chart_left_text_right`
- Keys: `title`, `subtitle`, `chart_type` (`COLUMN_CLUSTERED`), `categories[]`, `series[]`, `text_items[]`

4. `text_left_chart_right`
- Keys: `title`, `subtitle`, `chart_type` (`PIE`), `categories[]`, `series[]`, `text_items[]`

5. `table_left_text_right`
- Keys: `title`, `subtitle`, `columns[]`, `rows[][]`, `text_items[]`

6. `text_left_chart_right`
- Keys: `title`, `subtitle`, `chart_type` (`LINE`), `categories[]`, `series[]`, `text_items[]`

7. `card_grid`
- Keys: `title`, `subtitle`, `items[]`
- Recommended: up to 4 items

8. `text_left_image_right`
- Keys: `title`, `subtitle`, `text_items[]`
- Notes: layout shows image placeholder (`Image Area`) unless template code is extended for real image insertion

9. `three_points_circle`
- Keys: `title`, `subtitle`, `items[]`
- Recommended: exactly 3 items

10. `point_list_compact`
- Keys: `title`, `subtitle`, `items[]`
- Recommended: up to 4 items

11. `point_list_large`
- Keys: `items[]`
- Recommended: up to 3 items

12. `timeline`
- Keys: `title`, `subtitle`, `timeline_items[]`
- `timeline_items` item schema: `{ "year": "...", "title": "...", "description": "..." }`
- Hard cap: 4 items

## Chart Constraints

- For non-PIE chart:
  - each series: `{ "name": str, "values": list[number] }`
  - `len(values)` must match `len(categories)`

- For PIE chart:
  - only first series is used by renderer
  - prefer one series

## Table Constraints

- `rows` can be variable-length overall, but each row should have column count equal to `len(columns)`.
- Header row is auto-generated from `columns`.
