# ¿Cómo es "hacer" un lenguaje? (ECI-2021)

Este repositorio contiene el código para la [charla] dada durante la ECI 2021
por parte de [Onapsis].

Se requiere una instalación de ANTLR4 para la generación de código, la cuál
puede correrse ejecutando `make grammar/OnaVisitor.py`. El Makefile también
incluye el target `test` que corre [unittest] pero por ser expeditivo con la
charla terminé omitiendo este paso (no le recomendo eso al lector!).

## Bugs

La implementación de `return` para el intérprete sobre el parsetree está
**mal**, evaluar de esa manera no permite un early-return desde un `if`. Queda
cómo ejercicio interesante al lector repararlo :P

## Más data

Lista no exhaustiva de recursos que creo están buenísimos:
- [PySECD](https://github.com/carlohamalainen/pysecd): Una implementación de la máquina abstracta SECD.
- [bobscheme](https://github.com/eliben/bobscheme): Una implementación simplista de un lisp. ¡Tanto en C++ cómo en python!
- [MIT6001](https://youtube.com/playlist?list=PLE18841CABEA24090): Una materia del MIT de la que hay grabaciones dictadas en los 80. La materia gira alrededor del libro [_"Structure and Interpretation of Computer Programs"_](https://mitpress.mit.edu/sites/default/files/sicp/index.html). Las clases 7A, 7B, 9A, 9B, 10A y 10B hablan específicamente sobre implementar lenguajes. Pero todo el curso es precioso :)
- [SOM](http://som-st.github.io/): Un lenguaje experimental súper chiquitito basado en smalltalk. Una extensión interesante del lenguaje es [MATE](https://dl.acm.org/doi/10.1145/2814228.2814241) ([pdf](https://hal.inria.fr/hal-01185843/document)) que tiene dos implementaciones disponibles, [TruffleMATE](https://github.com/charig/truffleMate) y [RTruffleMate](https://github.com/gefarion/RTruffleMate)
- [Lua](https://www.lua.org/): Lua es un lenguaje pequeño del que salieron varios documentos contando el diseño y la implementación. Dos destacables son [The Evolution of Lua](http://www.lua.org/doc/hopl.pdf), dónde detallan la historia del lenguaje dando contexto histórico para las decisiones de diseño e implementación y [The Implementation of Lua 5.0](https://www.lua.org/doc/jucs05.pdf).
- [From specification to implementation](https://www.youtube.com/watch?v=uSkiDxb0m0Y): Una charla de Yulia Starsev dóne habla sobre el proceso de diseño e implementación de características en javascript. **Es básicamente la inspiración de mi charla**. Yulia también tiene una serie llamada [Compiler Compiler](https://www.youtube.com/playlist?list=PLo3w8EB99pqKF1FQllRsxyQh3sA7V2Hc-) dónde habla mucho más sobre estos temas.

## ¡Está buenísimo lo que hacen! ¿Cómo me sumo a onapsis?
[onapsis.com/careers](https://onapsis.com/careers) tiene los postings
actuales, aunque no encajes a la perfección en ninguno sos más que bienvenidx
a sumar tu CV!

[charla]: http://www.youtube.com/watch?v=wzxama2RsaE
[Onapsis]: https://onapsis.com/
[unittest]: https://docs.python.org/3/library/unittest.html
