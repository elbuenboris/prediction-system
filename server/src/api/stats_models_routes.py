from fastapi import APIRouter
from typing import Dict, Any
from ..repositories.order_repository import OrderRepository
from ..database import get_db_session
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind
from tabulate import tabulate
from scipy.stats import chi2_contingency



stats_models_router = APIRouter()

@stats_models_router.post("/lineal-regretion")
def lineal_regretion(data: Dict[str, Any]):
    db = get_db_session()

    try:
        orders = OrderRepository.get_orders(db)
        df = pd.DataFrame([order.to_dict() for order in orders])
        model = smf.ols("profit_margin_percentage ~ unit_price + C(region) + C(category)", data=df).fit()
        print(model.summary())
        

        #return{"message": "Lineal regresion summary", "summary": model.summary().as_text()}
        return {
            "message": "Linear regression result",
            "coefficients": model.params.to_dict(),
            "pvalues": model.pvalues.to_dict(),
            "standard_errors": model.bse.to_dict(),
            "r_squared": model.rsquared,
            "r_squared_adj": model.rsquared_adj,
            "f_statistic": model.fvalue,
            "f_pvalue": model.f_pvalue,
            "n_observations": model.nobs
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()


@stats_models_router.post("/t-test")
def t_test(data: Dict[str, Any]):

    db = get_db_session()

    try:
        orders = OrderRepository.get_orders(db)
        df = pd.DataFrame([order.to_dict() for order in orders])

        group1 = df[df["region"] == "Asia"]["profit_margin_percentage"].dropna()
        group2 = df[df["region"] == "North America"]["profit_margin_percentage"].dropna()

        t_stat, p_val = ttest_ind(group1, group2, equal_var=False)
        summary_data = [
            ["Asia", group1.mean()],
            ["North America", group2.mean()]
        ]
        print("\n=== Group Means ===")
        print(tabulate(summary_data, headers=["Group", "Mean Profit Margin"], floatfmt=".2f"))
        print("\n=== T-Test Statistics ===")
        print(tabulate([["T-statistic", t_stat], ["P-value", p_val]], floatfmt=".4f"))


        return {
            "message": "Two-sample t-test for profit margin by region",
            "group_1_mean": group1.mean(),
            "group_2_mean": group2.mean(),
            "t_statistic": t_stat,
            "p_value": p_val
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@stats_models_router.post("/correlation")
def correlation_analysis(data: Dict[str, Any]):
    db = get_db_session()

    try:
        orders = OrderRepository.get_orders(db)
        df = pd.DataFrame([order.to_dict() for order in orders])

        df = df.dropna(subset=["quantity", "profit_margin_percentage"])

        correlation = df["quantity"].corr(df["profit_margin_percentage"])

        print("\n=== Correlation Analysis ===")
        data = [
            ["Variable 1", "quantity"],
            ["Variable 2", "profit_margin_percentage"],
            ["Correlation Coefficient", f"{correlation:.4f}"]
        ]
        print(tabulate(data, tablefmt="plain"))

        return {
            "message": "Correlation between quantity and profit margin",
            "correlation_coefficient": correlation
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

@stats_models_router.post("/chi-square")
def chi_square_test(data: Dict[str, Any]):
    db = get_db_session()

    try:
        orders = OrderRepository.get_orders(db)
        df = pd.DataFrame([order.to_dict() for order in orders])

        contingency_table = pd.crosstab(df["region"], df["status"])
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        print(data.get("model"))

        #print("\n=== Chi-Square Test for Independence ===")

        # Estadísticas
        stats_table = [
            ["Chi² Statistic", f"{chi2:.4f}"],
            ["Degrees of Freedom", dof],
            ["P-value", f"{p:.4f}"]
        ]
        print(tabulate(stats_table, tablefmt="plain"))

        # Contingency Table
        print("\nObserved Frequencies (Contingency Table):")
        print(tabulate(contingency_table.reset_index(), headers="keys", tablefmt="grid"))

        # Expected Frequencies
        expected_df = pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)
        print("\nExpected Frequencies:")
        print(tabulate(expected_df.reset_index(), headers="keys", tablefmt="grid", floatfmt=".2f"))

        return {
            "message": "Chi-squared test for independence between region and status",
            "chi2_statistic": chi2,
            "p_value": p,
            "degrees_of_freedom": dof,
            "contingency_table": contingency_table.to_dict(),
            "expected_freqs": pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns).to_dict()
        }

    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()

