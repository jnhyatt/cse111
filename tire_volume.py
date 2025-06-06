# I exceeded requirements by prepending `volumes.txt` with a line containing the column names so the
# file can be read as a CSV if desired (also makes it easier to understand the data so it's not just
# loose numbers).

from datetime import date
import math
import os


def tire_volume(width, aspect_ratio, diameter):
    return (
        math.pi * (width**2) * aspect_ratio * (width * aspect_ratio + 2540 * diameter)
    ) / 1e10


# If we're creating the file for the first time, write the header line
if not os.path.exists("volumes.txt"):
    with open("volumes.txt", "w") as file:
        file.write("Date,Width (mm),Aspect Ratio,Diameter (in),Volume (L)\n")


# Prompt user for input, calculate/print volume
width = float(input("Enter tire width (mm): "))
aspect_ratio = float(input("Enter aspect ratio: "))
diameter = float(input("Enter wheel diameter (in): "))
volume = tire_volume(width, aspect_ratio, diameter)
print(f"Total volume: {volume:.2f}L")

# Append row to `volumes.txt`
with open("volumes.txt", "a") as file:
    file.write(f"{date.today()},{width},{aspect_ratio},{diameter},{volume:.2f}\n")
