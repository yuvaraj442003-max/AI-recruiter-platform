"""
curriculum_data_science.py - Complete 8 Chapters Comprehensive Curriculum for Data Science.
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & Architecture
3. Step-by-Step Solved Examples with working code and breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

DATA_SCIENCE_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Data Science Lifecycle & Scientific Python Stack (NumPy, Pandas, SciPy)",
        "key_takeaways": "Master OSEMN / CRISP-DM lifecycle, vectorized NumPy broadcasting, Pandas DataFrames indexing/grouping, and memory profiling.",
        "topics": [
            "Data Science Lifecycle: OSEMN (Obtain, Scrub, Explore, Model, iNterpret) and CRISP-DM",
            "NumPy ndarray internals: Memory layouts (C-contiguous vs Fortran), strides, broadcasting rules",
            "Pandas High-Performance Manipulation: loc/iloc indexing, assign, merge, join, concat & groupby aggregations",
            "Vectorization vs Python loops: Eliminating slow iterrows in favor of vectorized NumPy operations",
            "Memory Optimization: Downcasting numeric types (float64 to float32/int16), Categorical types & Parquet file storage"
        ],
        "sections": {
            "concept": "Data Science extracts actionable insights, predictive models, and business intelligence from structured and unstructured data. The standard lifecycle follows CRISP-DM (Cross-Industry Standard Process for Data Mining): Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Deployment. The Python scientific stack forms the core engine: NumPy provides contiguous ndarrays executing compiled C/BLAS vector instructions up to 100x faster than pure Python lists; Pandas builds on NumPy, offering tabular DataFrames with SQL-like joining, filtering, and rolling window aggregations.",
            "formulas": "1. NumPy Broadcasting Rule: Dimensions must match or one of them must be 1\n2. Memory Downcasting: int64 (8 bytes) -> int16 (2 bytes) = 75% memory footprint reduction\n3. Parquet vs CSV Compression: Parquet columnar snappy compression reduces file size by 70-90%",
            "solved_examples": [
                {
                    "title": "Optimizing Large Pandas DataFrame Memory Usage by 80% via Type Downcasting",
                    "difficulty": "Medium | Amazon, Uber, Flipkart",
                    "problem": "Write a Python function that inspects a 10-million row DataFrame and downcasts float64 and int64 columns to their minimal safe representations.",
                    "step_by_step": [
                        "Step 1: Iterate over numeric columns in `df.select_dtypes(include=['int', 'float']).columns`.",
                        "Step 2: Find min and max values for the column using `col.min()` and `col.max()`.",
                        "Step 3: If integer: downcast to `np.int8`, `np.int16`, or `np.int32` based on boundary thresholds.",
                        "Step 4: If float: downcast to `np.float32` if precision permits.",
                        "Step 5: Convert low-cardinality object/string columns (< 50% unique) to `category` dtype."
                    ],
                    "code_or_math": "import pandas as pd\nimport numpy as np\n\ndef reduce_mem_usage(df):\n    start_mem = df.memory_usage().sum() / 1024**2\n    for col in df.columns:\n        col_type = df[col].dtype\n        if col_type == 'int64':\n            df[col] = pd.to_numeric(df[col], downcast='integer')\n        elif col_type == 'float64':\n            df[col] = pd.to_numeric(df[col], downcast='float')\n    end_mem = df.memory_usage().sum() / 1024**2\n    print(f'Memory reduced from {start_mem:.2f} MB to {end_mem:.2f} MB')"
                }
            ],
            "practice_questions": [
                {
                    "question": "Why should data scientists avoid using `df.iterrows()` when processing large Pandas DataFrames?",
                    "options": [
                        "It converts numbers to strings",
                        "`iterrows()` converts each row into a new Pandas Series, incurring massive Python object creation overhead and running up to 1,000x slower than vectorized operations",
                        "It deletes the DataFrame from RAM",
                        "It is deprecated in Python 3"
                    ],
                    "answer": "`iterrows()` converts each row into a new Pandas Series, incurring massive Python object creation overhead and running up to 1,000x slower than vectorized operations",
                    "explanation": "Iterating through DataFrames with `iterrows()` creates a new Series object per row, defeating C-level vectorization and executing in pure Python bytecode. Vectorized NumPy expressions (`df['A'] * df['B']`) run in compiled C at hardware memory bandwidth speeds."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Uber",
                    "question": "What is the NumPy Broadcasting Rule, and under what conditions can two arrays of different shapes be multiplied together?",
                    "model_answer": "NumPy broadcasting allows arithmetic operations on arrays of different shapes without copying data. When operating on two arrays, NumPy compares their shapes element-wise starting from the trailing (rightmost) dimensions. Two dimensions are compatible if: 1) they are equal, or 2) one of them is 1. If one dimension is 1, it is virtually stretched to match the other dimension without memory replication.",
                    "interviewer_tip": "Emphasize starting comparisons from the rightmost (trailing) dimension."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Exploratory Data Analysis (EDA), Missing Value Imputation & Feature Engineering",
        "key_takeaways": "Master skewness/kurtosis, outlier detection (IQR, Z-Score), advanced imputation (KNN, MICE), categorical encoding, and feature scaling.",
        "topics": [
            "Descriptive Statistics: Mean, Median, Mode, Variance, Skewness & Kurtosis distributions",
            "Outlier Detection & Treatment: Tukey's Interquartile Range (IQR 1.5x) vs Z-Score (> 3 sigma) vs Isolation Forests",
            "Missing Data Mechanics: MCAR (Missing Completely at Random), MAR (Missing at Random) & MNAR",
            "Imputation Techniques: Mean/Median/Mode, KNN Imputer, MICE (IterativeImputer) & Indicator flags",
            "Feature Engineering: Target Encoding, Weight of Evidence (WoE), Polynomial Features & Log/Box-Cox transforms"
        ],
        "sections": {
            "concept": "Exploratory Data Analysis (EDA) is the detective work of understanding distributions, relationships, correlations, and anomalies in data before modeling. Real-world data is messy: missing values must be diagnosed by missingness mechanism (MCAR, MAR, MNAR); dropping rows with missing values causes severe sample selection bias. Skewed distributions (e.g. income or prices with long right tails) are normalized using Log or Box-Cox transformations. Feature scaling (StandardScaler z = (x - mu)/sigma vs MinMaxScaler) is essential for distance-based algorithms (KNN, SVM) and gradient-based neural networks.",
            "formulas": "1. IQR Outlier Boundaries: Lower = Q1 - 1.5 * IQR, Upper = Q3 + 1.5 * IQR where IQR = Q3 - Q1\n2. Z-Score Standardization: z = (x - mu) / sigma\n3. Log Transformation: y = log(x + 1) (stabilizes right-skewed variance)",
            "solved_examples": [
                {
                    "title": "Detecting and Capping Outliers using Tukey's IQR Method in Python",
                    "difficulty": "Easy | Tiger Analytics, Mu Sigma, Fractal",
                    "problem": "Write a Python function that identifies outliers in a salary column using IQR and caps them to lower and upper bounds (Winsorization).",
                    "step_by_step": [
                        "Step 1: Calculate 25th percentile (Q1) and 75th percentile (Q3).",
                        "Step 2: Calculate Interquartile Range: `IQR = Q3 - Q1`.",
                        "Step 3: Define lower bound `Q1 - 1.5 * IQR` and upper bound `Q3 + 1.5 * IQR`.",
                        "Step 4: Use `np.clip()` to cap values exceeding boundaries without dropping rows."
                    ],
                    "code_or_math": "import numpy as np\nimport pandas as pd\n\ndef iqr_winsorize(series):\n    q1 = series.quantile(0.25)\n    q3 = series.quantile(0.75)\n    iqr = q3 - q1\n    lower = q1 - 1.5 * iqr\n    upper = q3 + 1.5 * iqr\n    return np.clip(series, lower, upper)\n\nsalaries = pd.Series([30000, 45000, 50000, 52000, 60000, 1000000]) # 1M is outlier\nprint('Capped Salaries:', iqr_winsorize(salaries).tolist())"
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is Median Imputation preferred over Mean Imputation when handling missing values in heavily skewed numerical features?",
                    "options": [
                        "Because the median is easier to calculate on paper",
                        "Because the median is a robust statistic resistant to extreme outliers, whereas the mean is distorted by extreme tail values",
                        "Because mean imputation deletes the column",
                        "Because median imputation converts numbers to integers"
                    ],
                    "answer": "Because the median is a robust statistic resistant to extreme outliers, whereas the mean is distorted by extreme tail values",
                    "explanation": "In skewed distributions (such as house prices with multi-million dollar mansions), the mean is pulled heavily toward the tail. The median represents the true 50th percentile central tendency and is unaffected by extreme outliers."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & American Express",
                    "question": "What is 'Target Leakage' in feature engineering, and how do you prevent it?",
                    "model_answer": "Target Leakage occurs when a feature introduces information from the future or directly from the target variable into the training dataset that would not be available at real-world prediction time. A classic example is computing Mean Target Encoding on the entire dataset before splitting into train/test, leaking test labels into training features. Prevention requires: 1) Performing all feature engineering, scaling, and imputation strictly inside Cross-Validation folds using Scikit-Learn Pipelines; 2) Verifying temporal causality (ensuring features precede target events in time).",
                    "interviewer_tip": "Cite Scikit-Learn Pipelines to prove you know how to prevent leakage in code."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Applied Statistics, Probability & Hypothesis Testing for Data Scientists",
        "key_takeaways": "Master the Central Limit Theorem, P-Values, Type I vs Type II errors, Z-tests, Student's t-tests, ANOVA, and Chi-Square tests of independence.",
        "topics": [
            "Probability Foundations: Bayes' Theorem, Conditional Probability & Random Variables",
            "Probability Distributions: Normal (Gaussian), Binomial, Poisson, Exponential & Student's t-distribution",
            "Central Limit Theorem (CLT) and Confidence Intervals (95% CI: mu +/- 1.96 * SE)",
            "Hypothesis Testing Framework: Null (H0) vs Alternative (H1), Alpha significance level, P-value interpretation",
            "Statistical Tests: One-sample & Two-sample T-test, Paired T-test, One-Way ANOVA & Chi-Square (chi2) test"
        ],
        "sections": {
            "concept": "Statistics is the mathematical compass that prevents data scientists from confusing random noise with genuine scientific signal. The Central Limit Theorem (CLT) states that the sampling distribution of the sample mean approaches a Normal distribution as sample size grows (n >= 30), regardless of the population distribution shape. In hypothesis testing, we assume the Null Hypothesis (H0: no effect) is true; the P-value measures the probability of observing results as extreme as the sample data purely by random chance. When p < alpha (typically 0.05), we reject H0. Student's t-tests compare means between two groups; ANOVA compares means across 3+ groups; Chi-Square tests evaluate independence between categorical variables.",
            "formulas": "1. Standard Error of the Mean: SE = sigma / sqrt(n)\n2. Two-Sample T-Statistic: t = (bar_x1 - bar_x2) / sqrt(s1^2 / n1 + s2^2 / n2)\n3. Chi-Square Test Statistic: chi^2 = Sum ((Observed - Expected)^2 / Expected)",
            "solved_examples": [
                {
                    "title": "Conducting an A/B Testing Two-Sample T-Test in Python (SciPy)",
                    "difficulty": "Medium | Google, Netflix, Booking.com",
                    "problem": "An e-commerce site tests two checkout layouts. Control (A) has 1,000 users with mean cart $85 (std $20); Variant (B) has 1,000 users with mean cart $88 (std $22). Determine if the difference is statistically significant (alpha = 0.05).",
                    "step_by_step": [
                        "Step 1: State hypotheses: H0: mu_A = mu_B (no difference); H1: mu_A != mu_B.",
                        "Step 2: Run two-sample independent t-test: `scipy.stats.ttest_ind_from_stats()`.",
                        "Step 3: Calculate t-statistic: t = (88 - 85) / sqrt(20^2/1000 + 22^2/1000) = 3.0 / 0.94 = 3.19.",
                        "Step 4: P-value for t=3.19 is approximately 0.0014.",
                        "Step 5: Since p (0.0014) < alpha (0.05), reject H0: Variant B's increased revenue is statistically significant."
                    ],
                    "code_or_math": "from scipy import stats\n\nt_stat, p_val = stats.ttest_ind_from_stats(mean1=85, std1=20, nobs1=1000,\n                                           mean2=88, std2=22, nobs2=1000)\nprint(f'T-statistic: {t_stat:.2f}, P-value: {p_val:.4f}')\nprint('Statistically Significant:', p_val < 0.05)"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is a Type I error in statistical hypothesis testing?",
                    "options": [
                        "Failing to reject a false null hypothesis (False Negative)",
                        "Rejecting a true null hypothesis (False Positive / False Alarm)",
                        "Running out of battery during test execution",
                        "Testing with a sample size greater than 100"
                    ],
                    "answer": "Rejecting a true null hypothesis (False Positive / False Alarm)",
                    "explanation": "A Type I error (alpha) occurs when you reject a Null Hypothesis that is actually true\u2014in other words, declaring a medical drug effective or an A/B test variant superior when there is no real effect (a False Positive)."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google & Meta",
                    "question": "What is the Central Limit Theorem, and why is it foundational to modern A/B testing and data science?",
                    "model_answer": "The Central Limit Theorem (CLT) states that if you draw independent, identically distributed random samples of size n from any population (even if the underlying distribution is heavily skewed or bimodal), the distribution of the sample means will asymptotically approach a normal distribution as n increases (typically n >= 30). This allows data scientists to compute confidence intervals, hypothesis tests (Z/T tests), and P-values without needing to know the true population distribution shape.",
                    "interviewer_tip": "Explicitly state that the sample mean distribution becomes normal, NOT the underlying data itself."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Supervised Learning Algorithms: Regression, Trees, Random Forests & XGBoost",
        "key_takeaways": "Master Ordinary Least Squares, Logistic Regression, Decision Trees (Entropy/Gini), Ensemble Bagging (Random Forest), and Gradient Boosting (XGBoost/LightGBM).",
        "topics": [
            "Linear & Logistic Regression: Cost functions, Odds ratios & Maximum Likelihood Estimation",
            "Decision Trees: Splitting criteria (Gini Impurity, Information Gain / Shannon Entropy, MSE)",
            "Ensemble Bagging: Random Forests, bootstrap aggregation, out-of-bag (OOB) error & feature importance",
            "Gradient Boosting: Residual fitting, Gradient Boosted Decision Trees (GBDT), XGBoost & LightGBM",
            "Evaluation Metrics: Precision, Recall, F1-Score, ROC-AUC, PR-AUC, MAE, RMSE & R-squared"
        ],
        "sections": {
            "concept": "Supervised learning maps input features X to labeled targets y. Linear and Logistic Regression serve as transparent, highly interpretable baselines. Decision Trees partition feature space into hyper-rectangles using recursive binary splitting based on Gini Impurity or Entropy. Individual trees suffer from high variance (overfitting). Ensemble methods resolve this: Random Forests average hundreds of de-correlated decision trees trained on bootstrap samples (Bagging) to slash variance. Gradient Boosting (XGBoost, LightGBM) trains trees sequentially: each new tree fits the pseudo-residuals (gradients of the loss function) of the prior ensemble.",
            "formulas": "1. Gini Impurity: Gini = 1 - Sum_i (p_i^2)\n2. XGBoost Objective: Obj = Sum_i l(y_i, hat_y_i) + Sum_k (gamma * T_k + 0.5 * lambda * Sum_j w_j^2)\n3. F1-Score: F1 = 2 * (Precision * Recall) / (Precision + Recall)",
            "solved_examples": [
                {
                    "title": "Building an Optimized XGBoost Classifier with Early Stopping in Python",
                    "difficulty": "Medium | Walmart, Amazon, Fractal",
                    "problem": "Train an XGBoost model on tabular data, evaluating on validation set with early stopping of 10 rounds.",
                    "step_by_step": [
                        "Step 1: Instantiate `XGBClassifier` with `n_estimators=500`, `learning_rate=0.05`, and `max_depth=6`.",
                        "Step 2: Add L2 regularization `reg_lambda=1.0`.",
                        "Step 3: Fit model with `eval_set=[(X_val, y_val)]` and `early_stopping_rounds=10`.",
                        "Step 4: Predict probabilities on test set: `preds = model.predict_proba(X_test)[:, 1]`.",
                        "Step 5: Compute ROC-AUC score using `roc_auc_score(y_test, preds)`."
                    ],
                    "code_or_math": "from xgboost import XGBClassifier\nfrom sklearn.metrics import roc_auc_score\n\nmodel = XGBClassifier(n_estimators=200, learning_rate=0.05, max_depth=5, eval_metric='logloss')\n# model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)\n# auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])"
                }
            ],
            "practice_questions": [
                {
                    "question": "In a severe class imbalance scenario (such as credit card fraud where only 0.05% of transactions are fraudulent), which evaluation metric is LEAST informative and actively misleading?",
                    "options": [
                        "Precision-Recall AUC (PR-AUC)",
                        "Raw Accuracy",
                        "F1-Score",
                        "Recall"
                    ],
                    "answer": "Raw Accuracy",
                    "explanation": "In extreme class imbalance, a naive model that predicts 'Not Fraud' for 100% of transactions achieves 99.95% accuracy while completely failing to catch any fraud. Precision-Recall AUC or F1-Score must be used instead."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Microsoft",
                    "question": "What is the primary architectural difference between Bagging (Random Forest) and Boosting (XGBoost)?",
                    "model_answer": "Bagging (Bootstrap Aggregating) trains multiple deep, high-variance decision trees independently and in parallel on different random subsamples of data and features, averaging their predictions to reduce variance (overfitting). Boosting trains shallow, high-bias trees sequentially: each new tree is trained specifically on the errors (residuals) of the previous trees to progressively reduce bias. Bagging reduces variance; Boosting reduces bias.",
                    "interviewer_tip": "Pair Bagging with Variance reduction and Boosting with Bias reduction."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Unsupervised Learning, Clustering & Dimensionality Reduction (PCA, t-SNE)",
        "key_takeaways": "Master K-Means clustering, the Elbow Method, Silhouette Analysis, DBSCAN density clustering, and Principal Component Analysis (PCA).",
        "topics": [
            "Clustering Paradigms: Centroid-based (K-Means), Density-based (DBSCAN), Hierarchical Agglomerative",
            "K-Means Algorithm: Lloyd's algorithm, K-Means++ initialization & the Elbow Method (Inertia)",
            "Evaluating Clustering Quality: Silhouette Coefficient (-1 to +1) and Davies-Bouldin Index",
            "DBSCAN: Core points, border points, noise points, epsilon distance (eps) & min_samples",
            "Dimensionality Reduction: Principal Component Analysis (PCA: Eigenvalue decomposition, SVD) & t-SNE / UMAP"
        ],
        "sections": {
            "concept": "Unsupervised learning discovers hidden patterns, clusters, and low-dimensional manifolds in unlabeled data. K-Means partitions data into K spherical clusters by minimizing within-cluster sum of squares (Inertia). K-Means++ initialization chooses distant initial seeds, avoiding poor local minima. DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points that are densely packed, handling arbitrary non-convex cluster shapes and naturally isolating noise/outliers. Principal Component Analysis (PCA) projects high-dimensional data onto orthogonal axes of maximum variance via Singular Value Decomposition (SVD), eliminating multicollinearity and reducing dimensionality.",
            "formulas": "1. K-Means Inertia (WCSS): WCSS = Sum_{k=1}^K Sum_{x in C_k} ||x - mu_k||^2\n2. Silhouette Coefficient: s = (b - a) / max(a, b) where a=intra-cluster dist, b=nearest-cluster dist\n3. PCA Explained Variance Ratio: Ratio_i = lambda_i / Sum_j(lambda_j) where lambda is eigenvalue",
            "solved_examples": [
                {
                    "title": "Performing PCA Dimensionality Reduction and Scree Plot Analysis in Python",
                    "difficulty": "Medium | Uber, Airbnb, Microsoft",
                    "problem": "Reduce a 50-feature tabular dataset to principal components that retain at least 95% of total cumulative variance.",
                    "step_by_step": [
                        "Step 1: Standardize features using `StandardScaler` (PCA is scale-sensitive).",
                        "Step 2: Instantiate `PCA(n_components=0.95)` from Scikit-Learn.",
                        "Step 3: Fit and transform scaled data: `X_pca = pca.fit_transform(X_scaled)`.",
                        "Step 4: Check number of components retained: `pca.n_components_`.",
                        "Step 5: Verify explained variance ratio sums to >= 0.95."
                    ],
                    "code_or_math": "from sklearn.decomposition import PCA\nfrom sklearn.preprocessing import StandardScaler\nimport numpy as np\n\nX = np.random.randn(500, 50)\nX_scaled = StandardScaler().fit_transform(X)\npca = PCA(n_components=0.95)\nX_proj = pca.fit_transform(X_scaled)\nprint(f'Original features: 50 -> Reduced features for 95% variance: {pca.n_components_}')"
                }
            ],
            "practice_questions": [
                {
                    "question": "Why is feature standardization (StandardScaler) strictly required before applying Principal Component Analysis (PCA)?",
                    "options": [
                        "Because PCA code throws a syntax error on unstandardized data",
                        "Because PCA seeks axes of maximum variance; features with large arbitrary numerical scales (e.g. Income in millions vs Age in tens) would artificially dominate the principal components purely due to scale",
                        "Because PCA converts numbers to text strings",
                        "It is not required; it is optional"
                    ],
                    "answer": "Because PCA seeks axes of maximum variance; features with large arbitrary numerical scales (e.g. Income in millions vs Age in tens) would artificially dominate the principal components purely due to scale",
                    "explanation": "PCA projects onto directions of maximum variance. If a feature has large units (e.g. annual salary: variance ~10^8), PCA will assign 99% of the first component to that feature alone, ignoring vital features with smaller units."
                }
            ],
            "interview_questions": [
                {
                    "company": "Uber & Airbnb",
                    "question": "What is the primary advantage of DBSCAN clustering over K-Means clustering in real-world geospatial applications?",
                    "model_answer": "K-Means assumes that all clusters are spherical (isotropic) and roughly equal in size, and it forces every single data point into a cluster (highly sensitive to outliers). DBSCAN does not assume spherical shapes: it can discover clusters of arbitrary shapes (such as elongated highways or winding delivery corridors) and explicitly labels low-density points as 'Noise' (-1), naturally filtering out outliers without corrupting cluster centers.",
                    "interviewer_tip": "Cite arbitrary cluster geometry and built-in noise detection."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Time Series Analysis, Forecasting & Sequential Modeling (ARIMA, Prophet)",
        "key_takeaways": "Master stationarity, Augmented Dickey-Fuller (ADF) test, Autocorrelation (ACF/PACF), ARIMA, SARIMAX, and Facebook Prophet.",
        "topics": [
            "Time Series Components: Trend, Seasonality (Additive vs Multiplicative) & Residual Noise",
            "Stationarity: Mean, variance and autocorrelation invariant over time; Differencing (d)",
            "Statistical Tests: Augmented Dickey-Fuller (ADF) test and KPSS test for unit roots",
            "ARIMA Models: AutoRegressive (p), Integrated (d), Moving Average (q) & Seasonal SARIMA (P, D, Q, s)",
            "Facebook Prophet & Modern ML Forecasting: Changepoints, Holiday effects & Lagged features with XGBoost"
        ],
        "sections": {
            "concept": "Time series data exhibits strong temporal ordering where past observations correlate with future values. Classical statistical forecasting requires Stationarity: the statistical properties (mean, variance, covariance) remain constant over time. The Augmented Dickey-Fuller (ADF) test evaluates stationarity; non-stationary series are transformed via differencing (Delta y_t = y_t - y_{t-1}). Autoregressive Integrated Moving Average (ARIMA) models combine past values (AR(p)) and past forecast errors (MA(q)). ACF and PACF plots determine optimal lag orders (p, q). Facebook Prophet decomposes time series into piecewise linear trends, multi-period Fourier seasonality, and holiday impacts.",
            "formulas": "1. AR(p) Model: y_t = c + Sum_{i=1}^p phi_i * y_{t-i} + eps_t\n2. MA(q) Model: y_t = mu + eps_t + Sum_{j=1}^q theta_j * eps_{t-j}\n3. Additive Decomposition: Y_t = Trend_t + Seasonality_t + Residual_t",
            "solved_examples": [
                {
                    "title": "Testing for Stationarity with Augmented Dickey-Fuller (ADF) in Python",
                    "difficulty": "Medium | JPMorgan, Bloomberg, Walmart",
                    "problem": "Write a Python function to test if a revenue time series is stationary using the ADF test; if not, apply first-order differencing.",
                    "step_by_step": [
                        "Step 1: Run `adfuller()` from `statsmodels.tsa.stattools`.",
                        "Step 2: Check p-value against alpha 0.05. If p >= 0.05, the series has a unit root (non-stationary).",
                        "Step 3: Apply first-order differencing: `diff_series = series.diff().dropna()`.",
                        "Step 4: Re-test differenced series with `adfuller()` to confirm p < 0.05 (stationary).",
                        "Step 5: Use d=1 in the ARIMA(p, 1, q) model."
                    ],
                    "code_or_math": "from statsmodels.tsa.stattools import adfuller\nimport pandas as pd\n\ndef check_stationarity(series):\n    res = adfuller(series.dropna())\n    p_val = res[1]\n    print(f'ADF P-Value: {p_val:.4f} -> Stationary: {p_val < 0.05}')\n    return p_val < 0.05"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary visual difference between an Autocorrelation Function (ACF) plot and a Partial Autocorrelation Function (PACF) plot?",
                    "options": [
                        "ACF is plotted in blue, while PACF is plotted in red",
                        "ACF measures the direct and indirect correlation between y_t and y_{t-k}, while PACF measures the direct correlation after controlling for the effects of all intermediate lags",
                        "PACF can only be used on stock prices",
                        "ACF only works on stationary data"
                    ],
                    "answer": "ACF measures the direct and indirect correlation between y_t and y_{t-k}, while PACF measures the direct correlation after controlling for the effects of all intermediate lags",
                    "explanation": "ACF includes correlations propagated through intervening time steps (lag 1 affecting lag 2 affecting lag 3). PACF strips out intermediate lag correlations, isolating the pure direct linear relationship between y_t and y_{t-k}, which identifies the true order p of an AR(p) model."
                }
            ],
            "interview_questions": [
                {
                    "company": "JPMorgan Chase & Walmart",
                    "question": "Why can you not use standard K-Fold Cross Validation for time series data, and what must you use instead?",
                    "model_answer": "Standard K-Fold Cross Validation randomly shuffles data points, using future data points to train models that predict past events. This causes severe temporal lookahead bias (data leakage). For time series, you must use TimeSeriesSplit (Walk-Forward or Rolling Window validation): the training set strictly precedes the validation set chronologically (e.g. Train on Months 1-6 -> Test on Month 7; Train on Months 1-7 -> Test on Month 8), preserving temporal causality.",
                    "interviewer_tip": "Cite 'Temporal Data Leakage' and 'Walk-Forward Validation'."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Data Visualization, Storytelling & Interactive Dashboards (Plotly, Streamlit)",
        "key_takeaways": "Master visual perception rules, chart selection matrices, Seaborn statistical plots, interactive Plotly charts, and Streamlit dashboards.",
        "topics": [
            "Principles of Effective Visual Communication: Edward Tufte's Data-to-Ink ratio & Lie Factor",
            "Chart Selection Matrix: Comparison, Composition, Distribution & Relationship visual archetypes",
            "Static Statistical Plotting with Seaborn & Matplotlib: Pairplots, Heatmaps, Violin plots & FacetGrids",
            "Interactive Dashboards with Plotly: Hover tooltips, zooming, Choropleth maps & multi-axis charts",
            "Rapid Web Applications with Streamlit: Sliders, caching (`@st.cache_data`), session state & deployment"
        ],
        "sections": {
            "concept": "Data visualization transforms complex quantitative analyses into clear, compelling narratives for executive decision-makers. Edward Tufte's Data-to-Ink ratio dictates maximizing the proportion of graphics devoted to non-redundant data while stripping away decorative 'chartjunk'. Chart selection follows strict rules: use Bar charts for discrete categorical comparisons (never pie charts with >3 slices); Histograms and KDE/Violin plots for continuous distributions; Scatter plots for continuous relationships; and Line charts for time-ordered series. Modern data science teams build interactive web apps using Streamlit and Plotly to enable stakeholders to test model hyperparameters in real time.",
            "formulas": "1. Data-to-Ink Ratio: Ratio = Data_Ink / Total_Ink_Used (Target close to 1.0)\n2. Lie Factor = Size_of_Effect_in_Graphic / Size_of_Effect_in_Data (Must equal 1.0)\n3. Color Contrast Ratio: WCAG AA Standard requires minimum 4.5:1 contrast for readability",
            "solved_examples": [
                {
                    "title": "Building a High-Performance Interactive Streamlit Dashboard with Caching",
                    "difficulty": "Easy | Snowflake, Streamlit, McKinsey",
                    "problem": "Create a clean Streamlit app that loads a million-row dataset with caching, filters by category slider, and renders a Plotly chart.",
                    "step_by_step": [
                        "Step 1: Use `@st.cache_data` to ensure the data is loaded and cached in RAM once.",
                        "Step 2: Add interactive sidebar slider for score filtering.",
                        "Step 3: Filter DataFrame using vectorized query.",
                        "Step 4: Render responsive Plotly scatter plot using `st.plotly_chart(fig, use_container_width=True)`."
                    ],
                    "code_or_math": "import streamlit as st\nimport plotly.express as px\nimport pandas as pd\n\n@st.cache_data\ndef load_data():\n    return pd.DataFrame({'Sales': [100, 250, 400], 'Profit': [20, 60, 110], 'Region': ['East', 'West', 'North']})\n\nst.title('Executive Sales Analytics')\ndf = load_data()\nfig = px.bar(df, x='Region', y='Sales', color='Profit', title='Regional Performance')\nst.plotly_chart(fig, use_container_width=True)"
                }
            ],
            "practice_questions": [
                {
                    "question": "Why do expert data scientists strongly discourage using 3D Pie Charts in executive presentations?",
                    "options": [
                        "Because 3D graphics require special 3D glasses",
                        "3D perspective distortion skews angles and surface areas, making slices in the foreground appear artificially larger than identical slices in the background",
                        "Because Python cannot render 3D graphics",
                        "Because pie charts only accept negative numbers"
                    ],
                    "answer": "3D perspective distortion skews angles and surface areas, making slices in the foreground appear artificially larger than identical slices in the background",
                    "explanation": "Human visual perception is notoriously poor at judging relative angles and 3D volumes. 3D perspective creates a severe 'Lie Factor' by visually inflating front-facing slices, distorting true proportions."
                }
            ],
            "interview_questions": [
                {
                    "company": "McKinsey & Netflix",
                    "question": "How do you communicate a complex Machine Learning model's predictions to non-technical executive stakeholders?",
                    "model_answer": "Executive communication requires bridging technical accuracy and business value: 1) Focus on business ROI and outcomes (e.g. 'This churn model saves $2.4M annually by retaining 15% more customers') rather than raw technical metrics like ROC-AUC; 2) Use explainable AI tools (SHAP values / Waterfall plots) to show the exact top drivers behind individual predictions; 3) Provide clear confidence intervals and sensitivity scenarios rather than point estimates; 4) Present interactive prototypes (e.g. Streamlit) that let executives simulate business scenarios.",
                    "interviewer_tip": "Focus on SHAP feature impact and business ROI metrics."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Solved Data Science Case Studies & Placement Technical Scenarios",
        "key_takeaways": "Master top Data Science placement interviews: Customer Churn modeling, Dynamic Pricing algorithms, Recommendation Systems, and Model Explainability (SHAP/LIME).",
        "topics": [
            "End-to-End Case Study 1: E-Commerce Customer Churn Prediction & Lifetime Value (LTV) modeling",
            "End-to-End Case Study 2: Dynamic Ride-Sharing Pricing Algorithm using Elasticity and Demand curves",
            "Recommendation Systems: Collaborative Filtering (Matrix Factorization / SVD) vs Content-Based filtering",
            "Model Explainability (XAI): SHAP (Shapley Additive exPlanations) & LIME for regulatory compliance",
            "FAANG Data Science placement technical interview questions, business case frameworks & coding drills"
        ],
        "sections": {
            "concept": "Data Science placement interviews test end-to-end technical competence combined with business intuition. In churn modeling, predicting churn probability is only the first step: models must be coupled with Customer Lifetime Value (LTV) to target retention discounts only at customers whose retention ROI is positive. Recommendation engines combine Collaborative Filtering (finding similar users via matrix factorization SVD) with Content-Based metadata filtering. In highly regulated domains (banking, healthcare), black-box models are unacceptable: SHAP (Shapley Additive exPlanations), derived from cooperative game theory, provides mathematically sound local and global feature attributions.",
            "formulas": "1. Customer Lifetime Value (CLV): CLV = (Average_Purchase_Value * Purchase_Frequency) / Churn_Rate\n2. Shapley Value Axiom: phi_i(v) = Sum_{S subseteq N \\ {i}} (|S|! * (|N| - |S| - 1)! / |N|!) * (v(S union {i}) - v(S))\n3. Matrix Factorization Decomposition: R approx P * Q^T where P is user matrix and Q is item matrix",
            "solved_examples": [
                {
                    "title": "Computing Global and Local Feature Attributions with TreeSHAP in Python",
                    "difficulty": "Hard | Google, Amazon, Capital One",
                    "problem": "Explain why an XGBoost credit risk model rejected a specific loan applicant using SHAP values.",
                    "step_by_step": [
                        "Step 1: Train XGBoost classifier on credit features.",
                        "Step 2: Create TreeExplainer: `explainer = shap.TreeExplainer(model)`.",
                        "Step 3: Compute SHAP values for the rejected applicant: `shap_values = explainer(applicant_df)`.",
                        "Step 4: Inspect feature contributions: Debt-to-Income ratio pushed risk score up by +0.35, while Credit Score of 610 pushed risk up by +0.22.",
                        "Step 5: Provide legally compliant adverse action notice citing the exact top negative SHAP factors."
                    ],
                    "code_or_math": "import shap\nimport numpy as np\n\n# Conceptual TreeSHAP Implementation\nprint('TreeSHAP decomposes prediction f(x) = base_value + sum(shap_values_i)')\nprint('Provides mathematically fair attribution satisfying local accuracy and consistency axioms.')"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the 'Cold Start Problem' in Collaborative Filtering recommendation systems?",
                    "options": [
                        "The server taking a long time to boot in winter",
                        "The system cannot make accurate collaborative recommendations for new users or new items because there are zero historical ratings or interaction interactions available",
                        "The database running out of storage",
                        "The user disabling cookies"
                    ],
                    "answer": "The system cannot make accurate collaborative recommendations for new users or new items because there are zero historical ratings or interaction interactions available",
                    "explanation": "Collaborative filtering relies on overlapping historical user ratings. When a new user signs up or a new item is added, zero ratings exist, leaving the matrix factorization model unable to find similar vectors. Solutions include hybrid models that fall back to content-based metadata."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Capital One",
                    "question": "Why are SHAP (Shapley Additive exPlanations) values preferred over traditional Gini feature importance from Random Forests?",
                    "model_answer": "Traditional Gini feature importance (Mean Decrease in Impurity) has two severe flaws: 1) It is heavily biased toward continuous features or categorical features with high cardinality; 2) It provides only global importance, with zero directionality (you cannot tell if high values increase or decrease risk) and zero local interpretability for individual predictions. SHAP values, rooted in cooperative game theory, are mathematically sound, consistency-proven, and provide both global impact and exact directional attribution for every individual prediction.",
                    "interviewer_tip": "Cite game theory foundations and lack of cardinality bias."
                }
            ]
        }
    }
]
