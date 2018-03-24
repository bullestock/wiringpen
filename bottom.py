#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *
from defs import *

SEGMENTS = 32

def body():
    return rotate([0, 90, 0])(cylinder(h=body_l, d=body_dia))

def slot():
    return translate([-1, -slot_w/2, 0])(cube([body_l+2, slot_w, body_dia]))

def wing():
    poly = polygon(points = [ [ 0, 0 ],
                              [ wing_w, 0 ],
                              [ wing_w, wing_c_h ],
                              [ wing_c_w, wing_h ],
                              [ 0, wing_h ] ])
    shape = minkowski()(linear_extrude(height = wing_th)(poly),
                        cylinder(r = wing_r, h = 0.01))
    hole = translate([wing_h/2, 1, wing_h/2])(rotate([90, 0, 0])(cylinder(d=spool_h_dia, h = 2+wing_th)))
    return rotate([90, 0, 0])(shape) - hole

def assembly():
    b = body() - translate([-1, -body_dia/2, slot_h])(cube([body_l+2, body_dia, body_dia]))
    c_slot = translate([0, 0, -2])(slot())
    l_slot = translate([0, (slot_w+slot_wall_th), 0])(slot())
    r_slot = translate([0, -(slot_w+slot_wall_th), 0])(slot())
    handle = b - c_slot - l_slot - r_slot
    w1 = translate([-wing_w, spool_th/2+wing_th, -body_dia/2+wing_r])(wing())
    w2 = translate([-wing_w, -spool_th/2, -body_dia/2+wing_r])(wing())
    return handle + w1 + w2

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
