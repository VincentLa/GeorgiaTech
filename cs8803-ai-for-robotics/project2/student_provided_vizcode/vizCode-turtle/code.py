

import numpy as np
import robot
import turtle

def centered(pt):
    return (pt[0] + .50, pt[1] + .50)

def drawwarehouse(warehouse,robot):
    xlen = len(warehouse)
    ylen = len(warehouse[0])
    window = turtle.Screen()

    PIXELS = 100

    xscreensize = PIXELS * xlen
    yscreensize = PIXELS * ylen
    window.setup(yscreensize,xscreensize)
    # xscale = screensize /(xlen * 20.8333333)
    # yscale = screensize / (ylen * 20.8333333)

    scale = (PIXELS) / (20.8333333) #that's just how it works out


    window.bgcolor('white')
    window.setworldcoordinates(0,xlen,ylen,0)
    pen = turtle.Turtle()
    pen.color('green')
    pen.speed(0)
    pen.shapesize(.5, .5, 2)
    pen.penup()

    #draw grid
    for x in range(xlen):
        pen.goto(0,x)
        pen.pendown()
        pen.goto(ylen, x)
        pen.penup()

    for y in range(ylen):
        pen.goto(y, 0)
        pen.pendown()
        pen.goto(y, xlen)
        pen.penup()
    #draw objects
    for x in range(xlen):
        for y in range(ylen):
            spot = warehouse[x][y]
            pt = (y,x)
            if spot == '.': continue
            if spot == '#':
                turtlewall(turtle,pt,scale)
            elif spot == '@':
                turtledropzone(turtle,pt,scale)
            else:
                turtlebox(turtle,pt,scale)
    #draw robot
    bot = turtlerobot(turtle,robot,scale)
    return bot



def turtlerobot(turtle,robot,scale):

    bot = turtle.Turtle()
    bot.speed(0)
    bot.color('blue')
    bot.shape('circle')
    bot.penup()
    bot.shapesize(scale*.5, scale*.5)
    bot.goto((robot.x,robot.y))
    bot.pendown()
    bot.pensize(scale*9)

    return bot

def turtledropzone(turtle,pt,scale):

    dz = turtle.Turtle()
    dz.speed(0)
    dz.color('green')
    dz.shape('square')
    dz.penup()
    dz.shapesize(scale, scale)
    dz.goto(centered(pt))
    dz.stamp()


def turtlebox(turtle,pt,scale):

    box = turtle.Turtle()
    box.speed(0)
    box.color('blue')
    box.shape('square')
    box.penup()
    box.shapesize(scale*.2,scale*.2)
    box.goto(centered(pt))
    box.stamp()

def turtlewall(turtle,pt,scale):

    wall = turtle.Turtle()
    wall.speed(0)
    wall.color('red')
    wall.shape('square')
    wall.penup()
    wall.shapesize(scale,scale)
    wall.goto(centered(pt))
    wall.stamp()
