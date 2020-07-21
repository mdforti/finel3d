// Gmsh project created on Fri May 22 21:02:39 2020
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {20, 0, 0, 1.0};
//+
Point(3) = {20, 10, 0, 1.0};
//+
Point(4) = {0, 10, 0, 1.0};
//+
Point(5) = {10, 5, 0, 1.0};
//+
Point(6) = {11, 5, 0, 1.0};
//+
Point(7) = {9, 5, 0, 1.0};
//+
Point(8) = {0, 5, 0, 1.0};
//+
Point(9) = {20, 5, 0, 1.0};
//+
Point(10) = {10, 10, 0, 1.0};
//+
Point(11) = {10, 0, 0, 1.0};
//+
Point(12) = {10, 6, 0, 1.0};
//+
Point(13) = {10, 4, 0, 1.0};
//+
Line(1) = {4, 10};
//+
Line(2) = {4, 8};
//+
Line(3) = {8, 7};
//+
Line(4) = {12, 10};
//+
Line(5) = {10, 3};
//+
Line(6) = {3, 9};
//+
Line(7) = {9, 6};
//+
Line(8) = {13, 11};
//+
Line(9) = {11, 2};
//+
Line(10) = {2, 9};
//+
Line(11) = {11, 1};
//+
Line(12) = {1, 8};
//+
Circle(13) = {13, 5, 6};
//+
Circle(14) = {6, 5, 12};
//+
Circle(15) = {12, 5, 7};
//+
Circle(16) = {7, 5, 13};
//+
Curve Loop(1) = {2, 3, -15, 4, -1};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {5, 6, 7, 14, 4};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {7, -13, 8, 9, 10};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {8, 11, 12, 3, 16};
//+
Plane Surface(4) = {4};
//+
Physical Curve("border_1", 1) = {1, 5};
//+
Physical Curve("border_2", 2) = {6, 10};
//+
Physical Curve("border_3", 3) = {9, 11};
//+
Physical Curve("border_4", 4) = {12, 2};
//+
Physical Curve("hole", 5) = {14, 13, 16, 15};
//+
Physical Curve("sym_Y", 6) = {7, 3};
//+
Physical Curve("sym_X", 7) = {4, 8};
//+
Physical Surface("sup1", 8) = {2, 1};
//+
Physical Surface("sup2", 9) = {4, 3};
