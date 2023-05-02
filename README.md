# ME400-MP3
Files for the project. Ideally all of these things would be nestled in functions and nice but that is for later.
# Files
"Hydrogen-Rich" is a basic combustion process with excess hydrogen.
"Hydrogen air analysis" is basic combustion with stoichiometric ratios.
"Iso-octane analysis" is ... stoichiometric.

This will be cleaned up at some later data.

# Install
You're gonna need PYroMAT. Follow the installation instructions or do it the way you are most comfortable.
See https://tbretl.github.io/ae353-sp22/setup#windows on how to set up python real nice with VSCode.

# Assumptions
The premise of this project is to do the math behind a theoretical hydrogen converison of a two-stroke engine. Basically to see what would happen, how would the performance chnage, what would the temperatures, mass flow rates, pressures, etc., look like when compared to a conventional two-stroke engine running iso-octane fuel.

Now, in order to complete this project in time (amidst other classes, coursework, research, and life), we make several important assumptions.

### All Gasses Are Ideal

We assume all gasses to be ideal. This assumption is pretty decent, considering that, for the gasses involved, we are way above the phase change point. Thankfully, we are also below the extreme temperatures at which the dissociation of molecular species dominates and begins to alter properties of the gasses involved.

### Full Combustion of Reactants

We assume the full combustion of reactants in the combustion chamber. This is important as is simplifies the reaction taking place. It also explains the very high power ratings we get from our theoretical calculations. With full combustion, combustion temperatures are incredibly high, much higher than real-life engines. This assumption also means the combustion chamber is fully evacuated after every expansion, and is fully replentished with new, uncombusted gas. This is not the true operation of many engines, particularly two-strokes, which oftentimes want some portion of the exhaust gasses to remain in the combusiton chamber as a way to increase fuel-efficiency.

### Intake Conditions at STP

We assume the gasses are at standard temperature and pressure at the intake. This may not necessarily be true for engines in the real world. Some may boost their pressures above ambient before compression. For example, many two-stroke engines use the downstroke of the piston to slightly compress the air-fuel misture in the cranckcase, pushing it into the combustion chamber. Other engines may use a vacuum to pull air into the combustion chamber, and as a result operate with intake pressures below ambient. This is not complex to model or account for, but we have to base our intake on something we know (STP) instead of some random intake pressure which may vary from engine to engine.