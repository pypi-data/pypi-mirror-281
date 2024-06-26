model RLCircuit
  Modelica.Electrical.Analog.Basic.Ground ground annotation(
    Placement(transformation(origin = {-32, -70}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Resistor resistor annotation(
    Placement(transformation(origin = {-22, 70}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Basic.Inductor inductor annotation(
    Placement(transformation(origin = {50, 70}, extent = {{-10, -10}, {10, 10}})));
  Modelica.Electrical.Analog.Sources.SineVoltage sineVoltage annotation(
    Placement(transformation(origin = {-32, 8}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
equation
  connect(resistor.n, inductor.p) annotation(
    Line(points = {{-12, 70}, {40, 70}}, color = {0, 0, 255}));
  connect(inductor.n, ground.p) annotation(
    Line(points = {{60, 70}, {68, 70}, {68, -60}, {-32, -60}}, color = {0, 0, 255}));
  connect(sineVoltage.n, ground.p) annotation(
    Line(points = {{-32, -2}, {-32, -60}}, color = {0, 0, 255}));
  connect(sineVoltage.p, resistor.p) annotation(
    Line(points = {{-32, 18}, {-32, 70}}, color = {0, 0, 255}));

annotation(
    uses(Modelica(version = "4.0.0")));
end RLCircuit;
