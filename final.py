import tkinter as tk
from tkinter import ttk
import numpy as np


# This is a list of constraints where each constraint tracks a shaft and coefficient. A pair of
# gears connected by a chain where gear A is on shaft A and has 10 teeth and gear B is on shaft B
# with 20 teeth would be represented as {type: "chain", a: {shaft: "A", teeth: 10}, b: {shaft: "B", teeth: 20}}.
# Planetary gears would be represented as {type: "planetary", sun: {shaft: "A", teeth: 10}, ring: {shaft: "B", teeth: 30}, carrier: {shaft: "C"}}.
# This is the upstream source of truth for the constraint matrix.
constraints = []
shafts = {"input": {}, "fixed": {}}


def create_ui(root):
    root.title("Transmission Simulator")

    ttk.Label(root, text="Shafts").grid(row=0, column=0)
    ttk.Label(root, text="Gears").grid(row=0, column=2)

    shaft_frame = ttk.Frame(root)
    shaft_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

    gear_frame = ttk.Frame(root)
    gear_frame.grid(row=1, column=2, sticky="ew")

    # Store references to the frame and root for updating
    root.shaft_frame = shaft_frame
    root.gear_frame = gear_frame
    root.update_shaft_list = lambda: update_shaft_list(root)
    root.update_gear_list = lambda: update_gear_list(root)

    update_shaft_list(root)
    update_gear_list(root)

    ttk.Label(root, text="Input Shaft Speed (RPM):").grid(row=0, column=4, sticky="e")
    root.input_speed_entry = ttk.Entry(root)
    root.input_speed_entry.grid(row=0, column=5, sticky="ew")

    ttk.Button(root, text="Run Simulation", command=lambda: run_simulation(root)).grid(
        row=1, column=4, columnspan=2
    )


def update_shaft_list(root):
    for widget in root.shaft_frame.winfo_children():
        widget.destroy()

    for i, shaft in enumerate(shafts.keys()):
        ttk.Label(root.shaft_frame, text=shaft).grid(row=i, column=0)
        if shaft != "fixed" and shaft != "input":
            ttk.Button(
                root.shaft_frame,
                text="🗑",
                command=lambda s=shaft: remove_shaft(s, root),
            ).grid(row=i, column=1)

    ttk.Button(
        root.shaft_frame, text="Add Shaft", command=lambda: add_shaft_dialog(root)
    ).grid(row=len(shafts), column=0, pady=10)


def update_gear_list(root):
    for widget in root.gear_frame.winfo_children():
        widget.destroy()

    for i, constraint in enumerate(constraints):
        if constraint["type"] == "chain":
            ttk.Label(
                root.gear_frame,
                text=f"Chain ({constraint['a']['shaft']} {constraint['a']['teeth']} -> {constraint['b']['shaft']} {constraint['b']['teeth']})",
            ).grid(row=i, column=0)
        elif constraint["type"] == "mesh":
            ttk.Label(
                root.gear_frame,
                text=f"Mesh ({constraint['a']['shaft']} {constraint['a']['teeth']} -> {constraint['b']['shaft']} {constraint['b']['teeth']})",
            ).grid(row=i, column=0)
        elif constraint["type"] == "planetary":
            ttk.Label(
                root.gear_frame,
                text=f"Planetary ({constraint['sun']['shaft']} {constraint['sun']['teeth']} -> {constraint['ring']['shaft']} {constraint['ring']['teeth']}, Carrier: {constraint['carrier']['shaft']})",
            ).grid(row=i, column=0)

        ttk.Button(
            root.gear_frame,
            text="🗑",
            command=lambda c=constraint: remove_constraint(c, root),
        ).grid(row=i, column=1)

    ttk.Button(
        root.gear_frame,
        text="Add Chained Gears",
        command=lambda: add_chain_dialog(root),
    ).grid(row=len(constraints), column=0, pady=10)
    ttk.Button(
        root.gear_frame,
        text="Add Mesh Gears",
        command=lambda: add_mesh_dialog(root),
    ).grid(row=len(constraints) + 1, column=0, pady=10)
    ttk.Button(
        root.gear_frame,
        text="Add Planetary Gears",
        command=lambda: add_planetary_dialog(root),
    ).grid(row=len(constraints) + 2, column=0, pady=10)


def remove_shaft(shaft_name, root):
    if shaft_name in shafts:
        shafts.pop(shaft_name)
        # also remove any constraints that reference this shaft
        global constraints
        constraints = [
            c
            for c in constraints
            if c["a"]["shaft"] != shaft_name and c["b"]["shaft"] != shaft_name
        ]
        root.update_shaft_list()
        root.update_gear_list()


def remove_constraint(constraint, root):
    if constraint in constraints:
        constraints.remove(constraint)
        root.update_gear_list()


def add_shaft_dialog(root):
    dialog = tk.Toplevel(root)
    dialog.title("Add Shaft")

    ttk.Label(dialog, text="Shaft Name:").grid(row=0, column=0)
    shaft_name_entry = ttk.Entry(dialog)
    shaft_name_entry.grid(row=0, column=1)

    def on_ok():
        shaft_name = shaft_name_entry.get()
        if shaft_name and shaft_name not in shafts:
            shafts[shaft_name] = {}
            print("Added Shaft:", shaft_name)
            root.update_shaft_list()
        dialog.destroy()

    ttk.Button(dialog, text="OK", command=on_ok).grid(row=1, column=0, pady=10)


def add_chain_dialog(root):
    dialog = tk.Toplevel(root)
    dialog.title("Add Chain Gear")

    ttk.Label(dialog, text="Gear A Teeth:").grid(row=0, column=0)
    gear_a_entry = ttk.Entry(dialog)
    gear_a_entry.grid(row=0, column=1)

    ttk.Label(dialog, text="Gear B Teeth:").grid(row=1, column=0)
    gear_b_entry = ttk.Entry(dialog)
    gear_b_entry.grid(row=1, column=1)

    ttk.Label(dialog, text="Shaft A:").grid(row=2, column=0)
    shaft_a_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    shaft_a_combobox.grid(row=2, column=1)

    ttk.Label(dialog, text="Shaft B:").grid(row=3, column=0)
    shaft_b_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    shaft_b_combobox.grid(row=3, column=1)

    def on_ok():
        gear_a_teeth = int(gear_a_entry.get())
        gear_b_teeth = int(gear_b_entry.get())
        if gear_a_teeth > 0 and gear_b_teeth > 0:
            shaft_a = shaft_a_combobox.get()
            shaft_b = shaft_b_combobox.get()
            if shaft_a and shaft_b and shaft_a != shaft_b:
                constraints.append(
                    {
                        "type": "chain",
                        "a": {"shaft": shaft_a, "teeth": gear_a_teeth},
                        "b": {"shaft": shaft_b, "teeth": gear_b_teeth},
                    }
                )
                root.update_gear_list()
        dialog.destroy()

    ttk.Button(dialog, text="OK", command=on_ok).grid(row=4, column=0, pady=10)


def add_mesh_dialog(root):
    dialog = tk.Toplevel(root)
    dialog.title("Add Mesh Gear")

    ttk.Label(dialog, text="Gear A Teeth:").grid(row=0, column=0)
    gear_a_entry = ttk.Entry(dialog)
    gear_a_entry.grid(row=0, column=1)

    ttk.Label(dialog, text="Gear B Teeth:").grid(row=1, column=0)
    gear_b_entry = ttk.Entry(dialog)
    gear_b_entry.grid(row=1, column=1)

    ttk.Label(dialog, text="Shaft A:").grid(row=2, column=0)
    shaft_a_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    shaft_a_combobox.grid(row=2, column=1)

    ttk.Label(dialog, text="Shaft B:").grid(row=3, column=0)
    shaft_b_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    shaft_b_combobox.grid(row=3, column=1)

    def on_ok():
        gear_a_teeth = int(gear_a_entry.get())
        gear_b_teeth = int(gear_b_entry.get())
        if gear_a_teeth > 0 and gear_b_teeth > 0:
            shaft_a = shaft_a_combobox.get()
            shaft_b = shaft_b_combobox.get()
            if shaft_a and shaft_b and shaft_a != shaft_b:
                constraints.append(
                    {
                        "type": "mesh",
                        "a": {"shaft": shaft_a, "teeth": gear_a_teeth},
                        "b": {"shaft": shaft_b, "teeth": gear_b_teeth},
                    }
                )
                root.update_gear_list()
        dialog.destroy()

    ttk.Button(dialog, text="OK", command=on_ok).grid(row=4, column=0, pady=10)


def add_planetary_dialog(root):
    dialog = tk.Toplevel(root)
    dialog.title("Add Planetary Gear")

    ttk.Label(dialog, text="Sun Gear Teeth:").grid(row=0, column=0)
    sun_teeth_entry = ttk.Entry(dialog)
    sun_teeth_entry.grid(row=0, column=1)

    ttk.Label(dialog, text="Ring Gear Teeth:").grid(row=1, column=0)
    ring_teeth_entry = ttk.Entry(dialog)
    ring_teeth_entry.grid(row=1, column=1)

    ttk.Label(dialog, text="Sun Shaft:").grid(row=2, column=0)
    carrier_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    carrier_combobox.grid(row=2, column=1)

    ttk.Label(dialog, text="Ring Shaft:").grid(row=3, column=0)
    ring_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    ring_combobox.grid(row=3, column=1)

    ttk.Label(dialog, text="Carrier Shaft:").grid(row=4, column=0)
    carrier_shaft_combobox = ttk.Combobox(dialog, values=list(shafts.keys()))
    carrier_shaft_combobox.grid(row=4, column=1)

    def on_ok():
        sun_teeth = int(sun_teeth_entry.get())
        ring_teeth = int(ring_teeth_entry.get())
        if sun_teeth > 0 and ring_teeth > 0:
            sun_shaft = carrier_combobox.get()
            ring_shaft = ring_combobox.get()
            carrier_shaft = carrier_shaft_combobox.get()
            if (
                sun_shaft
                and ring_shaft
                and carrier_shaft
                and sun_shaft != ring_shaft
                and sun_shaft != carrier_shaft
                and ring_shaft != carrier_shaft
            ):
                constraints.append(
                    {
                        "type": "planetary",
                        "sun": {"shaft": sun_shaft, "teeth": sun_teeth},
                        "ring": {"shaft": ring_shaft, "teeth": ring_teeth},
                        "carrier": {"shaft": carrier_shaft},
                    }
                )
                root.update_gear_list()
        dialog.destroy()

    ttk.Button(dialog, text="OK", command=on_ok).grid(row=5, column=0, pady=10)


def run_simulation(root):
    input_speed = float(root.input_speed_entry.get())
    matrix, shaft_mapping = matrix_from_constraints(shafts, constraints)
    x = np.zeros(len(shaft_mapping), dtype=float)
    x[-1] = input_speed
    solution = np.dot(np.linalg.inv(matrix), x)
    print(f"{solution}, {shaft_mapping}")
    result_dialog = tk.Toplevel(root)
    result_dialog.title("Simulation Results")
    for shaft, speed in zip(shaft_mapping.keys(), solution):
        ttk.Label(result_dialog, text=f"{shaft}: {speed} RPM").pack()
    ttk.Button(result_dialog, text="OK", command=result_dialog.destroy).pack()


def chain_constraint_vector(a, b, shaft_mapping):
    # a and b are objects {"shaft": "input", "teeth": 10}
    # shaft_mapping is a dictionary mapping shaft names to indices
    vector = np.zeros(len(shaft_mapping), dtype=float)
    # Since w_a/w_b = t_b/t_a, we can write the constraint as:
    # w_a * t_a - w_b * t_b = 0
    vector[shaft_mapping[a["shaft"]]] = a["teeth"]
    vector[shaft_mapping[b["shaft"]]] = -b["teeth"]
    return vector


def mesh_constraint_vector(a, b, shaft_mapping):
    # a and b are objects {"shaft": "input", "teeth": 10}
    # shaft_mapping is a dictionary mapping shaft names to indices
    vector = np.zeros(len(shaft_mapping), dtype=float)
    # Since w_a/w_b = -t_b/t_a, we can write the constraint as:
    # w_a * t_a + w_b * t_b = 0
    vector[shaft_mapping[a["shaft"]]] = a["teeth"]
    vector[shaft_mapping[b["shaft"]]] = b["teeth"]
    return vector


def planetary_constraint_vector(sun, ring, carrier, shaft_mapping):
    # sun and ring are objects {"shaft": "input", "teeth": 10}
    # carrier is an object {"shaft": "output"}
    # planet teeth count is implicitly defined by the sun and ring teeth counts: T_p = (T_r - T_s) / 2
    # shaft_mapping is a dictionary mapping shaft names to indices
    vector = np.zeros(len(shaft_mapping), dtype=float)
    # For planetary gears, the equation of motion is T_s * w_s + T_r * w_r = (T_s + T_r) * w_c
    # The constraint can be written as:
    # T_s * w_s + T_r * w_r - (T_s + T_r) * w_c = 0
    vector[shaft_mapping[sun["shaft"]]] = sun["teeth"]
    vector[shaft_mapping[ring["shaft"]]] = ring["teeth"]
    vector[shaft_mapping[carrier["shaft"]]] = -(sun["teeth"] + ring["teeth"])
    return vector


def constraint_vector(constraint, shaft_mapping):
    if constraint["type"] == "chain":
        return chain_constraint_vector(constraint["a"], constraint["b"], shaft_mapping)
    elif constraint["type"] == "mesh":
        return mesh_constraint_vector(constraint["a"], constraint["b"], shaft_mapping)
    elif constraint["type"] == "planetary":
        return planetary_constraint_vector(
            constraint["sun"],
            constraint["ring"],
            constraint["carrier"],
            shaft_mapping,
        )
    else:
        raise ValueError(f"Unknown constraint type: {constraint['type']}")


def matrix_from_constraints(shafts, constraints):
    # Each column represents a shaft, so let's create a mapping from shaft names to indices so
    # we can build each constraint vector.
    shaft_mapping = {name: idx for idx, name in enumerate(shafts.keys())}
    # For each constraint, append the constraint vector to the matrix.
    matrix = np.zeros((len(constraints) + 2, len(shaft_mapping)), dtype=float)
    for i, constraint in enumerate(constraints):
        matrix[i] = constraint_vector(constraint, shaft_mapping)
    matrix[-2, shaft_mapping["fixed"]] = 1  # fixed shaft
    matrix[-1, shaft_mapping["input"]] = 1  # input shaft

    return matrix, shaft_mapping


if __name__ == "__main__":
    root = tk.Tk()
    create_ui(root)
    root.mainloop()
