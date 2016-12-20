function plus(x,y)
  var a, b;
begin a := x; b := y;
  return (a + b)
end;

const m = 7, n = 8;
var x,y;

begin
  write m;
  write n;
  writeln;
  write plus(m, n);
  writeln;
end.
