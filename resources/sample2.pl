function multiply(x,y)
  var a,b,c;
begin a := x; b := y; c := 0;
  while b > 0 do
  begin
    if odd b then c := c + a;
    a := 2*a; b := b/2;
  end;
  return c
end;

const m = 7, n = 85;
var x,y;

begin
  x := m; y := n;
  write x; write y; write multiply(x,y); writeln;
end.
