---
theme: default
class: text-center
highlighter: shiki
layout: cover
title: Parallel programmeren
---

# Parallel programmeren

2000wetppr 2022-2023

[Engel]bert Tijskens

---

# Wie ben ik?

- Lic. Aard- en delfstofkunde, *Master in Physics of Microelectronics 
  and Material Sciences*, Doctor in de Natuurwetenschappen - en dus 
  eigenlijk geen 
- ik werk sinds 2012 voor CalcUA, de UA kernfaciliteit voor 
  supercomputing, en voor het VSC, het Vlaams Supercomputercentrum
- Daarvoor leidde ik de DEM Research Group aan de KU Leuven. DEM = 
  *Discrete Element Modelling*. Je kan het vergelijken met 
  *Molecular Dynamics*, maar dan met atomen die een vorm hebben, 
  korrels dus, of *grains* in het Engels. Daarom wordt het ook 
  *Granular Dynamics* genoemd. Korrelstromen komen in heel wat 
  industriële processen voor en het modelleren ervan is interessant,
  maar erg uitdagend omdat de fysica complex is. In tegenstelling tot 
  MD zijn interacties tussen grains dissipatief en worden de 
  contactkrachten bepaald door materiaaleigenschappen en 
  oppervlakteeigenschappen en zijn er zowel normale als tangentiële
  contactkrachten (wrijving). Bovendien zijn de korrels - afhankelijk van het
  materiaal - soms vervormbaar.

---
[![Alternate Text]({image-url})]({video-url} "Link Title")
![](/Users/etijskens/software/dev/workspace/markdown/slidev/lecture-1/spheres2000_sheet4.mp4)

---

https://www.youtube.com/watch?v=wkIadVGhQeg

---

<br/><br/>
# Doelstellingen

- wat is parallel programmeren?
- waarom parallel programmeren?
- hoe parallel programmeren?
  - gereedschap
  - principes en *best practices*
  - strategie voor wetenschappelijke softwareontwikkeling

---

<br/><br/>
# Achtergrondkennis

- hoe werkt een moderne processor?
  - geheugen
  - processor
  - acceleratoren (GPU) 
- hoe werkt een supercomputer?
  - interconnect

---

