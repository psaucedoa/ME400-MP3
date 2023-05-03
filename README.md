### Full report above! Click "View code" to find our pdf!

# ME400-MP3
Files for Mini-Project 3 of Professor Leon Liebenberg's ME400 "Energy Conversion Systems" class, Spring 2023.

The premise of this project is to do the math behind a theoretical hydrogen converison of a two-stroke engine. We want to understand how the performance, temperatures, mass flow rates, and pressures would change when compared to a conventional two-stroke engine running iso-octane fuel.

Ideally all of these things would be nestled in functions and nice and presentable but unfrotunately that is a function of time which I sadly do not have haha.
# Files
"Hydrogen_air_an" is a basic combustion process with varying levels of hydrogen.
"Isooctane_analysis" is basic combustion process with varying lecels of hydrogen.

This will be cleaned up further at some later data.

# Install
Besides the usual python packages, you're gonna need PYroMat. Follow the installation instructions below (or do it the way you are most comfortable).

See https://tbretl.github.io/ae353-sp22/setup#windows on how to set up python real nice with VSCode.

See http://www.pyromat.org/download.html for PYroMat installation instructions.
# Results
Our graphs and figures are located in the folders above, labeled "Hydrogen-Air_graphs" and "Iso-Octane_graphs."

Alternitavely, one could also clone the repo and run the scripts themselves, which should produce those same graphs.
# Assumptions

Now, in order to complete this project in time (amidst other classes, coursework, research, and life), we make several important assumptions.

### All Gasses Are Ideal

We assume all gasses to be ideal. This assumption is pretty decent, considering that, for the gasses involved, we are way above the phase change point. Thankfully, we are also below the extreme temperatures at which the dissociation of molecular species dominates and begins to alter properties of the gasses involved.

### Full Combustion of Reactants

We assume the full combustion of reactants in the combustion chamber. This is important as is simplifies the reaction taking place. It also explains the very high power ratings we get from our theoretical calculations. With full combustion, combustion temperatures are incredibly high, much higher than real-life engines. This assumption also means the combustion chamber is fully evacuated after every expansion, and is fully replentished with new, uncombusted gas. This is not the true operation of many engines, particularly two-strokes, which oftentimes want some portion of the exhaust gasses to remain in the combusiton chamber as a way to increase fuel-efficiency.

### Intake Conditions at STP

We assume the gasses are at standard temperature and pressure at the intake. This may not necessarily be true for engines in the real world. Some may boost their pressures above ambient before compression. For example, many two-stroke engines use the downstroke of the piston to slightly compress the air-fuel mixture in the cranckcase, pushing it into the combustion chamber. Other engines may use a vacuum to pull air into the combustion chamber, and as a result operate with intake pressures below ambient. This is not complex to model or account for, but we have to base our intake on something we know (STP) instead of some random intake pressure which may vary from engine to engine.

### Iso-Octane Powered Engine is an Ideal Air Cycle

We are delaing with iso-octane in the liquid form, so the volume is negligible. Throughout the cycle, this may change, however, due to the high density of iso-octane and relatively low volume it would take up, we feel comfortable treating the iso-octane example as an air engine. During combustion, we add the heat of combustion from the iso-octane which would be required for stoichiometric combustion.

### Hydrogen Powered Engine is not an Ideal Air Cycle

We assume Hydrogen makes up a significant portion of the volume of the intake gas. This is in fact true, as we need twice the moles of hydrogen as oxygen present in our atmopsheric gas. However, this means that many properties of air, such as specific heats, will change. We account for this in our calculations. This also means that, since hydrogen takes up lots of volume, the amount of oxygen present in the combustion chamber is less than that of the iso-octane powered engine. We also assume the composition of the exhaust gasses remains the same as the intake gasses, just as with the iso-octane powered engine analysis. 
