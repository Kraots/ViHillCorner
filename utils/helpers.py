import discord
import asyncio
import time
import random
import datetime

def time_phaser(seconds):
    output = ""
    print(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    mo, d = divmod(d, 30)
    if mo > 0:
        output = output + str(int(round(m, 0))) + " Months "
    if d > 0:
        output = output + str(int(round(d, 0))) + " Days "
    if h > 0:
        output = output + str(int(round(h, 0))) + " Hours "
    if m > 0:
        output = output + str(int(round(m, 0))) + " Minutes "
    if s > 0:
        output = output + str(int(round(s, 0))) + " Seconds "
    return output

def Developer(ctx):
    return ctx.author.id == 374622847672254466

def fuckmicroseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)