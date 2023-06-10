import pandas as pd
import gurobipy
import os
from gurobipy import GRB, Model, quicksum
import itertools
from pp import *


cosecha, trabajadores, estanques = optimizacion_cosecha(1, 40,estanques_ocupados, total_cosechar, 0.15)
