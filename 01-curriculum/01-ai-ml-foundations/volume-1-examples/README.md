# Example scripts for Foundational Mathematics for AI, ML, and LLMs (Version 2)

Every code listing in the book is an excerpt of a script in this folder, and every
`Output:` block in the book was pasted from running it. Each script also checks the
book's hand-worked numbers with `assert`, so a clean run is a proof that the worked
examples are right.

## Set up and run

```bash
# from the folder that contains volume-1-examples/
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r volume-1-examples/requirements.txt
./volume-1-examples/run_all.sh                      # everything
.venv/bin/python volume-1-examples/ch00_reading_math.py   # or one chapter
```

Without `uv`: `python3 -m venv .venv && .venv/bin/pip install -r volume-1-examples/requirements.txt`.

The scripts need Python 3.13 or later, use fixed random seeds, download nothing and
call no outside service. Scripts that draw one of the book's figures save it as an SVG
in a `volume-1-assets` folder next to this one.

## Scripts by chapter

| Chapter | Script |
|---|---|
| 0 | `ch00_reading_math.py` |
| 1 | `ch01_vectors.py` |
| 2 | `ch02_matrices.py` |
| 3 | `ch03_matmul.py` |
| 4 | `ch04_independence.py` |
| 5 | `ch05_det_trace.py` |
| 6 | `ch06_linear_systems.py` |
| 7 | `ch07_eigen.py` |
| 8 | `ch08_pca.py` |
| 9 | `ch09_svd.py` |
| 10 | `ch10_high_dimensions.py` |
| 11 | `ch11_cosine.py` |
| 12 | `ch12_vector_search.py` |
| 13 | `ch13_probability_spaces.py` |
| 14 | `ch14_conditional_probability.py` |
| 15 | `ch15_bayes.py` |
| 16 | `ch16_random_variables.py` |
| 17 | `ch17_expectation_variance.py` |
| 18 | `ch18_distributions.py` |
| 19 | `ch19_clt.py` |
| 20 | `ch20_mle.py` |
| 21 | `ch21_map.py` |
| 22 | `ch22_hypothesis_testing.py` |
| 23 | `ch23_many_tests.py` |
| 24 | `ch24_limits.py` |
| 25 | `ch25_derivatives.py` |
| 26 | `ch26_gradient.py` |
| 27 | `ch27_directional.py` |
| 28 | `ch28_backprop.py` |
| 29 | `ch29_jacobian.py` |
| 30 | `ch30_hessian.py` |
| 31 | `ch31_taylor.py` |
| 32 | `ch32_convexity_saddles.py` |
| 33 | `ch33_gradient_descent.py` |
| 34 | `ch34_sgd_minibatch.py` |
| 35 | `ch35_momentum_adam.py` |
| 36 | `ch36_lagrange_budget.py` |
| 37 | `ch37_kkt_svm.py` |
| 38 | `ch38_entropy.py` |
| 39 | `ch39_joint_conditional_entropy.py` |
| 40 | `ch40_cross_entropy.py` |
| 41 | `ch41_kl_divergence.py` |
| 42 | `ch42_mutual_information.py` |
| 43 | `ch43_perplexity.py` |
| 44 | `ch44_graphs.py` |
| 45 | `ch45_trees.py` |
| 46 | `ch46_bfs_dfs.py` |
| 47 | `ch47_dag_pipeline.py` |
| 48 | `ch48_propositional_logic.py` |
| 49 | `ch49_resolution.py` |
| 50 | `ch50_rule_engine.py` |
| 51 | `ch51_stationarity.py` |
| 52 | `ch52_arma.py` |
| 53 | `ch53_returns.py` |
| 54 | `ch54_volatility.py` |
| 55 | `ch55_sharpe_information_ratio.py` |
| 56 | `ch56_forecasting.py` |
| 57 | `ch57_lab01_similarity.py`, `ch57_lab02_pca.py`, `ch57_lab03_bayes.py`, `ch57_lab04_ab_test.py`, `ch57_lab05_backprop.py`, `ch57_lab06_learning_rate.py`, `ch57_lab07_drift_kl.py`, `ch57_lab08_fraud_ring.py`, `ch57_lab09_promo_tail.py` |
| 58 | `ch58_case01_fraud_lift.py`, `ch58_case02_training_run.py`, `ch58_case03_vector_index.py` |
| 59 | `ch59_spoken_answer.py` |
| 60 | `ch60_question_bank_numbers.py` |
