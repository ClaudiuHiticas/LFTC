/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     ID = 258,
     INT = 259,
     CHAR = 260,
     FLOAT = 261,
     CIN = 262,
     COUT = 263,
     IF = 264,
     ELSE = 265,
     WHILE = 266,
     FOR = 267,
     MAIN = 268,
     OBRACE = 269,
     EBRACE = 270,
     SEMICOLON = 271,
     OPAR = 272,
     EPAR = 273,
     PLUS = 274,
     MINUS = 275,
     MULT = 276,
     DIV = 277,
     MOD = 278,
     GT = 279,
     LT = 280,
     GE = 281,
     LE = 282,
     EQ = 283,
     NOTEQ = 284,
     ASSIGN = 285,
     RETURN = 286,
     INTEGER = 287,
     REAL = 288,
     TEXT = 289
   };
#endif
/* Tokens.  */
#define ID 258
#define INT 259
#define CHAR 260
#define FLOAT 261
#define CIN 262
#define COUT 263
#define IF 264
#define ELSE 265
#define WHILE 266
#define FOR 267
#define MAIN 268
#define OBRACE 269
#define EBRACE 270
#define SEMICOLON 271
#define OPAR 272
#define EPAR 273
#define PLUS 274
#define MINUS 275
#define MULT 276
#define DIV 277
#define MOD 278
#define GT 279
#define LT 280
#define GE 281
#define LE 282
#define EQ 283
#define NOTEQ 284
#define ASSIGN 285
#define RETURN 286
#define INTEGER 287
#define REAL 288
#define TEXT 289




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
#line 38 "lab5.y"
{
  int integer;
  float real;
  char *text;
}
/* Line 1529 of yacc.c.  */
#line 123 "y.tab.h"
	YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

