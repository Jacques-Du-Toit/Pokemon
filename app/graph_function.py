import matplotlib.pyplot as plt


def damage_calc(level=50, power=80, attack=70, defense=70, divisor=50, constant=2, critical=1, stab=1.5, type=1, random=1):
    first_bracket = ((((2 * level) / 5) + 2) * power * (attack / defense)) / divisor
    second_bracket = first_bracket + constant
    return round(second_bracket * critical * stab * type * random, 2)


power_levels = [p for p in range(0, 110, 10)]
damage_stab_off = [damage_calc(level=p, stab=1) for p in power_levels]
damage_stab_on = [damage_calc(level=p) for p in power_levels]


# Plot the data
plt.plot(power_levels, damage_stab_off, label='Off')
plt.plot(power_levels, damage_stab_on, label='On')

# Annotate the points with their coordinates for 'stab off'
for p, d in zip(power_levels, damage_stab_off):
    plt.text(p, d, f"({p}, {d})", fontsize=8, ha='right', va='bottom', color='blue')

# Annotate the points with their coordinates for 'stab on'
for p, d in zip(power_levels, damage_stab_on):
    plt.text(p, d, f"({p}, {d})", fontsize=8, ha='left', va='top', color='green')

# Add legend and show plot
plt.legend()
plt.xlabel('Power Levels')
plt.ylabel('Damage')
plt.title('Damage vs Power Levels (Stab On vs Off)')
plt.grid(True)
plt.show()

