#!/bin/bash
./familytree clear # removes pre-existing persistent files for current testing
./familytree add relationship son nextgen
./familytree add relationship daughter nextgen
./familytree add relationship wife partner
./familytree add person vinay
./familytree add person sri
./familytree add person surya
./familytree add person satya
./familytree add person kid1
./familytree add person kid2
./familytree add person kid3
./familytree add person kid4
./familytree connect vinay --relation son --of surya
./familytree connect satya --relation wife --of surya
./familytree connect sri --relation daughter --of surya
./familytree connect kid1 --relation daughter --of vinay
./familytree connect kid4 --relation daughter --of sri
./familytree connect kid2 --relation son --of vinay
./familytree connect kid3 --relation son --of sri
