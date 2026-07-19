from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    if any(word in normalized for word in ["流失率", "流失"]):
        return (
            f"总体流失率为{metrics['流失率']:.1%}，"
            f"共{int(metrics['流失人数']):,}人流失。"
        )
    if any(word in normalized for word in ["偏好品类", "品类", "哪个品类"]):
        category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
        top = category_df.loc[category_df["用户数"].idxmax()]
        return f"偏好品类中{top['PreferedOrderCat']}的用户最多，共{int(top['用户数']):,}人。"
    if any(word in normalized for word in ["生命周期", "风险最高", "哪个阶段"]):
        segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
        worst = segment_df.loc[segment_df["流失率"].idxmax()]
        return (
            f"{worst['TenureGroup']}的流失率最高，"
            f"达到{worst['流失率']:.1%}，"
            f"建议重点关注新用户留存。"
        )
    if any(word in normalized for word in ["订单数", "平均订单"]):
        return (
            f"平均订单数为{metrics['平均订单数']:.2f}单，"
            f"中位数为{int(metrics['订单数中位数'])}单。"
        )

    return "抱歉，我还没学会回答这个问题。请试试推荐问题。"
