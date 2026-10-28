"""
ai_ml_master.py — Prescribed Master Textbook for Artificial Intelligence & Machine Learning.
Comprehensive unabridged campus placement textbook covering supervised/unsupervised learning,
gradient descent mathematics, regression/classification, bias-variance tradeoff,
decision trees, Random Forest, XGBoost, deep learning, backpropagation derivations,
CNNs, Transformers, multi-head attention equations, RAG architectures, and solved placement ML problems.
"""

AI_ML_MASTER_CHAPTERS = [
    {
        "chapter_num": 1,
        "title": "Foundations of Machine Learning & Mathematical Fundamentals",
        "topics": [
            "Taxonomy of AI: Supervised, Unsupervised, Semi-supervised, and Reinforcement Learning",
            "Linear Algebra essentials: Vectors, matrix multiplications, eigenvalues & eigenvectors, SVD",
            "Multivariable Calculus: Gradients, partial derivatives, chain rule for tensor operations",
            "Loss functions: Mean Squared Error (MSE), Binary Cross-Entropy (BCE), Categorical Cross-Entropy",
            "Maximum Likelihood Estimation (MLE) and statistical foundations of learning"
        ],
        "key_takeaways": "Machine learning optimizes model parameters by minimizing loss functions using gradient descent. Cross-entropy loss measures the divergence between true label probability distributions and model predicted probabilities."
    },
    {
        "chapter_num": 2,
        "title": "Supervised Learning: Regression, Classification & Optimization",
        "topics": [
            "Linear Regression: Ordinary Least Squares (OLS) normal equation vs iterative Gradient Descent",
            "Gradient Descent variants: Batch GD, Stochastic GD (SGD), Mini-batch GD, and Adam optimizer (momentum + RMSprop)",
            "Logistic Regression: Sigmoid activation function, log-odds (logit), and decision boundary derivation",
            "Regularization techniques: L1 Lasso (sparsity and feature selection) vs L2 Ridge (weight shrinkage) vs ElasticNet",
            "K-Nearest Neighbors (KNN): Distance metrics (Euclidean, Manhattan), curse of dimensionality, k hyperparameter selection"
        ],
        "key_takeaways": "L1 regularization drives coefficients to exactly zero, performing automatic feature selection; L2 regularization shrinks weights smoothly toward zero, preventing collinearity explosions."
    },
    {
        "chapter_num": 3,
        "title": "Model Evaluation, Bias-Variance Tradeoff & Feature Engineering",
        "topics": [
            "The Bias-Variance Decomposition: Underfitting (High Bias) vs Overfitting (High Variance)",
            "Confusion Matrix metrics: Accuracy, Precision, Recall (Sensitivity), F1-Score, Specificity",
            "Receiver Operating Characteristic (ROC) curve and Area Under Curve (AUC-ROC) interpretation",
            "Cross-Validation: K-Fold, Stratified K-Fold (for imbalanced datasets), Leave-One-Out (LOOCV)",
            "Feature Engineering: Standardization (Z-score) vs Min-Max Normalization, One-Hot Encoding vs Target Encoding, handling missing data"
        ],
        "key_takeaways": "In imbalanced domains (e.g. fraud detection), raw accuracy is misleading. Precision measures purity of positive predictions; Recall measures capture rate of actual positives. F1-Score represents their harmonic mean."
    },
    {
        "chapter_num": 4,
        "title": "Tree-Based Algorithms & Ensemble Learning",
        "topics": [
            "Decision Trees: Splitting criteria (Shannon Entropy & Information Gain vs Gini Impurity)",
            "Tree Pruning: Pre-pruning (max_depth, min_samples_split) vs Cost-Complexity Post-Pruning (alpha)",
            "Bagging (Bootstrap Aggregating): Random Forest (feature subsampling, out-of-bag error estimation)",
            "Boosting fundamentals: Sequential error correction on residual errors",
            "Gradient Boosting Machines (GBM), XGBoost (second-order Taylor approximation, tree leaf regularization), and LightGBM"
        ],
        "key_takeaways": "Random Forest builds independent trees in parallel on bootstrapped subsets to reduce variance. Gradient Boosting builds sequential trees to predict the negative gradient (residual) of the loss function to reduce bias."
    },
    {
        "chapter_num": 5,
        "title": "Deep Learning Architectures & The Backpropagation Algorithm",
        "topics": [
            "The Artificial Neuron (Perceptron) and Multi-Layer Perceptrons (MLP)",
            "Activation functions: Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, and Softmax",
            "Mathematical derivation of Backpropagation: Forward pass, loss calculation, backward chain-rule error propagation",
            "Vanishing and Exploding Gradients: Causes, Xavier/He weight initialization, Batch Normalization, Layer Normalization",
            "Convolutional Neural Networks (CNN): Kernels/filters, padding ('valid' vs 'same'), stride, pooling, and spatial hierarchy"
        ],
        "key_takeaways": "ReLU activation eliminates vanishing gradients in the positive domain. Backpropagation computes the partial derivative of the loss function with respect to every weight tensor via the multivariate chain rule."
    },
    {
        "chapter_num": 6,
        "title": "Sequence Models, Transformers, Attention & Modern LLMs",
        "topics": [
            "Recurrent Neural Networks (RNN) and Long Short-Term Memory (LSTM) gating units (Forget, Input, Output gates)",
            "The Transformer Revolution ('Attention Is All You Need'): Architecture breakdown",
            "Self-Attention mechanics: Query (Q), Key (K), and Value (V) projections, Scaled Dot-Product Attention equation",
            "Multi-Head Attention (MHA) and Positional Encodings (sinusoidal & rotary embeddings)",
            "LLM paradigms: Autoregressive Decoders (GPT), Encoders (BERT), and Retrieval-Augmented Generation (RAG) pipelines"
        ],
        "key_takeaways": "Scaled Dot-Product Attention allows every token in a sequence to attend to every other token in parallel in O(1) sequential steps, overcoming RNN sequential execution bottlenecks."
    },
    {
        "chapter_num": 7,
        "title": "Solved AI/ML Placement Interview Problems & Assessment Drills",
        "topics": [
            "Mathematical derivation of Gradient Descent weight update for Linear Regression",
            "Precision, Recall, and F1-Score step-by-step numerical calculation from confusion matrix",
            "Self-Attention dimension computation for Transformer layers",
            "Bias-variance diagnosis scenario walkthrough with regularization remedies",
            "Self-assessment practice drills with verified solutions"
        ],
        "key_takeaways": "Mastering the mathematics of backpropagation, self-attention dimension tracking, and evaluation metrics ensures high placement test scores at Google, Microsoft, Amazon, and NVIDIA."
    }
]

AI_ML_TEXTBOOK_MARKDOWN = r"""# Artificial Intelligence & Machine Learning: Complete Master Edition (Prescribed Textbook)

**Edition:** 2026 Campus Placement Edition  
**Subject:** Artificial Intelligence & Machine Learning  
**Courseware Board:** Prescribed Placement Architectural Board  
**Status:** In-App Complete Master Textbook (Full Curriculum Available In-Platform)

> **🔒 EXAM GROUNDING POLICY:** All campus placement assessments, AI/ML engineering technical interviews, and online test evaluations (Google, Microsoft, Amazon, NVIDIA, Adobe, TCS Digital) are strictly grounded in the loss functions, optimization proofs, neural architectures, and Transformer equations detailed in this textbook.

---

## 📑 Complete Table of Contents

- [Chapter 1: Foundations of Machine Learning & Mathematical Fundamentals](#chapter-1-foundations-of-machine-learning--mathematical-fundamentals)
  - [1.1 Taxonomy of Machine Learning Paradigms](#11-taxonomy-of-machine-learning-paradigms)
  - [1.2 Essential Linear Algebra & Multivariable Calculus](#12-essential-linear-algebra--multivariable-calculus)
  - [1.3 Core Loss Functions: MSE vs Cross-Entropy](#13-core-loss-functions-mse-vs-cross-entropy)
- [Chapter 2: Supervised Learning: Regression, Classification & Optimization](#chapter-2-supervised-learning-regression-classification--optimization)
  - [2.1 Linear Regression & The Normal Equation](#21-linear-regression--the-normal-equation)
  - [2.2 Gradient Descent Optimization: Batch, SGD, Mini-Batch & Adam](#22-gradient-descent-optimization-batch-sgd-mini-batch--adam)
  - [2.3 Logistic Regression & The Sigmoid Function](#23-logistic-regression--the-sigmoid-function)
  - [2.4 Regularization: L1 Lasso vs L2 Ridge](#24-regularization-l1-lasso-vs-l2-ridge)
- [Chapter 3: Model Evaluation, Bias-Variance Tradeoff & Feature Engineering](#chapter-3-model-evaluation-bias-variance-tradeoff--feature-engineering)
  - [3.1 The Bias-Variance Decomposition](#31-the-bias-variance-decomposition)
  - [3.2 The Confusion Matrix & Classification Metrics](#32-the-confusion-matrix--classification-metrics)
  - [3.3 ROC Curves & AUC Analysis](#33-roc-curves--auc-analysis)
  - [3.4 Feature Scaling & Encoding Pipelines](#34-feature-scaling--encoding-pipelines)
- [Chapter 4: Tree-Based Algorithms & Ensemble Learning](#chapter-4-tree-based-algorithms--ensemble-learning)
  - [4.1 Decision Tree Splitting: Entropy vs Gini Impurity](#41-decision-tree-splitting-entropy-vs-gini-impurity)
  - [4.2 Bagging & Random Forest Architecture](#42-bagging--random-forest-architecture)
  - [4.3 Boosting: GBM, XGBoost & LightGBM](#43-boosting-gbm-xgboost--lightgbm)
- [Chapter 5: Deep Learning Architectures & The Backpropagation Algorithm](#chapter-5-deep-learning-architectures--the-backpropagation-algorithm)
  - [5.1 Multi-Layer Perceptrons & Activation Functions](#51-multi-layer-perceptrons--activation-functions)
  - [5.2 Complete Mathematical Derivation of Backpropagation](#52-complete-mathematical-derivation-of-backpropagation)
  - [5.3 Vanishing Gradients & Normalization Techniques](#53-vanishing-gradients--normalization-techniques)
  - [5.4 Convolutional Neural Networks (CNNs)](#54-convolutional-neural-networks-cnns)
- [Chapter 6: Sequence Models, Transformers, Attention & Modern LLMs](#chapter-6-sequence-models-transformers-attention--modern-llms)
  - [5.1 From RNNs and LSTMs to Attention](#61-from-rnns-and-lstms-to-attention)
  - [6.2 Scaled Dot-Product Self-Attention Mathematics](#62-scaled-dot-product-self-attention-mathematics)
  - [6.3 Multi-Head Attention & Transformer Architecture](#63-multi-head-attention--transformer-architecture)
  - [6.4 Modern LLM Foundations & Retrieval-Augmented Generation (RAG)](#64-modern-llm-foundations--retrieval-augmented-generation-rag)
- [Chapter 7: Solved AI/ML Placement Interview Problems & Assessment Drills](#chapter-7-solved-aiml-placement-interview-problems--assessment-drills)
  - [Solved Problem 1: Gradient Descent Weight Update Derivation](#solved-problem-1-gradient-descent-weight-update-derivation)
  - [Solved Problem 2: Confusion Matrix & F1-Score Numerical](#solved-problem-2-confusion-matrix--f1-score-numerical)
  - [Solved Problem 3: Self-Attention Tensor Dimension Tracing](#solved-problem-3-self-attention-tensor-dimension-tracing)
  - [Self-Assessment Practice Exercises & Verified Solutions](#self-assessment-practice-exercises--verified-solutions)

---

## Chapter 1: Foundations of Machine Learning & Mathematical Fundamentals

### 1.1 Taxonomy of Machine Learning Paradigms
- **Supervised Learning:** Training data consists of input features $X \in \mathbb{R}^{n \times d}$ paired with ground-truth labels $y \in \mathbb{R}^n$. The algorithm learns a mapping function $f: X \to y$.
  - *Regression:* Target $y$ is continuous (e.g., house price, salary).
  - *Classification:* Target $y$ is categorical (e.g., spam vs non-spam, tumor benign vs malignant).
- **Unsupervised Learning:** Training data consists strictly of features $X$ without labels. The algorithm discovers hidden intrinsic structure, clusters, or lower-dimensional representations.
  - *Clustering:* K-Means, DBSCAN, Hierarchical Clustering.
  - *Dimensionality Reduction:* Principal Component Analysis (PCA), t-SNE, UMAP.
- **Reinforcement Learning:** An **Agent** interacts with an **Environment** through **Actions** $a$, receiving **Rewards** $r$ and transitioning between **States** $s$, guided by the Bellman Equation to maximize cumulative expected discounted return.

### 1.2 Essential Linear Algebra & Multivariable Calculus
- **Matrix Multiplication:** Given $A \in \mathbb{R}^{m \times k}$ and $B \in \mathbb{R}^{k \times n}$, product $C = AB \in \mathbb{R}^{m \times n}$:
  $$C_{ij} = \sum_{p=1}^k A_{ip} B_{pj}$$
- **Eigenvalues and Eigenvectors:** For square matrix $A$:
  $$A v = \lambda v, \quad \det(A - \lambda I) = 0$$
  In PCA, principal component directions correspond strictly to the eigenvectors of the data covariance matrix with the largest eigenvalues.
- **The Gradient Vector ($\nabla f$):** The vector of all first-order partial derivatives pointing in the direction of steepest ascent:
  $$\nabla_\theta J(\theta) = \left[ \frac{\partial J}{\partial \theta_0}, \frac{\partial J}{\partial \theta_1}, \dots, \frac{\partial J}{\partial \theta_d} \right]^T$$

### 1.3 Core Loss Functions: MSE vs Cross-Entropy
- **Mean Squared Error (MSE) — For Regression:**
  $$J(\theta) = \frac{1}{2m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})^2$$
- **Binary Cross-Entropy (BCE) / Log Loss — For Binary Classification:**
  $$J(\theta) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)} \ln(\hat{y}^{(i)}) + (1 - y^{(i)}) \ln(1 - \hat{y}^{(i)}) \right]$$
  Where $\hat{y} = \sigma(\theta^T x) \in [0, 1]$.
- **Categorical Cross-Entropy — For Multi-Class ($K$ classes) with Softmax:**
  $$J(\theta) = -\sum_{i=1}^m \sum_{k=1}^K y_k^{(i)} \ln(\hat{y}_k^{(i)}), \quad \hat{y}_k = \frac{e^{z_k}}{\sum_{j=1}^K e^{z_j}}$$

---

## Chapter 2: Supervised Learning: Regression, Classification & Optimization

### 2.1 Linear Regression & The Normal Equation
Model hypothesis:
$$\hat{y} = \theta_0 + \theta_1 x_1 + \dots + \theta_d x_d = \theta^T x$$
In matrix form with design matrix $X \in \mathbb{R}^{m \times (d+1)}$:
$$\hat{y} = X\theta$$

**Closed-Form Analytical Solution (The Normal Equation):**
Setting $\nabla_\theta J(\theta) = 0$:
$$\theta = (X^T X)^{-1} X^T y$$
- *Computational Complexity:* Matrix inversion $(X^T X)^{-1}$ takes $O(d^3)$ time. For $d > 10,000$ features, the normal equation becomes prohibitively slow, necessitating iterative Gradient Descent.

### 2.2 Gradient Descent Optimization: Batch, SGD, Mini-Batch & Adam
General parameter update rule:
$$\theta := \theta - \alpha \nabla_\theta J(\theta)$$
Where $\alpha$ is the learning rate.

| Optimization Algorithm | Samples per Gradient Step | Convergence Behavior | Computational Efficiency |
|:---|:---|:---|:---|
| **Batch Gradient Descent** | All $m$ samples in dataset | Smooth, deterministic trajectory toward global minimum. | Slow for massive datasets; requires entire dataset in RAM. |
| **Stochastic GD (SGD)** | Exactly $1$ random sample | Highly oscillatory/noisy; can escape local minima. | Fast updates, but oscillations can prevent settling at exact minimum. |
| **Mini-Batch GD** | Batch size $B$ (e.g., 32, 64, 128) | Balanced stability with vectorized GPU matrix execution. | **Industry standard** for training modern neural networks. |
| **Adam Optimizer** | Mini-batch with adaptive learning rates | Computes exponentially decaying moving averages of past gradients (momentum $m_t$) and squared gradients ($v_t$). | Fastest convergence, default optimizer for deep learning. |

### 2.3 Logistic Regression & The Sigmoid Function
Logistic regression maps real-valued linear predictions $z = \theta^T x$ into probabilities $[0, 1]$ via the **Sigmoid (Logistic) Function**:
$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

- **Property of Sigmoid Derivative:**
  $$\frac{d\sigma(z)}{dz} = \sigma(z) \cdot (1 - \sigma(z))$$
- **Decision Boundary:** The model predicts positive class $y = 1$ when $\hat{y} \ge 0.5 \iff z = \theta^T x \ge 0$.

### 2.4 Regularization: L1 Lasso vs L2 Ridge
Prevents overfitting by penalizing large model weight magnitudes:

- **L2 Regularization (Ridge Regression):**
  $$J_{\text{Ridge}}(\theta) = \text{MSE} + \lambda \sum_{j=1}^d \theta_j^2$$
  - Weight update: $\theta_j := \theta_j (1 - 2\alpha\lambda) - \alpha \frac{\partial \text{MSE}}{\partial \theta_j}$ (Weight Decay).
  - Shrinks all weights smoothly toward zero; handles multicollinearity effectively.
- **L1 Regularization (Lasso Regression):**
  $$J_{\text{Lasso}}(\theta) = \text{MSE} + \lambda \sum_{j=1}^d |\theta_j|$$
  - The L1 diamond constraint region possesses sharp corners along axes, forcing less informative coefficients to become **identically zero**.
  - Serves as an embedded **Automatic Feature Selection** mechanism.

---

## Chapter 3: Model Evaluation, Bias-Variance Tradeoff & Feature Engineering

### 3.1 The Bias-Variance Decomposition
Expected test error decomposes into three fundamental components:
$$\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}[\hat{f}(x)]^2 + \text{Var}[\hat{f}(x)] + \sigma^2 \text{ (Irreducible Error)}$$

```
Error ^
      |           Total Error
      |         \             /
      |          \    *      /
      |  Variance \  / \    /  Variance (Overfitting)
      |            \/   \  /
      |  Bias       \    \/
      |  (Underfitting)   \  Bias
      +------------------------------------> Model Complexity
```

- **High Bias (Underfitting):** Model is overly simplistic and makes strong incorrect assumptions (e.g., fitting a linear model to a cubic dataset). High error on both training and test sets.
  - *Remedy:* Increase model capacity, add polynomial features, reduce regularization $\lambda$.
- **High Variance (Overfitting):** Model memorizes random noise in the training set (e.g., deep unpruned decision tree). Low training error but high test error.
  - *Remedy:* Add more training data, apply L1/L2 regularization, feature selection, prune tree depth, use bagging ensemble.

### 3.2 The Confusion Matrix & Classification Metrics
Given binary ground truth ($P, N$) and predictions:

```
                  Predicted Positive   Predicted Negative
Actual Positive: [ True Positive (TP)  | False Negative (FN) - Type II Error ]
Actual Negative: [ False Positive (FP) | True Negative (TN)  - Type I Error  ]
```

1. **Accuracy:** $\frac{TP + TN}{TP + TN + FP + FN}$ (Misleading in imbalanced classes!).
2. **Precision:** $\frac{TP}{TP + FP}$ — "Out of all instances the model predicted positive, how many were actually positive?" (Crucial when False Positives are expensive, e.g. spam filters).
3. **Recall (Sensitivity):** $\frac{TP}{TP + FN}$ — "Out of all actual positive instances, how many did the model capture?" (Crucial when False Negatives are fatal, e.g. cancer diagnosis, fraud detection).
4. **F1-Score:** The harmonic mean of Precision and Recall:
   $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2TP}{2TP + FP + FN}$$

### 3.3 ROC Curves & AUC Analysis
- **Receiver Operating Characteristic (ROC) Curve:** Plots **True Positive Rate** (Recall, Y-axis) against **False Positive Rate** ($FPR = \frac{FP}{FP + TN}$, X-axis) across all possible classification probability thresholds ($0.0 \to 1.0$).
- **Area Under Curve (AUC-ROC):**
  - $\text{AUC} = 1.0$: Perfect classifier.
  - $\text{AUC} = 0.5$: Random guess (diagonal line).
  - Represents the probability that the classifier ranks a randomly chosen positive instance higher than a randomly chosen negative instance.

---

## Chapter 4: Tree-Based Algorithms & Ensemble Learning

### 4.1 Decision Tree Splitting: Entropy vs Gini Impurity
- **Shannon Entropy ($H(S)$):** Measures information disorder:
  $$H(S) = -\sum_{i=1}^C p_i \log_2(p_i)$$
  - For binary split with equal classes ($p = 0.5$): $H(S) = - (0.5 \log_2 0.5 + 0.5 \log_2 0.5) = 1.0\text{ bit}$ (maximum uncertainty).
  - For pure node ($p = 1.0$): $H(S) = 0\text{ bits}$.
- **Information Gain ($IG$):**
  $$IG(S, A) = H(S) - \sum_{v \in \text{Values}(A)} \frac{|S_v|}{|S|} H(S_v)$$
- **Gini Impurity ($G$):** Computationally faster because it avoids logarithm calculations:
  $$G(S) = 1 - \sum_{i=1}^C p_i^2$$

### 4.2 Bagging & Random Forest Architecture
- **Bagging (Bootstrap Aggregating):** Trains $B$ independent base learners in parallel on distinct bootstrap samples (sampling $m$ instances with replacement). Final prediction is obtained via majority voting (classification) or averaging (regression).
- **Random Forest:** Enhances bagging by introducing **Random Feature Subspace Sampling**:
  - At every candidate split in every tree, the algorithm considers strictly a random subset of $k$ features:
    $$k = \sqrt{d} \text{ for classification}, \quad k = \frac{d}{3} \text{ for regression}$$
  - **Decorrelation Effect:** Prevents dominant features from appearing at the root of every tree, decorrelating the trees and drastically reducing ensemble variance!

### 4.3 Boosting: GBM, XGBoost & LightGBM
Unlike bagging, **Boosting** trains trees sequentially, where each new tree is trained to correct the residual errors made by the previous ensemble:

```
[ Input X ] -> [ Tree 1 ] -> Calculates Residuals e1 = y - y_hat1
                     |
                     v
               [ Tree 2 ] -> Fits on Residuals e1 -> Calculates Residuals e2
                     |
                     v
               [ Tree 3 ] -> Fits on Residuals e2 ...
```

- **XGBoost (Extreme Gradient Boosting):**
  - Approximates the loss function using a **Second-Order Taylor Series Expansion** (computing both first derivative / gradient $g_i$ and second derivative / hessian $h_i$).
  - Incorporates explicit regularization parameters ($\gamma$ penalty per tree leaf, $\lambda$ L2 regularization on leaf weights) directly into the objective function.
  - Employs exact and quantile sketch greedy split-finding algorithms with built-in handling for sparse matrices and missing values.

---

## Chapter 5: Deep Learning Architectures & The Backpropagation Algorithm

### 5.1 Multi-Layer Perceptrons & Activation Functions
- **Perceptron Equation:** $z = W x + b, \quad a = g(z)$
- **Non-Linear Activation Functions:**
  - **ReLU (Rectified Linear Unit):** $g(z) = \max(0, z)$. Derivative is $1$ if $z > 0$, $0$ if $z \le 0$. Blazing-fast computation; eliminates vanishing gradient in positive domain. (Susceptible to "Dying ReLU" if large gradients push activations into permanently negative territory).
  - **Leaky ReLU:** $g(z) = \max(\alpha z, z)$, with $\alpha = 0.01$. Prevents dying neurons.
  - **GELU (Gaussian Error Linear Unit):** Smooth non-linearity used in modern Transformers (BERT, GPT).

### 5.2 Complete Mathematical Derivation of Backpropagation
Consider an $L$-layer neural network with loss $J$:
Let $z^{[l]} = W^{[l]} a^{[l-1]} + b^{[l]}$, and $a^{[l]} = g(z^{[l]})$.

By the multivariable chain rule:
$$\frac{\partial J}{\partial W^{[l]}} = \frac{\partial J}{\partial z^{[l]}} \cdot \frac{\partial z^{[l]}}{\partial W^{[l]}} = \delta^{[l]} (a^{[l-1]})^T$$
Where the error vector $\delta^{[l]}$ is defined as:
$$\delta^{[l]} = \frac{\partial J}{\partial z^{[l]}}$$

**Backward Error Recursion:**
1. **For Output Layer $L$ (with Softmax and Cross-Entropy):**
   $$\delta^{[L]} = a^{[L]} - y$$
2. **For Hidden Layer $l$:**
   $$\delta^{[l]} = \left( (W^{[l+1]})^T \delta^{[l+1]} \right) \odot g'(z^{[l]})$$
   Where $\odot$ represents the element-wise Hadamard product.
3. **Weight & Bias Gradient Updates:**
   $$\frac{\partial J}{\partial W^{[l]}} = \frac{1}{m} \delta^{[l]} (a^{[l-1]})^T$$
   $$\frac{\partial J}{\partial b^{[l]}} = \frac{1}{m} \sum_{i=1}^m \delta^{[l](i)}$$

### 5.3 Vanishing Gradients & Normalization Techniques
- **Vanishing Gradients:** When using Sigmoid or Tanh activations, derivatives satisfy $|g'(z)| \le 0.25$. As gradients multiply backward across 50 layers via chain rule, $\prod_{l=1}^{50} (0.25) \approx 0$, freezing weights in the earliest layers.
- **Batch Normalization (Ioffe & Szegedy):** Normalizes activations across the mini-batch dimension to mean 0 and variance 1, followed by learned scale ($\gamma$) and shift ($\beta$) parameters. Reduces internal covariate shift and stabilizes deep network training.

---

## Chapter 6: Sequence Models, Transformers, Attention & Modern LLMs

### 6.1 From RNNs and LSTMs to Attention
- **Recurrent Neural Networks (RNNs):** Process sequences sequentially one token at a time: $h_t = \tanh(W x_t + U h_{t-1} + b)$.
  - *Catastrophic Limitation:* Gradients vanish over sequences longer than ~20 steps; cannot parallelize training because step $t$ strictly requires step $t-1$.
- **LSTMs (Hochreiter & Schmidhuber):** Introduced an explicit **Cell State ($C_t$)** regulated by 3 non-linear gates: Forget Gate ($f_t$), Input Gate ($i_t$), and Output Gate ($o_t$). Improved long-term memory but remained fundamentally sequential.

### 6.2 Scaled Dot-Product Self-Attention Mathematics
Introduced by Vaswani et al. (2017) in *"Attention Is All You Need"*, the self-attention mechanism processes all tokens simultaneously in parallel.

For an input sequence matrix $X \in \mathbb{R}^{n \times d_{\text{model}}}$:
Each token is projected into three distinct vector spaces via learned weight matrices:
$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$
Where $W_Q, W_K \in \mathbb{R}^{d_{\text{model}} \times d_k}$, and $W_V \in \mathbb{R}^{d_{\text{model}} \times d_v}$.

**The Scaled Dot-Product Attention Equation:**
$$\text{Attention}(Q, K, V) = \text{Softmax}\left( \frac{Q K^T}{\sqrt{d_k}} \right) V$$

```
Step 1: Compute Raw Similarity Matrix:  S = Q * K^T  (Shape: n x n)
Step 2: Scale by 1 / sqrt(d_k):         Prevents dot products from exploding for large dimensions
                                        (which would cause Softmax gradients to vanish!)
Step 3: Apply Softmax:                  Produces probability weights summing to 1 across rows
Step 4: Multiply by Value Matrix V:     Computes weighted sum of value representations
```

### 6.3 Multi-Head Attention & Transformer Architecture
Instead of computing attention once with large dimension $d_{\text{model}}$, **Multi-Head Attention (MHA)** projects queries, keys, and values $h$ times into distinct lower-dimensional subspaces ($d_k = d_{\text{model}} / h$):

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \dots, \text{head}_h) W_O$$
Where:
$$\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$

- Allows the model to attend simultaneously to information from different representation subspaces (e.g., one head focuses on grammatical syntax, another on semantic pronoun references, another on temporal markers).

### 6.4 Modern LLM Foundations & Retrieval-Augmented Generation (RAG)
- **Autoregressive Decoder LLMs (GPT-3, GPT-4, Llama 3):** Employ causal masking (lower-triangular mask) to prevent tokens from attending to future tokens, trained on the next-token prediction objective: $\max \sum \log P(w_t \mid w_1, \dots, w_{t-1})$.
- **Retrieval-Augmented Generation (RAG):** Overcomes LLM hallucinations and static training cutoffs by grounding generations in external knowledge:
  1. Chunk external documents (e.g. 500-token chunks with 50-token overlap).
  2. Generate dense vector embeddings using an embedding model (e.g., text-embedding-ada-002, BGE).
  3. Store and index embeddings in a Vector Database (Qdrant, Pinecone, Milvus) using HNSW (Hierarchical Navigable Small World) graphs.
  4. At query time, compute cosine similarity between the user query embedding and document chunks:
     $$\text{Cosine Similarity} = \frac{u \cdot v}{\|u\| \|v\|}$$
  5. Inject the top-$k$ relevant chunks into the LLM system prompt as verified context.

---

## Chapter 7: Solved AI/ML Placement Interview Problems & Assessment Drills

### Solved Problem 1: Gradient Descent Weight Update Derivation
- **Problem:** Derive the exact gradient update formula for single-variable linear regression with Mean Squared Error loss:
  $$J(w, b) = \frac{1}{2m} \sum_{i=1}^m (w x^{(i)} + b - y^{(i)})^2$$
- **Solution:**
  1. Compute partial derivative with respect to weight $w$:
     $$\frac{\partial J}{\partial w} = \frac{1}{2m} \sum_{i=1}^m 2(w x^{(i)} + b - y^{(i)}) \cdot \frac{\partial}{\partial w}(w x^{(i)} + b - y^{(i)})$$
     $$\frac{\partial J}{\partial w} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x^{(i)}$$
  2. Compute partial derivative with respect to bias $b$:
     $$\frac{\partial J}{\partial b} = \frac{1}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})$$
  3. The gradient update rules:
     $$w := w - \frac{\alpha}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)}) x^{(i)}$$
     $$b := b - \frac{\alpha}{m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})$$

### Solved Problem 2: Confusion Matrix & F1-Score Numerical
- **Problem (TCS Digital / Amazon Placement):** A machine learning model is evaluated on a fraud test set of 1,000 transactions:
  - Total actual fraudulent transactions: 100
  - Total actual legitimate transactions: 900
  - The model correctly flags 80 fraudulent transactions as fraud.
  - The model falsely flags 20 legitimate transactions as fraud.
  Calculate: Accuracy, Precision, Recall, and F1-Score.
- **Solution:**
  1. Construct Confusion Matrix:
     - Actual Positives $= 100 \implies TP = 80, \ FN = 100 - 80 = 20$.
     - Actual Negatives $= 900 \implies FP = 20, \ TN = 900 - 20 = 880$.
  2. Accuracy:
     $$\text{Accuracy} = \frac{TP + TN}{\text{Total}} = \frac{80 + 880}{1000} = \frac{960}{1000} = \mathbf{96.0\%}$$
  3. Precision:
     $$\text{Precision} = \frac{TP}{TP + FP} = \frac{80}{80 + 20} = \frac{80}{100} = \mathbf{0.80 \ (80.0\%)}$$
  4. Recall (Sensitivity):
     $$\text{Recall} = \frac{TP}{TP + FN} = \frac{80}{80 + 20} = \frac{80}{100} = \mathbf{0.80 \ (80.0\%)}$$
  5. F1-Score:
     $$F_1 = 2 \times \frac{0.80 \times 0.80}{0.80 + 0.80} = \frac{1.28}{1.60} = \mathbf{0.80 \ (80.0\%)}$$

### Solved Problem 3: Self-Attention Tensor Dimension Tracing
- **Problem:** In a Transformer layer, sequence length is $n = 512$, and model dimension is $d_{\text{model}} = 768$. Number of attention heads is $h = 12$.
  1. What is the dimension $d_k$ of each individual attention head?
  2. What is the exact tensor shape of $Q, K, V$ before head splitting?
  3. What is the shape of the attention score matrix $Q K^T$ for a single head?
- **Solution:**
  1. Dimension per head:
     $$d_k = \frac{d_{\text{model}}}{h} = \frac{768}{12} = \mathbf{64}$$
  2. Tensor shapes:
     $$X \in \mathbb{R}^{512 \times 768}, \quad W_Q \in \mathbb{R}^{768 \times 768} \implies Q, K, V \in \mathbb{R}^{\mathbf{512 \times 768}}$$
  3. For a single head, $Q_i \in \mathbb{R}^{512 \times 64}$ and $K_i \in \mathbb{R}^{512 \times 64}$:
     $$Q_i K_i^T \in \mathbb{R}^{512 \times 64} \times \mathbb{R}^{64 \times 512} = \mathbb{R}^{\mathbf{512 \times 512}}$$
     *(The attention matrix has size $n \times n = 512 \times 512$, quadratic with sequence length).*

---

### Self-Assessment Practice Exercises & Verified Solutions:

1. **Exercise 1 (Scaling Factor in Attention):** Why does the scaled dot-product attention formula divide $Q K^T$ by $\sqrt{d_k}$?
   - *Solution:* For large dimensions $d_k$, the dot products grow large in magnitude, pushing the Softmax function into regions with extremely tiny gradients (near 0 or 1), leading to vanishing gradients during backpropagation. Dividing by $\sqrt{d_k}$ scales the variance of the dot products back to 1.

2. **Exercise 2 (L1 vs L2 Weight Shrinkage):** Why does L1 regularization produce sparse models with zero coefficients while L2 regularization only shrinks coefficients close to zero?
   - *Solution:* The L1 norm penalty contour is an $L_1$ diamond with sharp non-differentiable vertices touching the parameter axes. When the elliptical contours of the MSE loss intersect the constraint boundary, they frequently hit these axis vertices where one or more coordinates are identically zero. The L2 norm constraint is a smooth circle/hypersphere, which almost never intersects the loss ellipse exactly on an axis.

3. **Exercise 3 (Out-of-Bag Error):** What is the theoretical percentage of dataset samples left out of any single bootstrap sample in Random Forest?
   - *Solution:* When sampling $m$ items with replacement, probability of an item NOT being picked in a single draw is $1 - 1/m$. Over $m$ draws: $\lim_{m \to \infty} (1 - 1/m)^m = \frac{1}{e} \approx \mathbf{36.8\%}$. These ~36.8% unpicked samples form the Out-of-Bag (OOB) validation set.

4. **Exercise 4 (ReLU Dead Neurons):** Under what condition does a neuron with a standard ReLU activation become a "Dead ReLU"?
   - *Solution:* If a large gradient causes the neuron's weights to update such that the weighted input $z = Wx + b \le 0$ for all training examples, the activation outputs 0 and the gradient $g'(z) = 0$. Consequently, the neuron never updates again during backpropagation and remains permanently inactive.

5. **Exercise 5 (RAG Cosine Similarity):** If two normalized document embedding vectors have a dot product of $1.0$, what is the geometric angle between them and what does it indicate?
   - *Solution:* Angle $\theta = 0^\circ$ ($\cos 0^\circ = 1.0$). It indicates that the two text passages have identical directional semantic embeddings in vector space.
"""

AI_ML_EXPANDED_QUESTIONS = [
    {
        "chapter_num": 6,
        "chapter_title": "Sequence Models, Transformers, Attention & Modern LLMs",
        "subtopic": "Scaled Dot-Product Attention Equation",
        "question": "In the Transformer Self-Attention mechanism, what is the purpose of dividing the dot product Q * K^T by sqrt(d_k)?",
        "options": [
            "To prevent the dot products from growing excessively large, which would cause Softmax gradients to vanish",
            "To convert the matrix into a lower-triangular causal mask",
            "To reduce the number of parameters in the multi-head projection",
            "To invert the token positions in the sequence"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [AI/ML Prescribed Textbook — Chapter 6: Transformers & Attention]\nAs vector dimension d_k increases, the magnitude of the dot product grows large, pushing the Softmax function into flat regions with near-zero gradients. Scaling by 1/sqrt(d_k) preserves unit variance and healthy gradient flow.",
        "difficulty": "medium",
    },
    {
        "chapter_num": 3,
        "chapter_title": "Model Evaluation, Bias-Variance Tradeoff & Feature Engineering",
        "subtopic": "Classification Metrics in Imbalanced Datasets",
        "question": "Which evaluation metric is the most appropriate when evaluating a credit card fraud detection model where only 0.1% of transactions are fraudulent?",
        "options": [
            "Precision, Recall, and F1-Score (or PR-AUC)",
            "Raw Classification Accuracy",
            "Mean Absolute Percentage Error",
            "Adjusted R-Squared"
        ],
        "correct_option_index": 0,
        "explanation": "📖 [AI/ML Prescribed Textbook — Chapter 3: Model Evaluation]\nIn severely imbalanced datasets, a trivial model predicting 'Legitimate' for every transaction achieves 99.9% accuracy while failing to detect any fraud. Precision, Recall, and the F1-Score are required to measure actual detection efficacy.",
        "difficulty": "easy",
    }
]
