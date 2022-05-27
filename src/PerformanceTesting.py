from src.graph import Graph
from src.landmarks import Landmarks

G1 = Graph([("A", "B"),
            ("A", "C"),
            ("B", "C"),
            ("B", "D"),
            ("B", "E"),
            ("C", "D"),
            ("C", "E"),
            ("D", "F"),
            ("D", "G"),
            ("E", "G"),
            ("E", "F"),
            ("F", "H"),
            ("G", "H")
            ])

L1 = Landmarks(G1, 3, method='hd')

test11 = L1.landmarks_basic("A", "E")
test12 = L1.landmarks_lca("A", "E")
print(test11)
if (test11 > 3):
    print("fail 11")
print(test12)
if (test12 > 3):
    print("fail 12")

test21 = L1.landmarks_basic("A", "G")
test22 = L1.landmarks_lca("A", "G")
print(test21)
if (test21 > 4):
    print("fail 21")
print(test22)
if (test22 > 4):
    print("fail 22")

test31 = L1.landmarks_basic("C", "H")
test32 = L1.landmarks_lca("C", "H")
print(test31)
if (test31 > 4):
    print("fail 31")
print(test32)
if (test32 > 4):
    print("fail 32")

G2 = Graph([("A", "B"),
            ("A", "C"),
            ("A", "F"),
            ("B", "C"),
            ("B", "D"),
            ("C", "F"),
            ("C", "D"),
            ("D", "E"),
            ("E", "F")
            ])

L2 = Landmarks(G2, 3, method='hd')

test41 = L1.landmarks_basic("A", "E")
test42 = L1.landmarks_lca("A", "E")
print(test41)
if (test41 > 3):
    print("fail 41")
print(test42)
if (test42 > 3):
    print("fail 42")

test51 = L1.landmarks_basic("A", "D")
test52 = L1.landmarks_lca("A", "D")
print(test51)
if (test51 > 3):
    print("fail 51")
print(test52)
if (test52 > 3):
    print("fail 52")

# Граф Халина
G3 = Graph([("0", "1"),
            ("0", "2"),
            ("0", "7"),
            ("1", "2"),
            ("1", "3"),
            ("2", "6"),
            ("3", "4"),
            ("3", "5"),
            ("4", "5"),
            ("4", "20"),
            ("5", "6"),
            ("6", "10"),
            ("7", "8"),
            ("7", "9"),
            ("8", "9"),
            ("8", "12"),
            ("9", "10"),
            ("10", "11"),
            ("10", "12"),
            ("11", "13"),
            ("11", "14"),
            ("12", "13"),
            ("13", "15"),
            ("14", "16"),
            ("14", "20"),
            ("15", "16"),
            ("15", "17"),
            ("16", "17"),
            ("16", "18"),
            ("16", "19"),
            ("17", "18"),
            ("18", "19"),
            ("19", "20")
            ])

L3 = Landmarks(G3, 5, method='bc')

test61 = L3.landmarks_basic("0", "3")
test62 = L3.landmarks_lca("0", "3")
print(test61)
if (test61 > 3):
    print("fail 61")
print(test62)
if (test62 > 3):
    print("fail 62")

test71 = L3.landmarks_basic("0", "5")
test72 = L3.landmarks_lca("0", "5")
print(test71)
if (test71 > 4):
    print("fail 71")
print(test72)
if (test72 > 4):
    print("fail 72")

test81 = L3.landmarks_basic("9", "17")
test82 = L3.landmarks_lca("9", "17")
print(test81)
if (test81 > 6):
    print("fail 81")
print(test82)
if (test82 > 6):
    print("fail 82")
