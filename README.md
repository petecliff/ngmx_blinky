# NGMX Blinky
Python script that shows the current energy mix for the UK grid using:

https://carbonintensity.org.uk/

The API could be used in automation - turn on the washing machine when the sun is high e.g. - but I wanted to start small (literally) and so grabbed the Raspberry Pi that sits on my desk, pushed on the [Unicorn pHAT](https://learn.pimoroni.com/article/getting-started-with-unicorn-phat) and created a small display of the forecast energy mix of the grid in the South West of England where I live.

The pHAT I have is an 8x4 matrix of LEDs. There are 9 energy types returned by the API but "other" doesn't seem to ever have a value here so I ignored it. For the other 8 types, they each get a row and a colour. Each row has 4 LEDs to show their intensity in the mix. Each LED represents levels of intensity:

0% - LEDs off
1-12% - half brightness 1 LED
13-25% - full brightness 1 LED

and so on up to 100% being all four LEDs in that row on full.

![The Pi Zero showing grid intensity on a Unicorn pHAT](pi.jpg?raw=true "The Pi Zero showing grid intensity on a Unicorn pHAT")

Here you can see some solar (yellow), some gas (blue) and some nuclear (pink). If any coal was burning that'd be bright red!

## Why?
Why not? :-)

It is also a good conversation starter on the energy mix on the grid. Armed with that
information you can make good choices about when to do things - put the washing machine on
when the sun is high e.g.

But don't feel bad about that late night cuppa fuelled by gas.

Next step - break the washing machine - https://www.youtube.com/watch?v=WtgMESLjLoQ ? ;-)

