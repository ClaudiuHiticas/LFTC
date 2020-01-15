%{
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int yylex();
int yyparse();
int main_lex();

void yyerror(const char *str) {
  fprintf(stderr,"> Error: %s.\n",str);
  exit(0);
}

int yywrap() {
  return 1;
}

int yydebug = 1;

int main(argc, argv)
int argc;
char **argv;
{
  main_lex(argc, argv);
  yyparse();
  fprintf(stdout, "> Finished: No syntax errors\n");
}

%}

%token ID INT CHAR FLOAT CIN COUT IF ELSE WHILE FOR MAIN OBRACE EBRACE
%token SEMICOLON OPAR EPAR PLUS MINUS MULT DIV MOD GT LT GE LE EQ NOTEQ
%token ASSIGN RETURN

%union
{
  int integer;
  float real;
  char *text;
}

%token <integer> INTEGER
%token <float> REAL
%token <text> TEXT

%%
program:
        | INT MAIN OPAR EPAR compound_stmt
        ;

type: INT
    | FLOAT
    | CHAR
    ;

compound_stmt:
        | OBRACE stmt_list EBRACE
        ;

stmt_list:
        | stmt_list stmt ;

stmt: decl SEMICOLON
    | assign SEMICOLON
    | return SEMICOLON
    | iostmt SEMICOLON
    | loop
    | if_stmt
	| for
    ;

decl:
      type ID
	| type assign
    ;

assign: ID ASSIGN expr
    ;

op: PLUS
  | MINUS
  | MULT
  | DIV
  | MOD
  ;

constant: INTEGER
  | REAL
  ;

expr: ID
    | constant
    | expr op ID
    | expr op constant
    | OPAR expr EPAR
    ;

return: RETURN INTEGER
    ;

iostmt: input
    | output
    ;

input: CIN ID
    ;
output:
    COUT ID {
      printf("cout id\n");
    }
    | COUT INTEGER {
      printf("cout int\n");
    }
    | COUT FLOAT {
      printf("cout float\n");
    }
    | COUT CHAR {
      printf("cout char\n");
    }
    ;

loop: WHILE OPAR condition EPAR compound_stmt
	|WHILE OPAR condition EPAR stmt
    ;

condition: expr relation_op expr
    ;

relation_op: EQ
    | NOTEQ
    | LT
    | LE
    | GT
    | GE
    ;

if_stmt: IF OPAR condition EPAR compound_stmt
	|IF OPAR condition EPAR stmt
    |IF OPAR condition EPAR compound_stmt ELSE compound_stmt
	|IF OPAR condition EPAR compound_stmt ELSE stmt
	|IF OPAR condition EPAR stmt ELSE compound_stmt
    |IF OPAR condition EPAR stmt ELSE stmt
    ;
	
	
for:  FOR OPAR assign SEMICOLON condition SEMICOLON assign EPAR stmt
|FOR OPAR assign SEMICOLON condition SEMICOLON assign EPAR compound_stmt
;

%%

