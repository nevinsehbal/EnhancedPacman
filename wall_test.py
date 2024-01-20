predefined_walls = [
    [0, 0, 6, 600],
    [0, 0, 600, 6],
    [0, 600, 606, 6],
    [600, 0, 6, 606],
    [300, 0, 6, 66],
    [60, 60, 186, 6],
    [360, 60, 186, 6],
    [60, 120, 66, 6],
    [60, 120, 6, 126],
    [180, 120, 246, 6],
    [300, 120, 6, 66],
    [480, 120, 66, 6],
    [540, 120, 6, 126],
    [120, 180, 126, 6],
    [120, 180, 6, 126],
    [360, 180, 126, 6],
    [480, 180, 6, 126],
    [180, 240, 6, 126],
    [180, 360, 246, 6],
    [420, 240, 6, 126],
    [240, 240, 42, 6],
    [324, 240, 42, 6],
    [240, 240, 6, 66],
    [240, 300, 126, 6],
    [360, 240, 6, 66],
    [0, 300, 66, 6],
    [540, 300, 66, 6],
    [60, 360, 66, 6],
    [60, 360, 6, 186],
    [480, 360, 66, 6],
    [540, 360, 6, 186],
    [120, 420, 366, 6],
    [120, 420, 6, 66],
    [480, 420, 6, 66],
    [180, 480, 246, 6],
    [300, 480, 6, 66],
    [120, 540, 126, 6],
    [360, 540, 126, 6]
]

# Separate y, x, height, and width values into four arrays
x_values = sorted(set(item[0] for item in predefined_walls))
y_values = sorted(set(item[1] for item in predefined_walls))
width_values = sorted(set(item[2] for item in predefined_walls))
height_values = sorted(set(item[3] for item in predefined_walls))

# Print the separated arrays
print("Y values:", y_values)
print("X values:", x_values)
print("Height values:", height_values)
print("Width values:", width_values)

