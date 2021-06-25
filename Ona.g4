grammar Ona;
WS    : [ \t] -> skip ;
ENTER : [\r]?[\n]     ;
IDENTIFIER : [A-Za-z_][A-Za-z0-9_]*   ;
NUMBER     : [0-9]+ | [0-9]*[.][0-9]+ ;
STRING     : ['] (~[^'\\]|[\\].)* ['] ;

variableAssignmentStatement
  : IDENTIFIER '=' expression ;
ifStatement
  : 'if' expression 'then' then_do=statementList ('else' else_do=statementList)? 'end' ;
functionCall
  : IDENTIFIER '(' expressionList ')' ;

endStatement
  : ENTER
  | ';'
  ;
statement
  : variableAssignmentStatement
  | ifStatement
  | expression
  ;
statementList
  : (endStatement* statement endStatement)* statement? endStatement? ;

expression
  : IDENTIFIER                                  # variableReferenceExpression
  | NUMBER                                      # numberLiteralExpression
  | STRING                                      # stringLiteralExpression
  | functionCall                                # functionCallExpression
  | expression '+' expression                   # binaryAdditionExpression
  | expression '>=' expression                  # greaterThanOrEqualsExpression
  | expression '!=' expression                  # notEqualsExpression
  ;
 expressionList
  : expression (',' expression)*
  |
  ;
