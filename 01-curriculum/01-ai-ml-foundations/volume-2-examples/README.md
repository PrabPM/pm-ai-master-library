# Example scripts for AI, Machine Learning, Deep Learning, and LLMs (Version 2)

Every code listing in the book is an excerpt of a script in this folder, and every
`Output:` block in the book was pasted from running it. Each script also checks the
book's hand-worked numbers with `assert`, so a clean run is a proof that the worked
examples are right.

## Set up and run

```bash
# from the folder that contains volume-2-examples/
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r volume-2-examples/requirements.txt
./volume-2-examples/run_all.sh                      # everything
.venv/bin/python volume-2-examples/ch00_payflow_data.py   # or one chapter
```

Without `uv`: `python3 -m venv .venv && .venv/bin/pip install -r volume-2-examples/requirements.txt`.

The scripts need Python 3.13 or later, use fixed random seeds, download nothing and
call no outside service. Scripts that draw one of the book's figures save it as an SVG
in a `volume-2-assets` folder next to this one.

## Scripts by chapter

| Chapter | Script |
|---|---|
| 0 | `ch00_payflow_data.py` |
| 1 | `ch01_linear_regression.py` |
| 2 | `ch02_logistic_regression.py` |
| 3 | `ch03_trees_forests.py` |
| 4 | `ch04_svm.py` |
| 5 | `ch05_knn_naive_bayes.py` |
| 6 | `ch06_bias_variance.py` |
| 7 | `ch07_clustering.py` |
| 8 | `ch08_dimensionality_reduction.py` |
| 9 | `ch09_evaluation.py` |
| 10 | `ch10_features.py` |
| 11 | `ch11_boosting_shap.py` |
| 12 | `ch12_backprop.py` |
| 13 | `ch13_convolution.py` |
| 14 | `ch14_rnn_attention.py` |
| 15 | `ch15_transformer.py` |
| 16 | `ch16_transfer_learning.py` |
| 17 | `ch17_generative.py` |
| 18 | `ch18_stabilizers.py` |
| 19 | `ch19_next_token.py` |
| 20 | `ch20_bpe.py` |
| 21 | `ch21_embeddings.py` |
| 22 | `ch22_pretraining.py` |
| 23 | `ch23_feedback.py` |
| 24 | `ch24_lora.py` |
| 25 | `ch25_prompting.py` |
| 26 | `ch26_rag.py` |
| 27 | `ch27_agent.py` |
| 28 | `ch28_evaluation.py` |
| 29 | `ch29_context_cache_quant.py` |
| 30 | `ch30_open_weights.py` |
| 31 | `ch31_multimodal.py` |
| 32 | `ch32_retry_mdp.py` |
| 33 | `ch33_value_iteration.py` |
| 34 | `ch34_q_learning_sarsa.py` |
| 35 | `ch35_linear_dqn.py` |
| 36 | `ch36_policy_gradient.py` |
| 37 | `ch37_bandits.py` |
| 38 | `ch38_uninformed_search.py` |
| 39 | `ch39_astar.py` |
| 40 | `ch40_adversarial_search.py` |
| 41 | `ch41_behavior_tree.py` |
| 42 | `ch42_mcts.py` |
| 43 | `ch43_belief_update.py` |
| 44 | `ch44_ts_features.py` |
| 45 | `ch45_lookahead.py` |
| 46 | `ch46_portfolio.py` |
| 47 | `ch47_trading_costs.py` |
| 48 | `ch48_churn_retention.py` |
| 49 | `ch49_fraud_detection.py` |
| 50 | `ch50_dynamic_pricing.py` |
| 51 | `ch51_ops_assistant.py` |
| 52 | `ch52_document_automation.py` |
| 53 | `ch53_recommendations.py` |
| 54 | `ch54_marketing_voc.py` |
| 55 | `ch55_experiments_inference.py` |
| 56 | `ch56_model_card.py` |
| 57 | `ch57_ai_metrics.py` |
| 58 | `ch58_build_buy_finetune.py` |
| 59 | `ch59_fairness.py` |
| 60 | `ch60_roadmap.py` |
| 61 | `ch61_problem_framing.py` |
| 62 | `ch62_baselines.py` |
| 63 | `ch63_thresholds_value.py` |
| 64 | `ch64_uplift.py` |
| 65 | `ch65_data_feasibility.py` |
| 66 | `ch66_guardrails.py` |
| 67 | `ch67_uncertainty_patterns.py` |
| 68 | `ch68_calibration.py` |
| 69 | `ch69_citations_provenance.py` |
| 70 | `ch70_reviewer_queue.py` |
| 71 | `ch71_graceful_degradation.py` |
| 72 | `ch72_audit_accessibility.py` |
| 73 | `ch73_contracts_lineage.py` |
| 74 | `ch74_point_in_time.py` |
| 75 | `ch75_streaming_parity.py` |
| 76 | `ch76_versions_embeddings.py` |
| 77 | `ch77_labeling_kappa_budget.py` |
| 78 | `ch78_active_weak.py` |
| 79 | `ch79_flywheel_selective_labels.py` |
| 80 | `ch80_tenant_isolation.py` |
| 81 | `ch81_tracking_registry.py` |
| 82 | `ch82_validation_gates.py` |
| 83 | `ch83_prompt_golden_metamorphic.py` |
| 84 | `ch84_canary_simulation.py` |
| 85 | `ch85_drift_psi.py` |
| 86 | `ch86_runbook_checklist.py` |
| 87 | `ch87_batching.py` |
| 88 | `ch88_kv_cache.py` |
| 89 | `ch89_speculative.py` |
| 90 | `ch90_capacity.py` |
| 91 | `ch91_router_cache.py` |
| 92 | `ch92_cost.py` |
| 93 | `ch93_distributed_training.py` |
| 94 | `ch94_data_curation.py` |
| 95 | `ch95_mixture_of_experts.py` |
| 96 | `ch96_long_context.py` |
| 97 | `ch97_state_space.py` |
| 98 | `ch98_graph_neural_networks.py` |
| 99 | `ch99_knowledge_graphs.py` |
| 100 | `ch100_hybrid_retrieval.py` |
| 101 | `ch101_vector_indexes.py` |
| 102 | `ch102_distillation.py` |
| 103 | `ch103_document_understanding.py` |
| 104 | `ch104_contrastive_edge.py` |
| 105 | `ch105_recommenders.py` |
| 106 | `ch106_time_series.py` |
| 107 | `ch107_agent_loop.py` |
| 108 | `ch108_tool_gateway.py` |
| 109 | `ch109_memory_planning.py` |
| 110 | `ch110_approval_audit.py` |
| 111 | `ch111_agent_rag_eval.py` |
| 112 | `ch112_tracing_cost.py` |
| 113 | `ch113_online_eval.py` |
| 114 | `ch114_prompt_injection.py` |
| 115 | `ch115_privacy.py` |
| 116 | `ch116_provenance.py` |
| 117 | `ch117_flywheel.py` |
| 118 | `ch118_build_buy.py` |
| 119 | `ch119_pricing_economics.py` |
| 120 | `ch120_governance_calendar.py` |
| 121 | `ch121_domain_gates.py` |
| 122 | `ch122_silent_failure.py` |
| 123 | `ch123_lab01_threshold_cost.py`, `ch123_lab02_overfitting.py`, `ch123_lab03_backprop_step.py`, `ch123_lab04_retrieval_metrics.py`, `ch123_lab05_bandit_retry.py`, `ch123_lab06_lookahead.py`, `ch123_lab07_uplift.py`, `ch123_lab08_calibration.py`, `ch123_lab09_kappa.py`, `ch123_lab10_psi.py`, `ch123_lab11_prefix_cache.py`, `ch123_lab12_privacy_budget.py` |
| 124 | `ch124_case1_fraud_ship_or_hold.py`, `ch124_case2_assistant_rollout.py`, `ch124_case3_tune_retrieve_or_bigger.py`, `ch124_case4_drift_incident.py` |
