
from math import *

import matplotlib.patches as patches
import matplotlib.pyplot as plt


def drawWH(wh, todo, moves):
    pos = convert_moves(init(wh), moves)
    ax = plt.gca()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, len(wh[0]))
    plt.ylim(-len(wh), 0)
    ax.add_artist(plt.Circle((pos[0][0], pos[0][1]), 0.25, color='g'))
    for p in range(1, len(pos)):
        ax.add_artist(plt.Circle((pos[p][0], pos[p][1]), 0.25, color='r'))

    for box in todo:
        ax.add_artist(patches.Rectangle((box[0] - 0.1, box[1] - 0.1), 0.2, 0.2))

    for row in range(len(wh)):
        for col in range(len(wh[0])):
            ch = wh[row][col]
            if ch == '#':
                p = (col, -row)
                ax.add_artist(patches.Rectangle((p[0], p[1] - 1), 1, 1, color='k'))

    for i in range(len(pos) - 1):
        pc = pos[i]
        qc = pos[i + 1]
        ux = qc[0] - pc[0]
        uy = qc[1] - pc[1]
        d = sqrt(ux * ux + uy * uy)
        if d > 1e-2:
            ux /= d
            uy /= d
            u = (uy * 0.25, -ux * 0.25)  # orthogonal unit vector times length
            p = (pc[0] - u[0], pc[1] - u[1])
            q = (qc[0] - u[0], qc[1] - u[1])
            for i in range(2):
                plt.plot([p[0], q[0]], [p[1], q[1]], 'k-')
                p = (pc[0] + u[0], pc[1] + u[1])
                q = (qc[0] + u[0], qc[1] + u[1])
    plt.show()


def convert_moves(init, moves):
    pos = []
    curr_pos = init
    for move in moves:
        new_pos = to_position(curr_pos, move)
        pos.append(new_pos[:2])
        curr_pos = new_pos
    return pos


def to_position(init, move):
    if 'move' in move:
        split = move.split()
        steer = float(split[1])
        d = float(split[2])
        heading = init[2] + steer
        return [init[0] + d * cos(heading), init[1] + d * sin(heading), heading]
    return init


def init(wh):
    for i in range(len(wh)):
        for j in range(len(wh[0])):
            if wh[i][j] == '@':
                return [j + 0.5, -i - 0.5, 0]
