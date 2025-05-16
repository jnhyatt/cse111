import math

cans = [
    {"name": "#1 Picnic", "radius": 6.83, "height": 10.16},
    {"name": "#1 Tall", "radius": 7.78, "height": 11.91},
    {"name": "#2", "radius": 8.73, "height": 11.59},
    {"name": "#2.5", "radius": 10.32, "height": 11.91},
    {"name": "#3 Cylinder", "radius": 10.79, "height": 17.78},
    {"name": "#5", "radius": 13.02, "height": 14.29},
    {"name": "#6Z", "radius": 5.40, "height": 8.89},
    {"name": "#8Z short", "radius": 6.83, "height": 7.62},
    {"name": "#10", "radius": 15.72, "height": 17.78},
    {"name": "#211", "radius": 6.83, "height": 12.38},
    {"name": "#300", "radius": 7.62, "height": 11.27},
    {"name": "#303", "radius": 8.10, "height": 11.11},
]


def cylinder_volume(radius, height):
    return math.pi * radius**2 * height


def cylinder_surface_area(radius, height):
    return 2 * math.pi * radius * (radius + height)


def cylinder_efficiency(radius, height):
    return cylinder_volume(radius, height) / cylinder_surface_area(radius, height)


def main():
    cans_with_efficiency = [
        (can, cylinder_efficiency(can["radius"], can["height"])) for can in cans
    ]
    cans_with_efficiency.sort(key=lambda x: x[1], reverse=True)
    print(f"{'Can':<15} {'Efficiency':<15}")
    print("-" * 31)
    for can, efficiency in cans_with_efficiency:
        print(f"{can['name']:<15} {efficiency:<15.2f}")


if __name__ == "__main__":
    main()
