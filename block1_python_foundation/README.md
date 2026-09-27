# Block 1 — Python Foundation for RF Validation

## Objective

This block establishes the Python foundation for an RF test and
validation automation framework.

The concepts are learned through a realistic 77 GHz automotive
radar TX validation example rather than isolated programming exercises.

---

## Engineering Problem

The objective is to validate radar TX performance under defined
operating conditions.

The test monitors:

- TX output power
- DUT temperature
- Supply voltage
- TX current
- RF spur level

Each measurement is compared against its engineering requirement.

> Note: The numerical limits used in this project are illustrative
> training values and are not claimed automotive product or
> regulatory specifications.

---

## Requirements

| Parameter | Requirement |
|---|---|
| TX Power | >= 18.0 dBm |
| Temperature | 23–27 °C |
| Supply Voltage | 11.8–12.2 V |
| TX Current | <= 1.2 A |
| Spur | <= -45 dBc |

---

## Python Concepts

### Variables and Data Types

The program uses:

- `float` for RF measurements
- `string` for timestamps
- `boolean` for validation states

### Dictionaries

Engineering measurements and requirements are represented as
structured dictionaries.

Example:

```python
measurement = {
    "power_dbm": 17.94,
    "temperature_c": 26.8,
    "voltage_v": 11.99,
    "current_a": 0.91,
    "spur_dbc": -51.2
}