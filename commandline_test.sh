#!/bin/bash
python run.py clear # removes pre-existing persistent files for current testing
python run.py add relationship son nextgen
python run.py add relationship daughter nextgen
python run.py add relationship wife partner
python run.py add person vinay
python run.py add person sri
python run.py add person surya
python run.py add person satya
python run.py add person kid1
python run.py add person kid2
python run.py add person kid3
python run.py add person kid4
python run.py connect vinay --relation son --of surya
python run.py connect satya --relation wife --of surya
python run.py connect sri --relation daughter --of surya
python run.py connect kid1 --relation daughter --of vinay
python run.py connect kid4 --relation daughter --of sri
python run.py connect kid2 --relation son --of vinay
python run.py connect kid3 --relation son --of sri
