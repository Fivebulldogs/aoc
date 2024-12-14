from dataclasses import dataclass, field


@dataclass
class Button:
    name: str = ""
    x_move: int = 0
    y_move: int = 0


@dataclass
class Machine:
    buttons: list[Button] = field(default_factory=list)
    x_prize: int = 0
    y_prize: int = 0


def read_lines(filename):
    machines = []
    with open(filename) as f:
        while True:
            machine = Machine()
            for button in ["A", "B"]:
                line = f.readline()
                split_line = line.split(" ")
                x_move = int(split_line[2].split("+")[1][:-1])
                y_move = int(split_line[3].split("+")[1][:-1])
                machine.buttons.append(Button(button, x_move, y_move))

            line = f.readline()
            split_line = line.split("=")
            machine.x_prize = int(split_line[1].split(",")[0]) + 10000000000000
            machine.y_prize = int(split_line[2].strip()) + 10000000000000
            machines.append(machine)
            if not f.readline():
                break
    return machines


machines: list[Machine] = read_lines("input")

tokens = 0
for m in machines:
    xa = m.buttons[0].x_move
    xb = m.buttons[1].x_move
    ya = m.buttons[0].y_move
    yb = m.buttons[1].y_move
    xp = m.x_prize
    yp = m.y_prize

    j_denom = xp * ya - xa * yp
    j_nom = xb * ya - xa * yb
    j = j_denom / j_nom

    i = (xp - j * xb) / xa

    if i == round(i) and j == round(j):
        tokens += i * 3 + j
print("tokens", int(tokens))
