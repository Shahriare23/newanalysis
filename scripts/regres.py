# Step 1: We import necessary packages
from pathlib import Path
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.vector_ar.vecm import (
    coint_johansen,
    select_order,
    VECM
)
from statsmodels.tsa.api import VAR
from statsmodels.tsa.stattools import adfuller


# Step 2: We create folder paths for saved files and ensure it will not crash if the folders are already there.
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Step 3: We load the data
df = pd.read_csv(
    "/workspaces/newanalysis/data/Final_Dataset_v3new.csv"
)

df['Month'] = pd.to_datetime(df['Month'])
df = df.set_index('Month')
df = df.asfreq("MS")

data = df[['Germany_News_Index', 'Search_Index_v3', 'DAX_Volatility']]

print("\nDATA PREVIEW")
print(data.head())

# Step 4: We run ADF stationarity test

# We store results separately

adf_level_results = []
adf_diff_results = []



# ADF Test Function


def adf_test(series, name, result_list):

    result = adfuller(
        series.dropna()
    )

    conclusion = (
        "Stationary"
        if result[1] < 0.05
        else "Non-stationary"
    )

    result_list.append(
        [
            name,
            round(result[0], 4),
            round(result[1], 5),
            conclusion
        ]
    )



# ADF TEST - LEVEL DATA

print("\n==============================")
print("ADF TEST - LEVELS")
print("==============================")


for col in data.columns:

    adf_test(
        data[col],
        col,
        adf_level_results
    )


# We build dataframe

adf_level_table = pd.DataFrame(
    adf_level_results,
    columns=[
        "Variable",
        "ADF Statistic",
        "p-value",
        "Conclusion"
    ]
)


print(adf_level_table)



# Now we save Level ADF PNG

fig, ax = plt.subplots(
    figsize=(8, 2.5)
)

ax.axis("off")


table = ax.table(
    cellText=adf_level_table.values,
    colLabels=adf_level_table.columns,
    loc="center",
    cellLoc="center"
)


table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)


plt.title(
    "ADF Test - Levels",
    fontsize=12,
    pad=20
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR / "ADF_levels_results.png",
    dpi=400,
    bbox_inches="tight"
)


plt.close()



# Step 6: We apply FIRST DIFFERENCING to make the variables stationary.


# We generate first difference

data_diff = data.diff().dropna()




#ADF TEST - DIFFERENCED DATA

print("\n==============================")
print("ADF TEST - First Diffrence")
print("==============================")


for col in data_diff.columns:

    adf_test(
        data_diff[col],
        col,
        adf_diff_results
    )



# We build the dataframe

adf_diff_table = pd.DataFrame(
    adf_diff_results,
    columns=[
        "Variable",
        "ADF Statistic",
        "p-value",
        "Conclusion"
    ]
)


print(adf_diff_table)



# We save the Difference ADF PNG

fig, ax = plt.subplots(
    figsize=(8, 2.5)
)

ax.axis("off")


table = ax.table(
    cellText=adf_diff_table.values,
    colLabels=adf_diff_table.columns,
    loc="center",
    cellLoc="center"
)


table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)


plt.title(
    "ADF Test - First Difference",
    fontsize=12,
    pad=20
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR / "ADF_difference_results.png",
    dpi=400,
    bbox_inches="tight"
)


plt.close()


# We run Johansen cointegration test to check if the variables have a long-run equilibrium relationship.

from statsmodels.tsa.vector_ar.vecm import coint_johansen
johansen_test = coint_johansen(df[['Germany_News_Index', 'Search_Index_v3', 'DAX_Volatility']], det_order=0, k_ar_diff=1)
print(johansen_test.lr1)
print(johansen_test.cvt)

johansen_results = pd.DataFrame(
    {
        "Trace Statistic": johansen_test.lr1,
        "90% Critical": johansen_test.cvt[:,0],
        "95% Critical": johansen_test.cvt[:,1],
        "99% Critical": johansen_test.cvt[:,2]
    }
)


print(johansen_results)

# We save the results as PNG file 


fig, ax = plt.subplots(
    figsize=(10, 3)
)

ax.axis("off")


table = ax.table(
    cellText=johansen_results.round(4).values,
    colLabels=johansen_results.columns,
    loc="center",
    cellLoc="center"
)


table.auto_set_font_size(False)
table.set_fontsize(10)

table.scale(
    1,
    2
)


plt.title(
    "Johansen Cointegration Test (Trace Statistics)",
    fontsize=13,
    pad=20
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR / "Johansen_results.png",
    dpi=400,
    bbox_inches="tight"
)


plt.close()



# We now choose the optimal lag path to run VECM

from statsmodels.tsa.vector_ar.vecm import select_order
lag_test = select_order(
    data,
    maxlags=10,
    deterministic="ci"
)
print(lag_test.summary())

# Based on AIC/FPE
selected_lag = 3

# We run VECM

from statsmodels.tsa.vector_ar.vecm import VECM

vecm_model = VECM(
    data,
    k_ar_diff=3,
    coint_rank=2,
    deterministic="ci"
)

vecm_result = vecm_model.fit()

vecm_summary = vecm_result.summary()

print(vecm_summary)


# We convert summary to image

fig = plt.figure(
    figsize=(16, 12)
)

ax = fig.add_subplot(111)

ax.axis("off")


summary_text = str(vecm_summary)


ax.text(
    0,
    1,
    summary_text,
    fontsize=7,
    family="monospace",
    verticalalignment="top"
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR / "VECM_summary.png",
    dpi=400,
    bbox_inches="tight"
)


plt.close()

# We run model diagnostics test (check for residuals)

vecm_result.test_whiteness(nlags=12)
vecm_result.test_normality()

print("\nWHITENESS TEST")
print(
    vecm_result.test_whiteness(nlags=12)
)


print("\nNORMALITY TEST")
print(
    vecm_result.test_normality()
)


# We run Impulse response function tests
irf = vecm_result.irf(12)

irf.plot()

plt.title(
    "Impulse Response Function (12 Months)"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "IRF_plot.png",
    dpi=400,
    bbox_inches="tight"
)

plt.show()




# We run Granger causality test

print("\n==============================")
print("GRANGER CAUSALITY TESTS")
print("==============================")


causality_tests = [

    (
        "Germany News -> DAX Volatility",
        "DAX_Volatility",
        "Germany_News_Index"
    ),

    (
        "Search Index -> DAX Volatility",
        "DAX_Volatility",
        "Search_Index_v3"
    ),

    (
        "DAX Volatility -> Germany News",
        "Germany_News_Index",
        "DAX_Volatility"
    ),

    (
        "DAX Volatility -> Search Index",
        "Search_Index_v3",
        "DAX_Volatility"
    ),

    (
        "Germany News -> Search Index",
        "Search_Index_v3",
        "Germany_News_Index"
    ),

    (
        "Search Index -> Germany News",
        "Germany_News_Index",
        "Search_Index_v3"
    )

]


# We store the results

granger_results = []


for title, caused, causing in causality_tests:


    result = vecm_result.test_granger_causality(
        caused=caused,
        causing=causing
    )


    # We extract the values

    granger_results.append(
        [
            title,
            round(result.test_statistic, 4),
            round(result.pvalue, 5),
            "Significant" if result.pvalue < 0.05 else "Not Significant"
        ]
    )


# we create dataframe

granger_table = pd.DataFrame(
    granger_results,
    columns=[
        "Causal Direction",
        "Test Statistic",
        "p-value",
        "Conclusion"
    ]
)


print(granger_table)


# We save the file as PNG
fig, ax = plt.subplots(
    figsize=(12, 4)
)

ax.axis("off")


table = ax.table(
    cellText=granger_table.values,
    colLabels=granger_table.columns,
    loc="center",
    cellLoc="center"
)


table.auto_set_font_size(False)

table.set_fontsize(9)

table.scale(
    1,
    2
)


plt.title(
    "Granger Causality Test Results (VECM)",
    fontsize=13,
    pad=20
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR / "Granger_causality_results.png",
    dpi=400,
    bbox_inches="tight"
)


plt.close()