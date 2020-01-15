int main(){
 int n;int i;
 int a = 0;
 int b = 10;
 cin>>n;

for(i=1;i<b/2;i=i+1)
     a=a+1;

for(i=b/2;i<=b;i=i+1)
{
    if(i!=b)
     a=a+1;
}

if(a>=b)
 {
  if(a!=b)
  {
     c=a;
  }
  else
    c=0;
 }
 else
 {
 c=b;
 }

 cout<<c;

 return 0;
 }
