ANTLRCLASSPATH ?= /usr/share/java/antlr4.jar:/usr/share/java/antlr4-runtime.jar
GRUN ?= /usr/share/antlr4/grun

test: grammar/OnaVisitor.py
	python3 -m unittest

clean:
	rm -rf *.pyc __pycache__ grammar/__pycache__ grammar/Ona* grammar/*.pyc
	rm -rf java-grammar

grammar/OnaLexer.py grammar/OnaParser.py grammar/OnaVisitor.py:  Ona.g4
	antlr4 -no-listener -visitor -Dlanguage=Python3 Ona.g4 -o grammar

java-grammar:  Ona.g4
	rm -rf java-grammar
	antlr4 -no-listener -no-visitor Ona.g4 -o java-grammar
	cd java-grammar/ && javac -classpath $(ANTLRCLASSPATH) *.java;

grun: java-grammar
	cd java-grammar && $(GRUN) Ona statement_list -gui

.PHONY: test clean
