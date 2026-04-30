"""
=============================================================
  Bayes Rule - Probabilistic Uncertainty Estimator
============================================================="""

from itertools import product as itertools_product
from fractions import Fraction
import math


# ─────────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────────

def read_joint_probability_table(variables: dict, table: dict) -> dict:
    """
    Reads and validates a joint probability table.

    Parameters
    ----------
    variables : dict  {var_name: [list of possible values]}
    table     : dict  {(val1, val2, ...): probability}

    Returns
    -------
    Validated table dict (raises ValueError if probs don't sum ≈ 1)
    """
    total = sum(table.values())
    if not math.isclose(total, 1.0, abs_tol=1e-6):
        raise ValueError(f"Joint probability table does not sum to 1.0 (got {total:.6f})")

    expected_keys = list(itertools_product(*variables.values()))
    for key in expected_keys:
        if key not in table:
            raise ValueError(f"Missing entry in table for combination: {key}")

    print("  [✔] Joint probability table loaded successfully.")
    print(f"      Variables : {list(variables.keys())}")
    print(f"      Entries   : {len(table)}, Total P = {total:.6f}\n")
    return table


def compute_marginal_probability(table: dict, variables: dict,
                                 target_var: str, target_val) -> float:
    """
    Computes P(target_var = target_val) by summing out all other variables.

    Parameters
    ----------
    table       : joint probability table  {(vals...): prob}
    variables   : dict {var_name: [values]}   — must preserve insertion order
    target_var  : variable name to compute marginal for
    target_val  : the specific value of target_var

    Returns
    -------
    float : marginal probability
    """
    var_names = list(variables.keys())
    idx = var_names.index(target_var)

    marginal = sum(
        prob
        for combo, prob in table.items()
        if combo[idx] == target_val
    )
    return marginal


def compute_conditional_probability(table: dict, variables: dict,
                                    target_var: str, target_val,
                                    given: dict) -> float:
    """
    Computes P(target_var = target_val | given).

    Parameters
    ----------
    table      : joint probability table
    variables  : dict {var_name: [values]}
    target_var : query variable name
    target_val : query variable value
    given      : dict of observed evidence {var_name: value}

    Returns
    -------
    float : conditional probability
    """
    var_names = list(variables.keys())

    def matches(combo, conditions):
        return all(combo[var_names.index(v)] == val for v, val in conditions.items())

    # P(target ∩ evidence)
    joint_conditions = {**given, target_var: target_val}
    numerator = sum(
        prob for combo, prob in table.items()
        if matches(combo, joint_conditions)
    )

    # P(evidence)
    denominator = sum(
        prob for combo, prob in table.items()
        if matches(combo, given)
    )

    if denominator == 0:
        raise ZeroDivisionError("Evidence has zero probability — check your table.")

    return numerator / denominator


def apply_bayes_rule(prior: float, likelihood: float,
                     marginal_likelihood: float) -> float:
    """
    Applies Bayes' Rule:  P(H|E) = P(E|H) * P(H) / P(E)

    Parameters
    ----------
    prior               : P(H)     — prior belief in hypothesis
    likelihood          : P(E|H)   — probability of evidence given hypothesis
    marginal_likelihood : P(E)     — total probability of evidence

    Returns
    -------
    float : posterior P(H|E)
    """
    if marginal_likelihood == 0:
        raise ZeroDivisionError("Marginal likelihood P(E) is zero.")
    return (likelihood * prior) / marginal_likelihood


# ─────────────────────────────────────────────
#  HELPER DISPLAY
# ─────────────────────────────────────────────

def print_section(title: str):
    width = 62
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)

def print_table(variables: dict, table: dict):
    """Pretty-print the joint probability table."""
    var_names = list(variables.keys())
    col_w = 14
    header = " | ".join(f"{v:^{col_w}}" for v in var_names) + " | " + f"{'P':^10}"
    print("  " + header)
    print("  " + "-" * len(header))
    for combo, prob in sorted(table.items(), key=lambda x: x[1], reverse=True):
        row = " | ".join(f"{str(c):^{col_w}}" for c in combo)
        print(f"  {row} | {prob:.6f}")
    print()


# ─────────────────────────────────────────────
#  QUESTION 1 — Simple Probability
#  Domain: Weather & Umbrella Carrying
# ─────────────────────────────────────────────

def question1_simple_probability():
    print_section("Q1 — Simple Probability : Weather & Umbrella")
    print("""
  Scenario:
    A city has 3 weather types: Sunny, Cloudy, Rainy.
    People carry an umbrella or not based on weather.
    Given a joint probability table, answer:
      (a) P(Rainy)               — marginal
      (b) P(Umbrella=Yes)        — marginal
      (c) P(Umbrella=Yes | Rainy)— conditional
    """)

    variables = {
        "Weather":   ["Sunny", "Cloudy", "Rainy"],
        "Umbrella":  ["Yes", "No"]
    }

    # Joint table P(Weather, Umbrella) — must sum to 1.0
    table = {
        ("Sunny",  "Yes"): 0.04,
        ("Sunny",  "No"):  0.36,
        ("Cloudy", "Yes"): 0.12,
        ("Cloudy", "No"):  0.18,
        ("Rainy",  "Yes"): 0.24,
        ("Rainy",  "No"):  0.06,
    }

    print("  Joint Probability Table:")
    table = read_joint_probability_table(variables, table)
    print_table(variables, table)

    # (a) Marginal P(Rainy)
    p_rainy = compute_marginal_probability(table, variables, "Weather", "Rainy")
    print(f"  (a)  P(Weather = Rainy)               = {p_rainy:.4f}")

    # (b) Marginal P(Umbrella = Yes)
    p_umbrella = compute_marginal_probability(table, variables, "Umbrella", "Yes")
    print(f"  (b)  P(Umbrella = Yes)                 = {p_umbrella:.4f}")

    # (c) Conditional P(Umbrella=Yes | Rainy)
    p_u_given_rainy = compute_conditional_probability(
        table, variables,
        target_var="Umbrella", target_val="Yes",
        given={"Weather": "Rainy"}
    )
    print(f"  (c)  P(Umbrella=Yes | Weather=Rainy)   = {p_u_given_rainy:.4f}")


# ─────────────────────────────────────────────
#  QUESTION 2 — Bayes Rule Problem
#  Domain: Medical Disease Diagnosis
# ─────────────────────────────────────────────

def question2_bayes_rule():
    print_section("Q2 — Bayes Rule : Medical Disease Diagnosis")
    print("""
  Scenario:
    A rare disease affects 1 % of the population.
    A diagnostic test has:
      • Sensitivity  P(Test+ | Disease)  = 0.95  (true-positive rate)
      • Specificity  P(Test- | No Dis.)  = 0.90  (true-negative rate)
      → False-positive rate P(Test+ | No Disease) = 0.10

    A patient tests POSITIVE.
    What is the probability the patient actually HAS the disease?
    → Compute P(Disease | Test+) using Bayes' Rule.
    """)

    # Known values
    P_disease      = 0.01          # Prior P(H)
    P_no_disease   = 1 - P_disease # P(¬H)
    P_pos_given_D  = 0.95          # Likelihood P(E|H)
    P_pos_given_nD = 0.10          # False-positive P(E|¬H)

    # Step 1: Total probability of a positive test P(E)
    P_positive = (P_pos_given_D  * P_disease +
                  P_pos_given_nD * P_no_disease)

    print("  ─── Step-by-Step Computation ───")
    print(f"  Prior            P(Disease)            = {P_disease}")
    print(f"  Likelihood       P(Test+ | Disease)    = {P_pos_given_D}")
    print(f"  False-Pos Rate   P(Test+ | No Disease) = {P_pos_given_nD}")
    print(f"  Marginal         P(Test+)              = "
          f"P(T+|D)·P(D) + P(T+|¬D)·P(¬D)")
    print(f"                                         = "
          f"{P_pos_given_D}×{P_disease} + {P_pos_given_nD}×{P_no_disease}")
    print(f"                                         = {P_positive:.4f}")

    # Step 2: Bayes' Rule
    P_disease_given_pos = apply_bayes_rule(
        prior               = P_disease,
        likelihood          = P_pos_given_D,
        marginal_likelihood = P_positive
    )

    print(f"\n  Bayes' Rule:  P(H|E) = P(E|H)·P(H) / P(E)")
    print(f"  P(Disease | Test+) = {P_pos_given_D}×{P_disease} / {P_positive:.4f}")
    print(f"                     = {P_disease_given_pos:.4f}  "
          f"({P_disease_given_pos*100:.2f} %)")

    # Also compute P(No Disease | Test+) as a sanity check
    P_no_disease_given_pos = apply_bayes_rule(
        prior               = P_no_disease,
        likelihood          = P_pos_given_nD,
        marginal_likelihood = P_positive
    )
    print(f"  P(No Disease | Test+) = {P_no_disease_given_pos:.4f}  "
          f"(sanity check — should sum to 1: "
          f"{P_disease_given_pos + P_no_disease_given_pos:.4f})")

# ─────────────────────────────────────────────
#  QUESTION 3 — Full Joint Distribution (Prior → Posterior)
#  Domain: Student Grade Prediction
# ─────────────────────────────────────────────

def question3_full_joint_distribution():
    print_section("Q3 — Full Joint Distribution : Smart Security System (A,B,C,D)")

    print("""
  Scenario:
    A smart home security system detects intrusions.

      A = Intruder (Yes/No)
      B = Motion Sensor (Yes/No)     depends on A
      C = Door Sensor   (Yes/No)     depends on A
      D = Alarm         (Yes/No)     depends on B and C

    Structure:
        A → B, C
        B, C → D

    Tasks:
      (a) Construct full joint P(A,B,C,D)
      (b) Compute marginal P(A,D)
      (c) Compute P(D|A)
    """)
    print("""
  Goal:
    Compute P(A, D) by expanding over B and C:

    P(A,D) =P(A,B,C,D)+ P(A,B,¬C,D)+ P(A,¬B,C,D)+ P(A,¬B,¬C,D)
    """)


    P_A = 0.75

    P_B_given_A = 0.2
    P_notB_given_A = 1 - P_B_given_A

    P_C_given_A = 0.7
    P_notC_given_A = 1 - P_C_given_A

    P_D_given = {
        ("B", "C"): 0.3,
        ("B", "¬C"): 0.25,
        ("¬B", "C"): 0.1,
        ("¬B", "¬C"): 0.35
    }
    print("\n  Probabilities:")
    print(f"    P(A) = {P_A}")
    print(f"    P(B | A) = {P_B_given_A}")
    print(f"    P(¬B | A) = {P_notB_given_A}")
    print(f"    P(C | A) = {P_C_given_A}")
    print(f"    P(¬C | A) = {P_notC_given_A:.4f}")

    print("\n    P(D | B, C):")
    print(f"      P(D | B, C)   = {P_D_given[('B','C')]}")
    print(f"      P(D | B, ¬C)  = {P_D_given[('B','¬C')]}")
    print(f"      P(D | ¬B, C)  = {P_D_given[('¬B','C')]}")
    print(f"      P(D | ¬B, ¬C) = {P_D_given[('¬B','¬C')]}")


    print("\n--- Step 1: Compute each joint term ---\n")

    term1 = P_A * P_notB_given_A * P_notC_given_A * P_D_given[("¬B", "¬C")]
    print(f"P(A, ¬B, ¬C, D) = {P_A} × {P_notB_given_A} × {P_notC_given_A:.4f} × 0.35 = {term1:.4f}")


    term2 = P_A * P_notB_given_A * P_C_given_A * P_D_given[("¬B", "C")]
    print(f"P(A, ¬B, C, D)  = {P_A} × {P_notB_given_A} × {P_C_given_A} × 0.1  = {term2:.4f}")

    term3 = P_A * P_B_given_A * P_notC_given_A * P_D_given[("B", "¬C")]
    print(f"P(A, B, ¬C, D)  = {P_A} × {P_B_given_A} × {P_notC_given_A:.4f} × 0.25 = {term3:.4f}")


    term4 = P_A * P_B_given_A * P_C_given_A * P_D_given[("B", "C")]
    print(f"P(A, B, C, D)   = {P_A} × {P_B_given_A} × {P_C_given_A} × 0.3  = {term4:.4f}")


    P_A_D = term1 + term2 + term3 + term4

    print("\n--- Step 2: Sum all terms ---")
    print(f"P(A,D) = {term1:.4f} + {term2:.4f} + {term3:.4f} + {term4:.4f}")
    print(f"       = {P_A_D:.4f}")


    print("\n--- Step 3: Compute P(D | A) ---")
    P_D_given_A = P_A_D / P_A
    print(f"P(D | A) = {P_A_D:.4f} / {P_A} = {P_D_given_A:.4f}")

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 62)
    print("    BAYES RULE — PROBABILISTIC UNCERTAINTY ESTIMATOR")
    print("=" * 62)

    question1_simple_probability()
    question2_bayes_rule()
    question3_full_joint_distribution()
