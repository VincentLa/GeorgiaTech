#Code from Asdaq Samir, Fall 2017 student
#

from math import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os

PI = pi


def drawWH(wh, boxes, pos):
    f = plt.figure()
    ax = plt.gca()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, len(wh[0]))
    plt.ylim(-len(wh), 0)
    print pos
    ax.add_artist(plt.Circle((pos[0][0], pos[0][1]), 0.25, color='g'))
    for p in range(1, len(pos)):
        ax.add_artist(plt.Circle((pos[p][0], pos[p][1]), 0.25, color='r'))

    for box in boxes:
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
        if (d > 1e-2):
            ux /= d
            uy /= d
            u = (uy * 0.25, -ux * 0.25)  # orthogonal unit vector times length
            p = (pc[0] - u[0], pc[1] - u[1])
            q = (qc[0] - u[0], qc[1] - u[1])
            for i in range(2):
                plt.plot([p[0], q[0]], [p[1], q[1]], 'k-')
                p = (pc[0] + u[0], pc[1] + u[1])
                q = (qc[0] + u[0], qc[1] + u[1])
    plt.savefig('foo.png', bbox_inches='tight')


def drawWH2(tc, wh, todo, moves):
    inital_pos = init(wh)
    curr_pos = inital_pos
    last_pos = curr_pos

    pos = convert_moves(init(wh), moves)
    ax = plt.gca()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, len(wh[0]))
    plt.ylim(-len(wh), 0)

    for i in range(len(moves) - 1):

        # calc new position
        new_pos = to_position(curr_pos, moves[i])
        next_pos = to_position(new_pos, moves[i+1])
        curr_pos = new_pos

        this_move_type = move_type(moves[i])
        if this_move_type != 'move':
            if this_move_type == 'lift':
                # assume you can do the lift.
                todo = todo[1:]

        ax = plt.gca()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.xlim(0, len(wh[0]))
        plt.ylim(-len(wh), 0)
        ax.add_artist(plt.Circle((inital_pos[0], inital_pos[1]), 0.5, color='#aaccaa'))
        ax.add_artist(plt.Circle((inital_pos[0], inital_pos[1]), 0.25, color='g'))

        for row in range(len(wh)):
            for col in range(len(wh[0])):
                ch = wh[row][col]
                if ch == '#':
                    p = (col, -row)
                    ax.add_artist(patches.Rectangle((p[0], p[1] - 1), 1, 1, color='k'))

        for box in todo:
            ax.add_artist(patches.Rectangle((box[0] - 0.1, box[1] - 0.1), 0.2, 0.2))

        if i > 0:
            ax.add_artist(plt.Circle((last_pos[0], last_pos[1]), 0.25, color='y'))

            pc = last_pos
            qc = new_pos
            ux = qc[0] - pc[0]
            uy = qc[1] - pc[1]
            d = sqrt(ux * ux + uy * uy)
            if d > 1e-2:
                ux /= d
                uy /= d
                u = (uy * 0.25, -ux * 0.25)  # orthogonal unit vector times length
                p = (pc[0] - u[0], pc[1] - u[1])
                q = (qc[0] - u[0], qc[1] - u[1])
                for idx in range(2):
                    plt.plot([p[0], q[0]], [p[1], q[1]], 'k-')
                    p = (pc[0] + u[0], pc[1] + u[1])
                    q = (qc[0] + u[0], qc[1] + u[1])


        ax.add_artist(plt.Circle((new_pos[0], new_pos[1]), 0.25, color='r'))
        ax.text(new_pos[0], new_pos[1], str(i+1), style='italic', horizontalalignment='center')

        last_pos = curr_pos

        plt.savefig('visual/vis{1}_{0}.png'.format(i, str(tc)), bbox_inches='tight')
        plt.clf()

    os.system("ffmpeg -r 1 -i visual/vis" + str(tc) + "_%01d.png -vcodec mpeg4 -y vis" + str(tc) + ".mp4")


def move_type(move):
    if 'move' in move:
        return 'move'
    elif 'lift' in move:
        return 'lift'
    elif 'drop' in move:
        return 'drop'

def convert_moves(init, moves):
    pos = [init]
    curr_pos = init
    for move in moves:
        if 'move' in move:
            new_pos = to_position(curr_pos, move)
            pos.append(new_pos[:2])
            curr_pos = new_pos
    return pos


def to_position(curr_pos, move):
    if 'move' in move:
        split = move.split()
        steer = float(split[1])
        d = float(split[2])
        heading = curr_pos[2] + steer
        return [curr_pos[0] + d * cos(heading), curr_pos[1] + d * sin(heading), heading]
    return curr_pos


def init(wh):
    for i in range(len(wh)):
        for j in range(len(wh[0])):
            if wh[i][j] == '@':
                return [j + 0.5, -i - 0.5, 0]


# How to call it:
#
#import drawMoves
#drawMoves.drawWH2(params['test_case'], params['warehouse'], params['todo'], the_plan)


#if it errors with "cannot find ffmpeg' you may need to install it.  If it is installed, you may need to use the full path to it.
#
#My full path was
#/usr/local/bin/ffmpeg
#I'm using a mac, but it should work fine on windows also.
#
#NOTE: You may need to create a folder called "visual" before running.
