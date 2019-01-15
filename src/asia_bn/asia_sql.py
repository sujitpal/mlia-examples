# -*- coding: utf-8 -*-

import sqlite3 as sql

def isEmpty(conn):
  cur = conn.cursor()
  cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
  rows = cur.fetchall()
  return len(rows) == 0

def train(conn):
  if isEmpty(conn):
    print "empty db, creating tables"
    cur = conn.cursor()
    cur.executescript("""
      CREATE TABLE A (A INT, P REAL);
      INSERT INTO A VALUES (0, 0.99);
      INSERT INTO A VALUES (1, 0.01);
      CREATE TABLE S (S INT, P REAL);
      INSERT INTO S VALUES (0, 0.5);
      INSERT INTO S VALUES (1, 0.5);
      CREATE TABLE T (T INT, A INT, P REAL);
      INSERT INTO T VALUES (0, 0, 0.99);
      INSERT INTO T VALUES (0, 1, 0.95);
      INSERT INTO T VALUES (1, 0, 0.01);
      INSERT INTO T VALUES (1, 1, 0.05);
      CREATE TABLE L (L INT, S INT, P REAL);
      INSERT INTO L VALUES (0, 0, 0.99);
      INSERT INTO L VALUES (0, 1, 0.9);
      INSERT INTO L VALUES (1, 0, 0.01);
      INSERT INTO L VALUES (1, 1, 0.1);
      CREATE TABLE B (B INT, S INT, P REAL);
      INSERT INTO B VALUES (0, 0, 0.7);
      INSERT INTO B VALUES (0, 1, 0.4);
      INSERT INTO B VALUES (1, 0, 0.3);
      INSERT INTO B VALUES (1, 1, 0.6);
      CREATE TABLE E (E INT, L INT, T INT, P REAL);
      INSERT INTO E VALUES (0, 0, 0, 1.0);
      INSERT INTO E VALUES (0, 0, 1, 0.0);
      INSERT INTO E VALUES (0, 1, 0, 0.0);
      INSERT INTO E VALUES (0, 1, 1, 0.0);
      INSERT INTO E VALUES (1, 0, 0, 0.0);
      INSERT INTO E VALUES (1, 0, 1, 1.0);
      INSERT INTO E VALUES (1, 1, 0, 1.0);
      INSERT INTO E VALUES (1, 1, 1, 1.0);
      CREATE TABLE X (X INT, E INT, P REAL);
      INSERT INTO X VALUES (0, 0, 0.95);
      INSERT INTO X VALUES (0, 1, 0.02);
      INSERT INTO X VALUES (1, 0, 0.05);
      INSERT INTO X VALUES (1, 1, 0.98);
      CREATE TABLE D (D INT, E INT, B INT, P REAL);
      INSERT INTO D VALUES (0, 0, 0, 0.90);
      INSERT INTO D VALUES (0, 0, 1, 0.20);
      INSERT INTO D VALUES (0, 1, 0, 0.30);
      INSERT INTO D VALUES (0, 1, 1, 0.10);
      INSERT INTO D VALUES (1, 0, 0, 0.10);
      INSERT INTO D VALUES (1, 0, 1, 0.80);
      INSERT INTO D VALUES (1, 1, 0, 0.70);
      INSERT INTO D VALUES (1, 1, 1, 0.90);
    """)
  conn.commit()
  
def test(conn, dis, conds):
  """
  Compute posterior probability for each disease given conditions
  """
  cur = conn.cursor()
  groupBy = ".".join([dis, dis])
  extraConds = "" if len(conds) == 0 else " AND " +  " AND ".join(conds)
  sql = """
    SELECT %s, SUM(A.P * S.P * T.P * L.P * B.P * E.P * X.P * D.P)
    FROM A, S, T, L, B, E, X, D
    WHERE D.E = E.E
    AND X.E = E.E
    AND D.B = B.B
    AND E.L = L.L
    AND E.T = T.T
    AND L.S = S.S
    AND B.S = S.S
    AND T.A = A.A
    %s
    GROUP BY %s
  """ % (groupBy, extraConds, groupBy)
  cur.execute(sql)
  rows = cur.fetchall()
  probs = {}
  sum = 0
  # normalize the scores to sum to 1
  for row in rows:
    probs[row[0]] = row[1]
    sum += row[1]
  for key in [0, 1]:
    print dis, ":", key, probs[key], probs[key] / sum

def main():
  conn = sql.connect("../../data/bnet.db")
  train(conn)
  print "## Unit test: TB should be 1% chance w/o evidence"
  for disease in ["T", "L", "B"]:
    test(conn, disease, [])
  print "## Question 1:"
  for disease in ["T", "L", "B"]:
    test(conn, disease, ["A.A=1", "S.S=0"])
  print "## Question 2:"
  for disease in ["T", "L", "B"]:
    test(conn, disease, ["A.A=1", "S.S=0", "D.D=0", "X.X=1"])
  if conn != None:
    conn.close()
    
if __name__ == "__main__":
  main()
