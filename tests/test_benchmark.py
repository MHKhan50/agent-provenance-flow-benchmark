import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from generate_dataset import build_scenarios
from benchmark import evaluate_scenario, evaluate_all, summarise


class ProvenanceFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scenarios = build_scenarios()
        cls.by_type = {}
        for row in cls.scenarios:
            cls.by_type.setdefault(row["scenario_type"], row)

    def test_generator_is_deterministic(self):
        self.assertEqual(build_scenarios(), build_scenarios())

    def test_default_dataset_size_and_scenario_coverage(self):
        self.assertEqual(len(self.scenarios), 1500)
        expected = {
            "trusted_only",
            "benign_untrusted_data",
            "helpful_third_party_instruction",
            "direct_injection",
            "transformed_injection",
            "mixed_helpful_and_malicious",
        }
        for seed in (17, 29, 43, 71, 101):
            present = {
                r["scenario_type"] for r in self.scenarios if int(r["seed"]) == seed
            }
            self.assertEqual(present, expected)
        attacks = sum(r["attack_present"] for r in self.scenarios)
        self.assertGreater(attacks, 0)
        self.assertLess(attacks, len(self.scenarios))

    def test_no_guard_executes_all_injected_actions(self):
        attacks = [r for r in self.scenarios if r["attack_present"]]
        for scenario in attacks:
            result = evaluate_scenario(scenario, "no_guard")
            self.assertEqual(result["malicious_action_executed"], 1)

    def test_direct_only_taint_fails_after_transform(self):
        scenario = self.by_type["transformed_injection"]
        self.assertGreater(scenario["transform_depth"], 0)
        result = evaluate_scenario(scenario, "direct_only_taint")
        self.assertEqual(result["malicious_action_executed"], 1)

    def test_strict_taint_blocks_data_dependent_primary_action(self):
        scenario = self.by_type["benign_untrusted_data"]
        result = evaluate_scenario(scenario, "strict_taint")
        self.assertEqual(result["primary_action_executed"], 0)

    def test_field_provenance_guard_preserves_primary_utility(self):
        for scenario in self.scenarios:
            result = evaluate_scenario(scenario, "field_provenance_guard")
            self.assertEqual(result["primary_action_executed"], 1)

    def test_field_provenance_guard_blocks_all_attack_actions(self):
        attacks = [r for r in self.scenarios if r["attack_present"]]
        for scenario in attacks:
            result = evaluate_scenario(scenario, "field_provenance_guard")
            self.assertEqual(result["malicious_action_executed"], 0)

    def test_in_scope_helpful_instructions_are_preserved(self):
        helpful = [r for r in self.scenarios if r["helpful_instruction"]]
        for scenario in helpful:
            result = evaluate_scenario(scenario, "field_provenance_guard")
            self.assertEqual(result["helpful_instruction_executed"], 1)


    def test_field_guard_can_be_bypassed_by_corrupted_source_label(self):
        scenario = dict(self.by_type["direct_injection"])
        scenario["attack_control_source"] = "user"
        result = evaluate_scenario(scenario, "field_provenance_guard")
        self.assertEqual(result["malicious_action_executed"], 1)

    def test_summary_metrics_are_bounded(self):
        summaries = summarise(evaluate_all(self.scenarios))
        self.assertEqual(len(summaries), 5)
        for row in summaries:
            for field in (
                "attack_success_rate",
                "primary_task_completion_rate",
                "false_block_rate",
                "helpful_instruction_acceptance_rate",
            ):
                self.assertGreaterEqual(row[field], 0.0)
                self.assertLessEqual(row[field], 1.0)


if __name__ == "__main__":
    unittest.main()
