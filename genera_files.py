import xsdtools
import pathlib 
from collections import deque 
from glob import glob

schema = '../qeschemas/PW_CPV/test_schemas/qes_211101.xsd' 
temps = map(pathlib.Path,glob('src/xsdtools/codes/templates/qe/*/qes_*_module.f90.jinja'))

g1 = ( (xsdtools.QEFortranGenerator(schema, p.parent ),p.name) for p in temps) 
g2 = (_[0].render_to_files(_[1], force=True) for _ in g1)
deque(g2, maxlen=0)
