// Archivo: gramatica.g4
grammar gramatica;

/* -----------------
 * Reglas del Parser (Sintaxis)
 * ----------------- */

// Un programa es una secuencia de tareas y transiciones [cite: 105]
program     : (task | transition)+ EOF ;

// 'tarea' ID '{' statement+ '}' [cite: 106]
task        : TAREA ID LBRACE statement+ RBRACE ;

// 'ir_a' ID 'si' condition ';' [cite: 107]
transition  : IR_A ID SI condition SEMI ;

// Un 'statement' es una asignación o un print
statement   : assignment_stmt
            | print_stmt
            ;

// ej: estado = "OK";
assignment_stmt : ID ASSIGN VALUE SEMI ;

// ej: print("Comenzando"); [cite: 114]
print_stmt  : PRINT LPAREN VALUE RPAREN SEMI ;

// 'ID comparator VALUE' [cite: 108]
condition   : ID comparator VALUE ;

// Comparadores
comparator  : EQ | NEQ | GT | LT | GTE | LTE ;

/* -----------------
 * Reglas del Léxico (Tokens)
 * ----------------- */

// Palabras Clave
TAREA       : 'tarea' ;
IR_A        : 'ir_a' ;
SI          : 'si' ;
PRINT       : 'print' ;

// Símbolos
LBRACE      : '{' ;
RBRACE      : '}' ;
LPAREN      : '(' ;
RPAREN      : ')' ;
SEMI        : ';' ;
ASSIGN      : '=' ;

// Comparadores
EQ          : '==' ;
NEQ         : '!=' ;
GT          : '>' ;
LT          : '<' ;
GTE         : '>=' ;
LTE         : '<=' ;

// Tipos de Datos y Variables
ID          : [a-zA-Z_] [a-zA-Z_0-9]* ;
VALUE       : STRING | NUMBER | BOOLEAN ; // Un valor puede ser string, numero o booleano

NUMBER      : [0-9]+ ('.' [0-9]+)? ;
STRING      : '"' ( ~('\\' | '"') | ('\\' .) )* '"' ;
BOOLEAN     : 'true' | 'false' ;

// Ignorar espacios en blanco y saltos de línea
WS          : [ \t\r\n]+ -> skip ;
COMMENT     : '//' ~[\r\n]* -> skip ;