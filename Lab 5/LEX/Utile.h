#include<stdio.h>
#include<string.h>
#include<math.h>

typedef struct{
  int id1;
  int id2;
}PIF;

typedef struct{
  char name[250];
}TSiden,TSstring;


int pifLength = 0;
int intLength = 0;
int floatLength = 0;
int stringLength = 0;
int identifierLength = 0;

int intCode = 2;
int floatCode = 3;
int stringCode = 1;
int identifierCode = 0;

int TSints[30];
float TSfloats[30];
TSstring TSstrings[30];
TSiden TSidentifiers[30];
PIF program[300];




void addPIF(int id1,int id2){
  program[pifLength].id1 = id1;
  program[pifLength].id2 = id2;
  ++pifLength;
}


void addInt(int atom){
  int found = 0;
  int i ;
  for(int i=0;i<intLength;++i){
    if(TSints[i] == atom){
      found = 1;
      addPIF(intCode,i);
    }
  }
  if(found == 0){
    TSints[intLength] = atom;
    addPIF(intCode,intLength);
    ++intLength;
  }
}

void addFloat(float atom){
  int found = 0;
  int i ;
  for(int i=0;i<floatLength;++i){
    if(TSfloats[i] == atom){
      found = 1;
      addPIF(floatCode,i);
    }
  }
  if(found == 0){
    TSfloats[floatLength] = atom;
    addPIF(floatCode,floatLength);
    ++floatLength;
  }
}

void addString(char *atom){
  int found = 0;
  int i = 0;
  while(i < stringLength){
    int res = strcmp(TSstrings[i].name,atom);
    if(res == 0){
      found = 1;
      addPIF(stringCode,i);
    }
    ++i;
  }
  if(found == 0){
    strcpy(TSstrings[stringLength].name,atom);
    addPIF(stringCode,stringLength);
    stringLength++;
  }
}

void addIdentifier(char *atom){
  if (strlen(atom) > 250) {
    fprintf(stderr, "ERROR: Identifier %s is too long!\n", atom);
    return ;
  }
  int found = 0;
  int i = 0;
  while(i < identifierLength){
    int res = strcmp(TSidentifiers[i].name,atom);
    if(res == 0){
      found = 1;
      addPIF(identifierCode,i);
    }
    ++i;
  }
  if(found == 0){
    strcpy(TSidentifiers[identifierLength].name,atom);
    addPIF(identifierCode,identifierLength);
    identifierLength++;
  }
}

void showPIF(){
  printf("PIF:\n");
  int t;
  for(t = 0; t < pifLength;++t){
    if(program[t].id1 != identifierCode && program[t].id1 != intCode && program[t].id1 != floatCode && program[t].id1 != stringCode){
      printf(" %d|- ",program[t].id1);
    }
    else{
      printf(" %d|%d ",program[t].id1,program[t].id2);
    }
  }
  printf("\n");
}

void showInt(){
  printf("Integers: \n");
  for(int i=0;i<intLength;++i){
    printf(" %d|%d", TSints[i],i);
  }
  printf("\n");
}

void showFloat(){
  printf("Floats: \n");
  for(int i=0;i<floatLength;++i){
    printf(" %f|%d", TSfloats[i],i);
  }
  printf("\n");
}

void showString(){
    printf("Chars:\n");
    for(int i = 0 ;i<stringLength;++i)
        printf(" %s|%d", TSstrings[i].name, i);
    printf("\n");
}

void showId(){
    printf("Identifiers:\n");
    for(int i = 0 ;i<identifierLength;++i)
        printf(" %s|%d", TSidentifiers[i].name, i);
    printf("\n");
}



void show(){
  showInt();
  showFloat();
  showString();
  showId();
  showPIF();
}
