begin
  if dummy1 = 0 then dummy1 := 10;
  if dummy2 < 0 then dummy2 := 10;
  if dummy3 > 0 then dummy3 := 10;
  if dummy4 <> 0 then dummy4 := 10;
  if dummy5 <= 0 then dummy5 := 10;
  if dummy6 >= 0 then dummy6 := 10;

  while dummy7 > 0 do
  begin
    dummy7 := 10;
  end;

  write dummy10;
  writeln;

  return 5;
end.
