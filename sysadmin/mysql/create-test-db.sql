drop database if exists test;
create database test;
use test;

CREATE TABLE animal
   (
     name     CHAR(40),
     category CHAR(40)
   );
CREATE TABLE mineral
   (
     name     CHAR(40),
     category CHAR(40)
   );
CREATE TABLE vegetable
   (
     name     CHAR(40),
     category CHAR(40)
   );
CREATE TABLE catalog
   (
     name   CHAR(40),
     thing_id   CHAR(10)
   );
INSERT INTO animal (name, category)
       VALUES
         ('snake', 'reptile'),
         ('frog', 'amphibian'),
         ('tuna', 'fish'),
         ('racoon', 'mammal');
INSERT INTO mineral (name, category)
       VALUES
         ('feldspar', 'silicate'),
         ('celestine', 'sulfate'),
         ('halite', 'halide'),
         ('hematite', 'oxide'),
         ('pyrite', 'sulfide'),
         ('arsenate', 'phosphate');
INSERT INTO vegetable (name, category)
       VALUES
         ('cress', 'leafy'),
         ('luffa', 'flowering'),
         ('lentil', 'podded'),
         ('garlic', 'bulb'),
         ('daikon', 'tuberous'),
         ('dulse', 'sea');
INSERT INTO catalog (name, thing_id)
      VALUES
        ('animal', '0'),
        ('mineral', '1'),
        ('vegetable', '2');
