# ¿Cómo es "hacer" un lenguaje? (ECI-2021)

Este repositorio contiene el código para la [charla] dada durante la ECI 2021
por parte de [Onapsis]. Los [slides] también están incluídos en el
repositorio.

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
- [PySECD]: Una implementación de la máquina abstracta SECD.
- [bobscheme]: Una implementación simplista de un lisp. ¡Tanto en C++ cómo en
  python!
- [MIT6001]: Una materia del MIT de la que hay grabaciones dictadas en los 80.
  La materia gira alrededor del libro
  _"[Structure and Interpretation of Computer Programs]"_. Las clases 7A, 7B,
  9A, 9B, 10A y 10B hablan específicamente sobre implementar lenguajes. Pero
  todo el curso es precioso :)
- [SOM]: Un lenguaje experimental súper chiquitito basado en smalltalk. Una
  extensión interesante del lenguaje es [MATE]
  ([pdf](https://hal.inria.fr/hal-01185843/document)) que tiene dos
  implementaciones disponibles, [TruffleMATE] y [RTruffleMate].
- [Lua]: Lua es un lenguaje pequeño del que salieron varios documentos contando
  el diseño e implementación. Dos destacables son [The Evolution of Lua], dónde
  detallan la historia del lenguaje dando contexto histórico para las
  decisiones de diseño e implementación y [The Implementation of Lua 5.0].
- [From specification to implementation]: Una charla de Yulia Starsev dónde
  habla sobre el proceso de diseño e implementación de características en
  javascript. **Es básicamente la inspiración de mi charla**. Yulia también
  tiene una serie llamada [Compiler Compiler] dónde habla mucho más a fondo
  sobre estos temas.
- [Crafting interpreters]: No lo leí personalmente pero me hablaron muy bien
  del libro :D

## ¡Está buenísimo lo que hacen! ¿Cómo me sumo a onapsis?
[onapsis.com/careers](https://onapsis.com/careers) tiene los postings
actuales, aunque no encajes a la perfección en ninguno sos más que bienvenidx
a sumar tu CV!

[charla]: http://www.youtube.com/watch?v=wzxama2RsaE
[Onapsis]: https://onapsis.com/
[unittest]: https://docs.python.org/3/library/unittest.html
[slides]: https://github.com/iglosiggio/charla-eci-2021/blob/develop/slides.pdf
[PySECD]: https://github.com/carlohamalainen/pysecd
[bobscheme]: https://github.com/eliben/bobscheme
[MIT6001]: https://youtube.com/playlist?list=PLE18841CABEA24090
[Structure and Interpretation of Computer Programs]: https://mitpress.mit.edu/sites/default/files/sicp/index.html
[SOM]: http://som-st.github.io/
[MATE]: https://dl.acm.org/doi/10.1145/2814228.2814241
[TruffleMATE]: https://github.com/charig/truffleMate
[RTruffleMate]: https://github.com/gefarion/RTruffleMate
[Lua]: https://www.lua.org/
[The Evolution of Lua]: http://www.lua.org/doc/hopl.pdf
[The Implementation of Lua 5.0]: https://www.lua.org/doc/jucs05.pdf
[From specification to implementation]: https://www.youtube.com/watch?v=uSkiDxb0m0Y
[Compiler Compiler]: https://www.youtube.com/playlist?list=PLo3w8EB99pqKF1FQllRsxyQh3sA7V2Hc-
[Crafting interpreters]: (http://craftinginterpreters.com/contents.html)