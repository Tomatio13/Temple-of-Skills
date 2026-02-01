#!/usr/bin/env python3
"""
生成されたMarkdownファイルに対してmarkdownlint-cli2を実行し、
エラーがなくなるまで修正を試みるスクリプト
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_markdownlint(target_file: Path, fix: bool = False) -> tuple[int, str, str]:
    """markdownlint-cli2を実行し、結果を返す"""
    cmd = ["markdownlint-cli2"]
    if fix:
        cmd.append("--fix")
    cmd.append(str(target_file))

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def main():
    parser = argparse.ArgumentParser(description="MarkdownファイルのLintと自動修正")
    parser.add_argument('file', help='対象のMarkdownファイルパス')
    parser.add_argument('--max-attempts', type=int, default=5,
                        help='自動修正の最大試行回数 (デフォルト: 5)')
    args = parser.parse_args()

    target_file = Path(args.file).expanduser().resolve()

    if not target_file.exists():
        print(f"エラー: ファイルが見つかりません: {target_file}", file=sys.stderr)
        sys.exit(1)

    if not target_file.suffix == '.md':
        print(f"警告: 拡張子が.mdではありません: {target_file}", file=sys.stderr)

    print(f"対象ファイル: {target_file}")
    print("-" * 60)

    # まずはLintのみ実行
    returncode, stdout, stderr = run_markdownlint(target_file, fix=False)

    if returncode == 0:
        print("✅ Lintエラーはありません。")
        return

    print(f"❌ Lintエラーが検出されました:\n{stdout}")
    print("-" * 60)

    # 自動修正を試行
    for attempt in range(1, args.max_attempts + 1):
        print(f"自動修正試行 {attempt}/{args.max_attempts}...")

        returncode, stdout, stderr = run_markdownlint(target_file, fix=True)

        # 修正後の再チェック
        returncode_check, stdout_check, stderr_check = run_markdownlint(target_file, fix=False)

        if returncode_check == 0:
            print("✅ すべてのエラーが修正されました。")
            return

        if stdout == stdout_check:
            # 変化がない場合は打ち切り
            print(f"⚠️  これ以上自動修正できません。")
            break

        print(f"修正後のエラー:\n{stdout_check}")
        print("-" * 60)

    print("\n📋 以下のエラーは手動修正が必要です:")
    print(stdout_check)
    print(f"\n対象ファイル: {target_file}")
    print("\n修正後、再度実行してください:")
    print(f"  markdownlint-cli2 {target_file}")

    sys.exit(1)


if __name__ == '__main__':
    main()
