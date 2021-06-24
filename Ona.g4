grammar Ona;
// Keywords
IF   : [Ii][Ff]         ;
THEN : [Tt][Hh][Ee][Nn] ;
ELSE : [Ee][Ll][Ss][Ee] ;
END  : [Ee][Nn][Dd]     ;

// Operators
PLUS         : '+'  ;
GREATER_THAN : '>=' ;
NOT_EQUALS   : '!=' ;

// More generic tokens
WS    : [ \t] -> skip ;
ENTER : [\r]?[\n]     ;
IDENTIFIER : [A-Za-z_][A-Za-z0-9_]*   ;
NUMBER     : [0-9]+ | [0-9]*[.][0-9]+ ;
STRING     : ['] (~[^'\\]|[\\].)* ['] ;

variableAssignmentStatement
  : IDENTIFIER '=' expression ;
ifStatement
  : IF expression THEN statementList (ELSE statementList)? END ;
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
  : IDENTIFIER                                       # variableExpression
  | NUMBER                                           # numberLiteralExpression
  | STRING                                           # stringLiteralExpression
  | functionCall                                     # functionCallExpression
  | expression PLUS expression                       # binaryAdditionExpression
  | expression GREATER_THAN expression               # greatherThanExpression
  | expression NOT_EQUALS expression                 # notEqualsExpression
  ;
 expressionList
  : expression (',' expression)*
  |
  ;
