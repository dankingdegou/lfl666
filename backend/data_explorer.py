"""Day 1 数据探查脚本：只读取并统计课程订单数据，不修改原始文件。"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "sales_orders.csv"
TOP_N = 10


def format_path(file_path: Path) -> str:
    """将项目内路径格式化为便于阅读的相对路径。"""
    try:
        return str(file_path.resolve().relative_to(PROJECT_ROOT))
    except ValueError:
        return str(file_path.resolve())


def load_data(file_path: Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    使用课程规定的 UTF-8-SIG 编码读取 CSV 数据。

    Args:
        file_path: 待读取的 CSV 文件路径。

    Returns:
        读取完成的 pandas DataFrame。
    """
    return pd.read_csv(file_path, encoding="utf-8-sig")


def show_basic_info(df: pd.DataFrame) -> None:
    """
    输出数据规模以及各字段的数据类型和非空数量。

    Args:
        df: 待探查的 pandas DataFrame。
    """
    print("\n=== 1. 数据规模 ===")
    print(f"数据规模：{df.shape[0]} 行 × {df.shape[1]} 列")

    print("\n=== 2. 列信息 ===")
    column_info = pd.DataFrame(
        {
            "列名": df.columns,
            "数据类型": [str(dtype) for dtype in df.dtypes],
            "非空数据数量": df.notna().sum().to_numpy(),
        }
    )
    print(column_info.to_string(index=False))


def analyze_missing_values(df: pd.DataFrame) -> None:
    """
    统计各字段的缺失值数量和缺失比例，仅输出结果而不清洗数据。

    Args:
        df: 待探查的 pandas DataFrame。
    """
    print("\n=== 3. 缺失值统计 ===")
    missing_count = df.isna().sum()
    missing_rate = missing_count.div(len(df)).mul(100)
    missing_summary = pd.DataFrame(
        {
            "字段": df.columns,
            "缺失值数量": missing_count.to_numpy(),
            "缺失率(%)": missing_rate.round(2).to_numpy(),
        }
    )
    print(missing_summary.to_string(index=False))


def analyze_duplicates(df: pd.DataFrame) -> None:
    """
    统计完全重复行的数量，不删除或修改任何记录。

    Args:
        df: 待探查的 pandas DataFrame。
    """
    print("\n=== 4. 重复行统计 ===")
    duplicate_count = int(df.duplicated().sum())
    print(f"完全重复行数量：{duplicate_count}")


def analyze_numeric_columns(df: pd.DataFrame) -> None:
    """
    自动识别数值列并输出描述性统计量。

    Args:
        df: 待探查的 pandas DataFrame。
    """
    print("\n=== 5. 数值列统计 ===")
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        print("当前数据集中未检测到数值列。")
        return

    # 转置后每个字段占一行，便于同时查看多个数值字段。
    print(numeric_df.describe().T.to_string())


def analyze_categorical_columns(df: pd.DataFrame, top_n: int = TOP_N) -> None:
    """
    输出非数值字段的唯一值数量和最常见类别分布。

    Args:
        df: 待探查的 pandas DataFrame。
        top_n: 每个字段最多展示的高频类别数量。
    """
    print("\n=== 6. 分类列分布 ===")
    categorical_df = df.select_dtypes(exclude="number")
    if categorical_df.shape[1] == 0:
        print("当前数据集中未检测到分类列。")
        return

    for column in categorical_df.columns:
        unique_count = int(categorical_df[column].nunique(dropna=True))
        print(f"\n字段：{column}")
        print(f"非空唯一值数量：{unique_count}")
        print(f"最常见的前 {top_n} 个值（包含缺失值）：")

        # 限制高基数字段的输出，避免打印成百上千行。
        value_counts = categorical_df[column].value_counts(dropna=False).head(top_n)
        distribution = value_counts.rename_axis("类别").reset_index(name="数量")
        print(distribution.to_string(index=False))


def run_exploration(file_path: Path = DEFAULT_DATA_PATH) -> bool:
    """
    执行完整的 Day 1 数据探查流程。

    Args:
        file_path: 待探查的 CSV 文件路径。

    Returns:
        探查成功返回 True，数据缺失或读取失败返回 False。
    """
    file_path = Path(file_path)
    display_path = format_path(file_path)

    if not file_path.is_file():
        print(f"未找到数据文件：\n{display_path}\n")
        print("请将课程提供的 sales_orders.csv 放入 data/ 目录后重新运行。")
        return False

    try:
        df = load_data(file_path)
    except pd.errors.EmptyDataError:
        print(f"数据文件为空，无法执行数据探查。\n文件路径：{display_path}")
        return False
    except UnicodeDecodeError as exc:
        print(f"CSV 无法按 utf-8-sig 编码读取。\n文件路径：{display_path}\n异常原因：{exc}")
        return False
    except (pd.errors.ParserError, OSError) as exc:
        print(f"CSV 无法读取。\n文件路径：{display_path}\n异常原因：{exc}")
        return False

    if df.empty:
        print(f"数据文件为空，无法执行数据探查。\n文件路径：{display_path}")
        return False

    print(f"正在探查数据文件：{display_path}")
    with pd.option_context("display.max_columns", None, "display.width", 160):
        show_basic_info(df)
        analyze_missing_values(df)
        analyze_duplicates(df)
        analyze_numeric_columns(df)
        analyze_categorical_columns(df)

    print("\n数据探查完成。原始 CSV 未被修改。")
    return True


if __name__ == "__main__":
    sys.exit(0 if run_exploration() else 1)
