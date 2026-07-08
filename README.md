# Economic Uncertainty, Information Seeking, and Financial Markets

This project examines the relationship between economic policy uncertainty, information-seeking behavior, and financial market volatility in Germany.

## Data Sources
- Germany Economic Policy Uncertainty (EPU)
- Google Trends
- Yahoo Finance (DAX)

## Period
2010–2026

## Current Status
- Data Collection ✔
- Data Cleaning ✔
- Dataset Construction ✔
- Preliminary Analysis ✔
- Regression Analysis (ongoing)

## Repository Structure

| Folder | Description |
|----------|----------|
| code | Python scripts for regression analysis and visualization |
| data | Raw and processed datasets |
| figures | Generated figures and plots |
| reports | Preliminary analysis report |
| README.md | Project overview and documentation |


# Vector Error Correction Model (VECM) Analysis

## Relationship Between German News Attention, Online Search Behaviour, and DAX Volatility


## 1. Project Overview

This project investigates the dynamic relationship between:

1. Germany News Attention Index
2. Online Search Behaviour Index
3. DAX Market Volatility

The objective is to examine whether information attention indicators influence stock market volatility and whether market volatility itself affects public attention dynamics.

A Vector Error Correction Model (VECM) framework is applied because the variables exhibit non-stationary behaviour and demonstrate long-run equilibrium relationships through cointegration analysis.


---

# 2. Research Variables

| Variable | Description |
|---|---|
| Germany_News_Index | Measure of German news attention intensity |
| Search_Index_v3 | Online search activity indicator |
| DAX_Volatility | Stock market volatility measure based on DAX index |


---

# 3. Methodological Framework

The analysis follows the standard time-series econometric workflow:
Data Preparation
|
↓
ADF Stationarity Test
|
↓
First Differencing
|
↓
ADF Test After Differencing
|
↓
Johansen Cointegration Test
|
↓
Lag Order Selection
|
↓
Vector Error Correction Model (VECM)
|
↓
Residual Diagnostics
|
↓
Impulse Response Function (IRF)
|
↓
Granger Causality Analysis


---

# 4. Econometric Methods


## 4.1 Augmented Dickey-Fuller (ADF) Test

The Augmented Dickey-Fuller test is used to determine whether each time-series variable is stationary.

### Hypotheses:

**Null hypothesis (H0):**

The series contains a unit root and is non-stationary.

**Alternative hypothesis (H1):**

The series is stationary.


### Decision Rule:

| p-value | Interpretation |
|---|---|
| p-value < 0.05 | Stationary |
| p-value ≥ 0.05 | Non-stationary |


Non-stationary variables are transformed using first differencing.


---

## 4.2 First Differencing


First differencing converts non-stationary variables into stationary series:


\[
\Delta X_t = X_t - X_{t-1}
\]


The differenced variables are tested again using the ADF test before applying cointegration analysis.


---

## 4.3 Johansen Cointegration Test


The Johansen cointegration test determines whether variables share a long-run equilibrium relationship.


The trace statistic is compared with critical values:


- Trace Statistic > Critical Value → Reject null hypothesis
- Trace Statistic < Critical Value → Fail to reject null hypothesis


The estimated cointegration rank determines the number of long-run equilibrium relationships used in the VECM model.


---

# 5. Vector Error Correction Model (VECM)


The VECM combines:

## Long-run relationship

Represented by the cointegration equation:


\[
\beta'Y_{t-1}
\]


## Short-run dynamics

Represented by:


\[
\Delta Y_t
=
\alpha\beta'Y_{t-1}
+
\Gamma_1\Delta Y_{t-1}
+
\epsilon_t
\]


where:

- where \(Y_t\) represents the state of the system at time \(t\). The vector \(Y_t\) contains the three variables analysed in the study.

- β represents long-run equilibrium relationships
- α represents adjustment coefficients
- Γ represents short-run dynamics


---

# 6. VECM Model Specification


The estimated model uses:

VECM(
k_ar_diff = 3,
coint_rank = 2,
deterministic = "ci"
)


Explanation:


| Parameter | Meaning |
|---|---|
| k_ar_diff = 3 | Three lagged differences included |
| coint_rank = 2 | Two long-run equilibrium relationships |
| deterministic = "ci" | Constant included inside cointegration relationship |


---

# 7. Error Correction Coefficients (Alpha)


The alpha coefficients show how quickly variables adjust after deviations from long-run equilibrium.


Interpretation:


- Significant alpha coefficient → variable adjusts toward equilibrium
- Insignificant alpha coefficient → variable does not significantly correct disequilibrium


---

# 8. Model Diagnostics


## Residual Whiteness Test


Purpose:

Checks whether residuals contain autocorrelation.


Desired outcome:

p-value > 0.05

indicates that residuals behave as white noise.


---

## Residual Normality Test


Purpose:

Tests whether residuals approximately follow a normal distribution.


Desired outcome:

p-value > 0.05



---

# 9. Impulse Response Function (IRF)


Impulse Response Function evaluates how variables respond to shocks from other variables over time.


The analysis uses:

12-month forecasting horizon



to analyse medium-term responses.


---

# 10. Granger Causality Analysis


Granger causality tests whether past values of one variable provide predictive information about another variable.



Interpretation:


| p-value | Meaning |
|---|---|
| p-value < 0.05 | Significant predictive relationship |
| p-value ≥ 0.05 | No significant predictive relationship |


---


# Team Contribution Statement

All team members actively contributed to the development of the research idea, variable selection, interpretation of results and final presentation decisions.

| Team Member | ID No. | Contribution |
|---|---|---|
| Alireza Takallouie | 254519 | Developed the Introduction, Literature Review, and Conclusion sections. |
| Sahba Maraghemianji | 254481 | Responsible for data collection and preparation, Developed the Data section Variable construction and the AI Assistance Statement. |
| Shahriar Shital | 249465 | Developed the empirical strategy, conducted findings and analysis, performed editorial refinement and managed references. |



