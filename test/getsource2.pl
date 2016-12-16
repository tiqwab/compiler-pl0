function multiply(x,y)
  var a,b,c;
begin a := x; b := y; c := 0;
  while b > 0 do
    begin
      if odd b then c := c + a;
      a := 2*a; b := b/2
    end;
  return c
end;
