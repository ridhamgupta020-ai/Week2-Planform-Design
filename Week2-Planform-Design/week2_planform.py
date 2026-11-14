
import math
import csv
import matplotlib.pyplot as plt # type: ignore
from matplotlib.patches import Polygon # type: ignore

# ==================================================
# WEEK 2: WING PLANFORM DESIGN
# Conceptual Fixed-Wing UAV
# ==================================================

# 1. DESIGN INPUTS (Week 1 assumptions)

MASS = 12.0
GRAVITY = 9.81

WING_AREA = 1.20
WING_SPAN = 3.00
TAPER_RATIO = 0.60

CRUISE_SPEED = 20.0
LOW_SPEED = 12.0

AIR_DENSITY = 1.225
DYNAMIC_VISCOSITY = 1.789e-5

BASELINE_AEROFOIL = "NACA 2412"


# 2. INPUT VALIDATION

def validate_inputs():

    if MASS <= 0:
        raise ValueError("Mass must be positive.")

    if WING_AREA <= 0 or WING_SPAN <= 0:
        raise ValueError("Wing area and span must be positive.")

    if not 0 < TAPER_RATIO <= 1:
        raise ValueError("Taper ratio must be between 0 and 1.")

    if CRUISE_SPEED <= 0 or LOW_SPEED <= 0:
        raise ValueError("Speed must be positive.")

    if AIR_DENSITY <= 0 or DYNAMIC_VISCOSITY <= 0:
        raise ValueError("Air properties must be positive.")


# 3. AIRCRAFT WEIGHT

def calculate_weight():

    return MASS * GRAVITY


# 4. ASPECT RATIO

def calculate_aspect_ratio():

    return WING_SPAN ** 2 / WING_AREA


# 5. WING GEOMETRY

def calculate_chords():

    root_chord = (
        2 * WING_AREA /
        (WING_SPAN * (1 + TAPER_RATIO))
    )

    tip_chord = root_chord * TAPER_RATIO

    return root_chord, tip_chord


# 6. MEAN AERODYNAMIC CHORD

def calculate_mac(root_chord):

    mac = (
        (2 / 3) * root_chord *
        (1 + TAPER_RATIO + TAPER_RATIO ** 2) /
        (1 + TAPER_RATIO)
    )

    return mac


# 7. MAC SPANWISE POSITION

def calculate_mac_position():

    position = (
        WING_SPAN / 6 *
        (1 + 2 * TAPER_RATIO) /
        (1 + TAPER_RATIO)
    )

    return position


# 8. WING LOADING

def calculate_wing_loading():

    return calculate_weight() / WING_AREA


# 9. DYNAMIC PRESSURE

def calculate_dynamic_pressure(speed):

    return 0.5 * AIR_DENSITY * speed ** 2


# 10. REQUIRED LIFT COEFFICIENT

def calculate_lift_coefficient(speed):

    weight = calculate_weight()

    pressure = calculate_dynamic_pressure(speed)

    return weight / (pressure * WING_AREA)


# 11. REYNOLDS NUMBER

def calculate_reynolds_number(speed, chord):

    return (
        AIR_DENSITY * speed * chord /
        DYNAMIC_VISCOSITY
    )


# 12. PLANFORM DRAWING

def create_planform_drawing(root_chord, tip_chord):

    tip_le = (root_chord - tip_chord) / 2

    half_span = WING_SPAN / 2

    points = [
        (0, 0),
        (root_chord, 0),
        (tip_le + tip_chord, half_span),
        (tip_le, half_span),
        (tip_le + tip_chord, -half_span),
        (tip_le, -half_span)
    ]

    fig, ax = plt.subplots(figsize=(9, 5))

    wing = Polygon(
        points,
        closed=True,
        fill=False,
        edgecolor="blue",
        linewidth=2
    )

    ax.add_patch(wing)

    ax.set_title("Trapezoidal Wing Planform")

    ax.set_xlabel("Chordwise Direction (m)")
    ax.set_ylabel("Spanwise Direction (m)")

    ax.text(
        root_chord / 2,
        -half_span - 0.15,
        f"Root Chord = {root_chord:.3f} m",
        ha="center"
    )

    ax.text(
        tip_le + tip_chord / 2,
        half_span + 0.15,
        f"Tip Chord = {tip_chord:.3f} m",
        ha="center"
    )

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)

    plt.tight_layout()

    plt.savefig(
        "week2_planform_drawing.png",
        dpi=200
    )

    plt.close()

    print("\nPlanform drawing saved successfully.")


# 13. AEROFOIL COMPARISON

def compare_aerofoils():

    aerofoils = [
        ["NACA 0012", "Symmetrical", "12%"],
        ["NACA 2412", "Cambered", "12%"],
        ["NACA 4412", "More Cambered", "12%"]
    ]

    print("\nAEROFOIL COMPARISON")
    print("--------------------------------")

    for foil in aerofoils:

        print(
            "Name:", foil[0],
            "| Type:", foil[1],
            "| Thickness:", foil[2]
        )


# 14. SAVE RESULTS TO CSV

def export_results(results):

    with open(
        "week2_planform_results.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Parameter",
            "Value",
            "Unit"
        ])

        for name, value, unit in results:

            writer.writerow([
                name,
                round(value, 4),
                unit
            ])

    print("\nCSV report generated successfully.")


# 15. MAIN FUNCTION

def main():

    try:

        validate_inputs()

        weight = calculate_weight()

        aspect_ratio = calculate_aspect_ratio()

        root_chord, tip_chord = calculate_chords()

        mac = calculate_mac(root_chord)

        mac_position = calculate_mac_position()

        wing_loading = calculate_wing_loading()

        q_cruise = calculate_dynamic_pressure(CRUISE_SPEED)

        cruise_cl = calculate_lift_coefficient(CRUISE_SPEED)

        low_speed_cl = calculate_lift_coefficient(LOW_SPEED)

        reynolds = calculate_reynolds_number(
            CRUISE_SPEED,
            mac
        )

        print("\n================================")
        print(" WEEK 2 WING DESIGN REPORT")
        print("================================")

        print("\nAIRCRAFT DATA")

        print("Mass:", MASS, "kg")
        print("Wing Area:", WING_AREA, "m2")
        print("Wing Span:", WING_SPAN, "m")
        print("Taper Ratio:", TAPER_RATIO)

        print("\nWING GEOMETRY")

        print("Weight:", round(weight, 2), "N")

        print("Aspect Ratio:", round(aspect_ratio, 2))

        print("Root Chord:", round(root_chord, 3), "m")

        print("Tip Chord:", round(tip_chord, 3), "m")

        print("Mean Aerodynamic Chord:", round(mac, 4), "m")

        print("MAC Position:", round(mac_position, 4), "m")

        print("Wing Loading:", round(wing_loading, 2), "N/m2")

        print("\nAERODYNAMIC RESULTS")

        print("Cruise Dynamic Pressure:", round(q_cruise, 2), "Pa")

        print("Cruise Required CL:", round(cruise_cl, 3))

        print("Low Speed Required CL:", round(low_speed_cl, 3))

        print("Reynolds Number:", round(reynolds))

        print("\nSelected Aerofoil:", BASELINE_AEROFOIL)

        compare_aerofoils()

        results = [
            ["Weight", weight, "N"],
            ["Aspect Ratio", aspect_ratio, "-"],
            ["Root Chord", root_chord, "m"],
            ["Tip Chord", tip_chord, "m"],
            ["Mean Aerodynamic Chord", mac, "m"],
            ["MAC Position", mac_position, "m"],
            ["Wing Loading", wing_loading, "N/m2"],
            ["Dynamic Pressure", q_cruise, "Pa"],
            ["Cruise Required CL", cruise_cl, "-"],
            ["Low Speed Required CL", low_speed_cl, "-"],
            ["Reynolds Number", reynolds, "-"]
        ]

        export_results(results)

        create_planform_drawing(
            root_chord,
            tip_chord
        )

        print("\nAll calculations completed successfully.")

    except ValueError as error:

        print("Input Error:", error)


if __name__ == "__main__":

    main()
