# Surface Water BOD Prediction

A Streamlit web application that estimates Biochemical Oxygen Demand
(BOD) in surface-water samples from water-quality measurements.

## Overview

Biochemical Oxygen Demand (BOD) is an indicator of the oxygen consumed
by microorganisms as they break down organic matter in water. BOD
measurements can help with surface-water quality monitoring and
analysis.

This project provides an interactive interface for entering
water-quality parameters and viewing a machine-learning-based BOD
estimate.

## Features

-   Interactive web interface built with Streamlit
-   Machine-learning-based BOD prediction
-   Water-quality input fields for physicochemical measurements
-   Prediction results displayed in the application

> **Note:** Predictions are model estimates, not laboratory measurements
> or official regulatory assessments. Use laboratory testing and expert
> review for important environmental or public-health decisions.

## Machine Learning

The development workflow evaluated Random Forest regression using
different target transformations, including the original BOD values,
`log1p(BOD)`, and square-root-transformed BOD.

In one experimental random 80/20 train/test split (`random_state=42`),
the Random Forest model trained with `log1p(BOD)` reported these
results:

  Metric                                  Result
  -------------------------------- -------------
  Mean Absolute Error (MAE)          0.5971 mg/L
  Root Mean Squared Error (RMSE)     0.8045 mg/L
  R²                                      0.2112

These are experimental results, not a guarantee of the performance of
every deployed version. Use these numbers to describe the live
application only if its model and preprocessing steps match this
experiment. A random split also does not establish how well the model
will perform on future years or unseen monitoring stations.

## Dataset

The model-development work used surface-water quality records from
Andhra Pradesh covering 2021--2025. Variables include BOD and
physicochemical measurements such as dissolved oxygen, electrical
conductivity, turbidity, temperature, total dissolved solids, pH, and
other water-quality parameters, along with sampling time and
monitoring-station information.

Confirm the dataset's original source, license, and attribution
requirements before redistributing it.

## Run the App Locally

### 1. Download the project

Clone the repository:

``` bash
git clone https://github.com/Vivek-010107/surface-water-bod-prediction.git
cd surface-water-bod-prediction
```

You can also download the repository as a ZIP file from GitHub and
extract it.

### 2. Install the required libraries

If the repository contains a `requirements.txt` file, run:

``` bash
pip install -r requirements.txt
```

There is **no requirement to create a `venv` folder or use a virtual
environment** for this project. You can install the listed dependencies
in your existing Python environment.

### 3. Start the Streamlit app

From the project folder, run:

``` bash
streamlit run app.py
```

Streamlit will show a local address in the terminal, usually
`http://localhost:8501`. Open that address in your browser.

## Deployment

The application can be hosted using [Streamlit Community
Cloud](https://share.streamlit.io/).

1.  Keep `app.py`, `requirements.txt` (if used), and any required model
    or data files in the GitHub repository.
2.  In Streamlit Community Cloud, select the repository and branch.
3.  Set the app's main file to `app.py`.
4.  Deploy the app and review the logs if an error occurs.
5.  After deployment, pushing changes to the configured GitHub branch
    normally triggers a redeployment.

Make sure the deployed app's dependencies, model files, and
preprocessing steps match what `app.py` expects.

## Limitations

-   Model predictions have uncertainty and do not replace laboratory BOD
    analysis.
-   A random train/test split can place records from the same stations
    or different years in both sets; its metrics do not prove
    future-year performance.
-   Rare, extreme BOD values may be difficult to predict accurately.
-   Results depend on data quality and whether app inputs match the
    features used during model training.
-   Do not use the model as the sole basis for regulatory,
    environmental, or public-health decisions.

## Future Improvements

-   Test the model on later-period data and stations not seen during
    training
-   Compare predictions with laboratory measurements
-   Evaluate performance across stations, years, and BOD ranges
-   Investigate unusual observations and quantify prediction uncertainty
-   Improve data documentation and input validation

## Disclaimer

This project is intended for educational and exploratory use. Its
predictions are model-generated estimates, not official water-quality
assessments.

## Author

**Vivek**

GitHub repository:
[Vivek-010107/surface-water-bod-prediction](https://github.com/Vivek-010107/surface-water-bod-prediction)
