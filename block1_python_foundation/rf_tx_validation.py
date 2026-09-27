# ============================================================
# 77 GHz Automotive Radar RF Validation
# Block 1 - Python Foundation
# ============================================================

# ------------------------------------------------------------
# 1. TEST REQUIREMENTS
# ------------------------------------------------------------

requirements = {
    "power_dbm": {
        "type": "minimum",
        "limit": 18.0
    },

    "temperature_c": {
        "type": "range",
        "min": 23.0,
        "max": 27.0
    },

    "voltage_v": {
        "type": "range",
        "min": 11.8,
        "max": 12.2
    },

    "current_a": {
        "type": "maximum",
        "limit": 1.2
    },

    "spur_dbc": {
        "type": "maximum",
        "limit": -45.0
    }
}


# ------------------------------------------------------------
# 2. MEASUREMENT DATA
# ------------------------------------------------------------

measurement = {
    "timestamp": "10:04",

    "power_dbm": 17.94,

    "temperature_c": 26.8,

    "voltage_v": 11.99,

    "current_a": 0.91,

    "spur_dbc": -51.2
}


# ------------------------------------------------------------
# 3. VALIDATION FUNCTION
# ------------------------------------------------------------

def validate_parameter(value, requirement):

    requirement_type = requirement["type"]

    # --------------------------------------------------------
    # Minimum requirement
    # Example: Power >= 18.0 dBm
    # --------------------------------------------------------

    if requirement_type == "minimum":

        limit = requirement["limit"]

        margin = value - limit

        passed = value >= limit


    # --------------------------------------------------------
    # Maximum requirement
    # Example: Current <= 1.2 A
    # --------------------------------------------------------

    elif requirement_type == "maximum":

        limit = requirement["limit"]

        margin = limit - value

        passed = value <= limit


    # --------------------------------------------------------
    # Range requirement
    # Example: Temperature = 23 to 27 °C
    # --------------------------------------------------------

    elif requirement_type == "range":

        minimum = requirement["min"]

        maximum = requirement["max"]

        passed = minimum <= value <= maximum

        lower_margin = value - minimum

        upper_margin = maximum - value

        # Distance to nearest boundary
        margin = min(lower_margin, upper_margin)


    # --------------------------------------------------------
    # Unknown requirement type
    # --------------------------------------------------------

    else:

        return {
            "status": "ERROR",
            "measured": value,
            "margin": None
        }


    # --------------------------------------------------------
    # Determine PASS / FAIL
    # --------------------------------------------------------

    if passed:

        status = "PASS"

    else:

        status = "FAIL"


    # --------------------------------------------------------
    # Return validation result
    # --------------------------------------------------------

    return {
        "status": status,
        "measured": value,
        "margin": margin
    }


# ------------------------------------------------------------
# 4. VALIDATE ALL PARAMETERS
# ------------------------------------------------------------

results = {}


for parameter in requirements:

    # Get measured value
    value = measurement[parameter]

    # Get corresponding requirement
    requirement = requirements[parameter]

    # Validate
    result = validate_parameter(
        value,
        requirement
    )

    # Store result
    results[parameter] = result


# ------------------------------------------------------------
# 5. DISPLAY INDIVIDUAL RESULTS
# ------------------------------------------------------------

print()
print("=" * 60)
print("       77 GHz RADAR RF TX VALIDATION")
print("=" * 60)

print()
print("Test timestamp:", measurement["timestamp"])

print()
print("-" * 60)
print("PARAMETER RESULTS")
print("-" * 60)


for parameter, result in results.items():

    print(
        f"{parameter:15}"
        f" | Measured: {result['measured']:8}"
        f" | Margin: {result['margin']:7.2f}"
        f" | {result['status']}"
    )


# ------------------------------------------------------------
# 6. OVERALL TEST RESULT
# ------------------------------------------------------------

all_passed = all(
    result["status"] == "PASS"
    for result in results.values()
)


print()
print("-" * 60)


if all_passed:

    print("Overall Test: PASS")

else:

    print("Overall Test: FAIL")


# ------------------------------------------------------------
# 7. FAILURE SUMMARY
# ------------------------------------------------------------

failed_parameters = []

for parameter, result in results.items():

    if result["status"] == "FAIL":

        failed_parameters.append(parameter)


print()
print("-" * 60)
print("FAILURE SUMMARY")
print("-" * 60)


if failed_parameters:

    for parameter in failed_parameters:

        print(
            f"FAIL: {parameter}"
        )

else:

    print("No requirement failures.")


print()
print("=" * 60)
print("Test execution completed.")
print("=" * 60)