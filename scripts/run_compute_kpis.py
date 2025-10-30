import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.kpi_calculations import compute_all_kpis

if __name__ == "__main__":
    compute_all_kpis()
    print("✅ All KPIs computed.")