"""
Talent Acquisition AI Engine & Funnel Intelligence Platform
Module: Executive C-Level Excel Workbook Generator (excel_builder.py)

Compiles high-impact executive workbooks with openpyxl, formatting KPI cards,
funnel drop-off tables, channel ROI matrices, and conditional alert formatting.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd


class ExecutiveExcelBuilder:
    """
    Generates high-polish executive workbooks for C-Level Talent & HR Directors.
    """

    def __init__(self, output_path: str = "dist/Talent_Acquisition_Executive_Dashboard.xlsx"):
        self.output_path = output_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    def build_dashboard(
        self,
        df_funnel: pd.DataFrame,
        df_channels: pd.DataFrame,
        df_employers: pd.DataFrame
    ) -> str:
        """
        Creates a multi-tab formatted Excel report with executive KPI cards.
        """
        wb = openpyxl.Workbook()
        
        # Styles
        font_title = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
        font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        font_data = Font(name="Segoe UI", size=10)
        font_kpi_val = Font(name="Segoe UI", size=18, bold=True, color="1E293B")
        font_kpi_lbl = Font(name="Segoe UI", size=9, color="64748B")

        fill_navy = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        fill_blue = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid")
        fill_light_gray = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        fill_card = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

        border_thin = Border(
            left=Side(style='thin', color='CBD5E1'),
            right=Side(style='thin', color='CBD5E1'),
            top=Side(style='thin', color='CBD5E1'),
            bottom=Side(style='thin', color='CBD5E1')
        )

        # ---------------------------------------------------------------------
        # TAB 1: EXECUTIVE SUMMARY & FUNNEL
        # ---------------------------------------------------------------------
        ws_funnel = wb.active
        ws_funnel.title = "Executive Funnel & KPIs"
        ws_funnel.views.sheetView[0].showGridLines = True

        # Header Title Banner
        ws_funnel.merge_cells("A1:F2")
        title_cell = ws_funnel["A1"]
        title_cell.value = "  APPLY ON JOB — TALENT ACQUISITION EXECUTIVE KPI DASHBOARD"
        title_cell.font = font_title
        title_cell.fill = fill_navy
        title_cell.alignment = Alignment(vertical="center", horizontal="left")

        # KPI Summary Cards (Row 4 to 6)
        kpis = [
            ("Total Applications", f"{df_funnel.iloc[0]['candidate_volume']:,}", "A", "B"),
            ("Passed Initial Triage", f"{df_funnel.iloc[1]['candidate_volume']:,}", "C", "C"),
            ("Technical Interviews", f"{df_funnel.iloc[2]['candidate_volume']:,}", "D", "D"),
            ("Offers Extended", f"{df_funnel.iloc[3]['candidate_volume']:,}", "E", "E"),
            ("Final Hires", f"{df_funnel.iloc[4]['candidate_volume']:,}", "F", "F"),
        ]

        for lbl, val, col_start, col_end in kpis:
            cell_ref = f"{col_start}4"
            if col_start != col_end:
                ws_funnel.merge_cells(f"{col_start}4:{col_end}4")
                ws_funnel.merge_cells(f"{col_start}5:{col_end}5")

            ws_funnel[f"{col_start}4"].value = lbl
            ws_funnel[f"{col_start}4"].font = font_kpi_lbl
            ws_funnel[f"{col_start}4"].fill = fill_card
            ws_funnel[f"{col_start}4"].alignment = Alignment(horizontal="center", vertical="center")

            ws_funnel[f"{col_start}5"].value = val
            ws_funnel[f"{col_start}5"].font = font_kpi_val
            ws_funnel[f"{col_start}5"].fill = fill_card
            ws_funnel[f"{col_start}5"].alignment = Alignment(horizontal="center", vertical="center")

        # Funnel Breakdown Table (Row 8)
        ws_funnel["A7"].value = "Application Funnel Stage Progression & Drop-Off Rates"
        ws_funnel["A7"].font = Font(name="Segoe UI", size=12, bold=True, color="0F172A")

        headers = ["Funnel Stage", "Candidate Volume", "Stage Conversion %", "Drop-Off %"]
        for col_idx, h in enumerate(headers, start=1):
            cell = ws_funnel.cell(row=8, column=col_idx)
            cell.value = h
            cell.font = font_header
            cell.fill = fill_blue
            cell.alignment = Alignment(horizontal="center", vertical="center")

        for r_idx, row in df_funnel.iterrows():
            curr_row = 9 + r_idx
            ws_funnel.cell(row=curr_row, column=1, value=str(row["stage_name"])).font = font_data
            ws_funnel.cell(row=curr_row, column=2, value=int(row["candidate_volume"])).font = font_data
            ws_funnel.cell(row=curr_row, column=3, value=float(row["stage_conversion_pct"])).font = font_data
            ws_funnel.cell(row=curr_row, column=4, value=float(row["drop_off_pct"])).font = font_data

            # Apply borders
            for c in range(1, 5):
                ws_funnel.cell(row=curr_row, column=c).border = border_thin

        # ---------------------------------------------------------------------
        # TAB 2: RECRUITMENT SOURCING CHANNELS
        # ---------------------------------------------------------------------
        ws_channels = wb.create_sheet(title="Sourcing Channels ROI")
        ws_channels.views.sheetView[0].showGridLines = True

        ws_channels.merge_cells("A1:H2")
        title_chan = ws_channels["A1"]
        title_chan.value = "  SOURCING CHANNEL EFFICIENCY & COST-PER-HIRE MATRIX"
        title_chan.font = font_title
        title_chan.fill = fill_navy
        title_chan.alignment = Alignment(vertical="center", horizontal="left")

        chan_headers = [
            "Channel Name", "Channel Type", "Total Candidates", "Interviews",
            "Final Hires", "Avg Match Score", "Hire Yield %", "Cost / Hire USD"
        ]
        for col_idx, h in enumerate(chan_headers, start=1):
            cell = ws_channels.cell(row=4, column=col_idx)
            cell.value = h
            cell.font = font_header
            cell.fill = fill_blue
            cell.alignment = Alignment(horizontal="center", vertical="center")

        for r_idx, row in df_channels.iterrows():
            curr_row = 5 + r_idx
            ws_channels.cell(row=curr_row, column=1, value=str(row["channel_name"])).font = font_data
            ws_channels.cell(row=curr_row, column=2, value=str(row["channel_type"])).font = font_data
            ws_channels.cell(row=curr_row, column=3, value=int(row["total_candidates"])).font = font_data
            ws_channels.cell(row=curr_row, column=4, value=int(row["interview_count"])).font = font_data
            ws_channels.cell(row=curr_row, column=5, value=int(row["hire_count"])).font = font_data
            ws_channels.cell(row=curr_row, column=6, value=float(row["avg_match_score"])).font = font_data
            ws_channels.cell(row=curr_row, column=7, value=float(row["channel_hire_yield_pct"])).font = font_data
            ws_channels.cell(row=curr_row, column=8, value=float(row["estimated_cost_per_hire_usd"]) if pd.notna(row["estimated_cost_per_hire_usd"]) else 0.0).font = font_data

            for c in range(1, 9):
                ws_channels.cell(row=curr_row, column=c).border = border_thin

        # Adjust column widths automatically
        for sheet in [ws_funnel, ws_channels]:
            for col in sheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col[0].column)
                sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

        wb.save(self.output_path)
        print(f"[Excel Builder] Executive dashboard exported -> {self.output_path}")
        return self.output_path
