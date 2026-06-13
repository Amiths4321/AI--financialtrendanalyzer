import warnings
# 1. Silencing the urllib3/chardet package warnings cleanly before loading requests
warnings.filterwarnings("ignore", category=UserWarning, module="requests")
warnings.filterwarnings("ignore", message=".*doesn't match a supported version!.*")
warnings.filterwarnings("ignore")

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO
from dotenv import load_dotenv

# Load environmental variables for the remote GPU node
load_dotenv()

# ==========================================
# 1. DATA INGESTION & ARCHIVE ENGINE
# ==========================================
class DataIngestionEngine:
    @staticmethod
    def load_historical_data():
        """
        Simulates parsing multi-year financial/inventory records.
        In a production pipeline, this would use: pd.read_csv() or pd.read_excel()
        """
        print("📥 Initializing Multi-Year Data Ingestion Matrix...")
        
        # Raw Mock Data spanning three periods to track financial trajectory
        historical_records = """Year,Revenue,Net_Profit,Total_Debt,Operational_Cost,Inventory_Value
2024,450000,189000,120000,261000,75000
2025,520000,197600,145000,322400,98000
2026,590000,206500,190000,383500,135000"""
        
        df = pd.read_csv(StringIO(historical_records))
        print(f"📊 Successfully aligned data schema for {len(df)} historical reporting periods.")
        return df

# ==========================================
# 2. CORE STATISTICAL ANALYTICS ENGINE
# ==========================================
class FinancialAnalyticsCore:
    @staticmethod
    def compute_performance_metrics(df):
        """
        Executes operational mathematical operations to locate growth,
        leverage anomalies, and margin compressions.
        """
        print("🔍 Executing multi-year performance calculations...")
        
        # Calculate Net Profit Margin Percentage over time
        df['Net_Margin_Pct'] = (df['Net_Profit'] / df['Revenue']) * 100
        
        # Calculate Debt-to-Equity / Leverage proxies
        df['Debt_To_Revenue_Ratio'] = df['Total_Debt'] / df['Revenue']
        
        # Calculate Year-over-Year Growth rates
        df['Revenue_YoY_Growth'] = df['Revenue'].pct_change() * 100
        df['Debt_YoY_Growth'] = df['Total_Debt'].pct_change() * 100
        
        return df

# ==========================================
# 3. HIGH-FIDELITY VISUALIZATION LAYER
# ==========================================
class DataVisualizer:
    @staticmethod
    def generate_trend_plots(df, output_filename="trends_analysis.png"):
        """
        Generates multi-pane trend charts tracking margins vs. liabilities
        and saves the asset to disk.
        """
        print(f"📈 Generating interactive charts grid layout...")
        sns.set_theme(style="darkgrid")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Revenue vs Net Profit Margin
        color = '#1f77b4'
        ax1 = axes[0]
        ax1.set_title("Topline Revenue Growth vs Net Margin Erosion", fontsize=12, fontweight='bold')
        ax1.set_xlabel("Fiscal Year")
        ax1.set_ylabel("Gross Revenue ($)", color=color)
        sns.barplot(x='Year', y='Revenue', data=df, ax=ax1, color=color, alpha=0.7)
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = '#d62728'
        ax2.set_ylabel("Net Margin (%)", color=color)
        sns.lineplot(x=range(len(df)), y='Net_Margin_Pct', data=df, ax=ax2, color=color, marker="o", linewidth=2.5)
        ax2.set_xticks(range(len(df)))
        ax2.set_xticklabels(df['Year'])
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Plot 2: Debt Accumulation vs Inventory Overhead
        ax3 = axes[1]
        ax3.set_title("Liability Escalation vs Inventory Value", fontsize=12, fontweight='bold')
        sns.lineplot(x='Year', y='Total_Debt', data=df, ax=ax3, color='#e377c2', marker="s", label="Total Debt Liabilities", linewidth=2)
        sns.lineplot(x='Year', y='Inventory_Value', data=df, ax=ax3, color='#bcbd22', marker="^", label="Inventory Holding Value", linewidth=2)
        ax3.set_xlabel("Fiscal Year")
        ax3.set_ylabel("Capital Cost ($)")
        ax3.set_xticks(df['Year'])
        ax3.legend(loc="upper left")
        
        plt.tight_layout()
        plt.savefig(output_filename, dpi=300)
        plt.close()
        print(f"💾 Visualization asset saved successfully to disk as '{output_filename}'.")

# ==========================================
# 4. REMOTE GPU EXECUTIVE SYNTHESIS
# ==========================================
class QwenExecutiveAnalyst:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://10.22.39.192:11434")
        self.model_name = os.getenv("OLLAMA_MODEL_NAME", "qwen2.5-coder:14b")

    def generate_narrative_brief(self, df):
        """
        Attempts to use the remote GPU cluster, falling back to local deterministic 
        insight synthesis if a network timeout occurs.
        """
        data_payload = df.to_string(index=False)
        
        system_prompt = (
            "You are an elite corporate financial controller and data intelligence analyst.\n"
            "Review the raw multi-year statistics and compile a scannable executive report.\n"
            "Format your final output with clean markdown headings and distinct bullet points."
        )

        try:
            print("🧠 Dispatched calculation array to remote GPU node (Timeout set to 4s)...")
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Review this multi-year financial dataset:\n\n{data_payload}"}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.2}
                },
                timeout=4  # ⚡ Fast timeout to bypass hanging connections safely
            )
            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "Failed to compile brief.")
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            print("⚠️ Remote GPU node unreachable. Activating Local Deterministic Insight Engine...")
            return self._execute_local_fallback_analysis(df)
        except Exception as e:
            return f"Unexpected operational exception: {e}"

    def _execute_local_fallback_analysis(self, df):
        """
        Programmatically parses calculated data frames to construct an advanced,
        corporate-grade diagnostic report without relying on external network models.
        """
        initial_year = int(df['Year'].iloc[0])
        final_year = int(df['Year'].iloc[-1])
        total_years = final_year - initial_year
        
        initial_rev = df['Revenue'].iloc[0]
        final_rev = df['Revenue'].iloc[-1]
        
        initial_margin = df['Net_Margin_Pct'].iloc[0]
        final_margin = df['Net_Margin_Pct'].iloc[-1]
        margin_delta = final_margin - initial_margin
        
        initial_debt = df['Total_Debt'].iloc[0]
        final_debt = df['Total_Debt'].iloc[-1]
        debt_growth = ((final_debt - initial_debt) / initial_debt) * 100

        # Revenue Compound Annual Growth Rate (CAGR)
        revenue_cagr = ((final_rev / initial_rev) ** (1 / total_years) - 1) * 100 if total_years > 0 else 0.0

        # Days Inventory Outstanding (DIO) = (Inventory Value / Operational Cost) * 365
        df['DIO'] = (df['Inventory_Value'] / df['Operational_Cost']) * 365
        initial_dio = df['DIO'].iloc[0]
        final_dio = df['DIO'].iloc[-1]
        dio_delta = final_dio - initial_dio

        report = f"### 📌 EXECUTIVE INSIGHT REPORT (Local Fallback Analytical Core)\n\n"
        report += f"**Operational Analysis Window:** FY {initial_year} to FY {final_year} ({total_years}-Year Cycle)\n\n"
        
        report += "### 📈 1. Topline Scaling & Margin Trajectory\n"
        report += f"* **Revenue Velocity:** Topline corporate revenue demonstrated a steady **Compound Annual Growth Rate (CAGR) of {revenue_cagr:.2f}%**, climbing from ${initial_rev:,} to ${final_rev:,}.\n"
        if margin_delta < 0:
            report += f"* 🚨 **WARNING (Margin Compression):** Despite solid revenue scaling, operational efficiency dropped. Net profit margins compressed from **{initial_margin:.1f}%** down to **{final_margin:.1f}%** (a net reduction of **{abs(margin_delta):.1f}%**). Scale expansion is driving unit profitability down.\n"
        else:
            report += f"* ✨ **STABLE OPERATIONS:** Scaled cleanly. Operating efficiency metrics are intact.\n"
            
        report += "\n### 💳 2. Financial Leverage & Debt Velocity\n"
        if debt_growth > 0:
            report += f"* ⚠️ **LEVERAGE ESCALATION:** Total corporate liabilities climbed by **{debt_growth:.1f}%**, moving from ${initial_debt:,} up to ${final_debt:,}. Structural leverage is expanding faster than long-term revenue growth vectors.\n"
        else:
            report += "* ✨ **DEBT DE-LEVERAGING:** Corporate liabilities are contracting smoothly.\n"
            
        report += "\n### 📦 3. Asset Liquidity & Inventory Efficiency\n"
        last_inv = df['Inventory_Value'].iloc[-1]
        report += f"* 📊 **CAPITAL CONCENTRATION:** Active cash liquidity reserves are increasingly locked up inside static inventory, reaching **${last_inv:,}** in the final period.\n"
        if dio_delta > 0:
            report += f"* 🚨 **WARNING (Overstock Bottleneck):** Days Inventory Outstanding (DIO) worsened, shifting from **{initial_dio:.1f} days** up to **{final_dio:.1f} days** (an addition of **{dio_delta:.1f} processing days**). Capital is remaining frozen in static stock pools significantly longer.\n"
        else:
            report += f"* ✨ **TURNOVER VELOCITY:** Stock liquidation loops remained optimal.\n"
        
        report += "\n### 🛠️ Strategic Remediation Directives\n"
        report += "1. **Overhead Optimization:** Conduct an immediate cost center audit on operational costs to protect unit margins from further scaling decay.\n"
        report += "2. **Inventory Liquidation:** Adjust reorder safety points downwards to release the frozen working capital locked inside warehouse assets.\n"
        report += "3. **Debt Rationalization:** Halt incremental leverage adjustments to safeguard net corporate liquidity against high interest servicing costs."
        
        return report

# ==========================================
# 5. ORCHESTRATION RUNTIME ENTRY POINT
# ==========================================
if __name__ == "__main__":
    print("============================================================")
    print("      📊 RUNTIME: MULTI-YEAR PERFORMANCE ENGINE STARTED     ")
    print("============================================================\n")
    
    try:
        # Step 1: Parse and Load Data
        data_matrix = DataIngestionEngine.load_historical_data()
        
        # Step 2: Run Statistical Indicators
        computed_matrix = FinancialAnalyticsCore.compute_performance_metrics(data_matrix)
        
        # Step 3: Draw charts and plots
        DataVisualizer.generate_trend_plots(computed_matrix)
        
        # Step 4: Run Narrative Analysis
        analyst = QwenExecutiveAnalyst()
        report_output = analyst.generate_narrative_brief(computed_matrix)
        
        print("\n============================================================")
        print("              EXECUTIVE INSIGHT REPORT (COMPLETE)           ")
        print("============================================================\n")
        print(report_output)
        print("\n============================================================")
        
    except Exception as e:
        print(f"\n❌ Script Execution Failure: {e}")