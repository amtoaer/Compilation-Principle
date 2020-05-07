{随便找来一段代码 (第一类注释) }
program exRecursion;
var
   num, f: integer;
function fact(x: integer): integer; // calculates factorial of x - x! (第二类注释)

begin
   if x=0 then
      fact := 1
   else
      fact := x * fact(x-1); (* recursive call (第三类注释) *)
end; { end of function fact}

begin
   writeln(" Enter a number: ");
   readln(num);
   f := fact(num);
   
   writeln(" Factorial ", num, " is: " , f);
end.
