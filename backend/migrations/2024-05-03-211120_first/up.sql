-- Your SQL goes here
  CREATE TABLE "Product" (
    "item_id" varchar PRIMARY KEY,
    "name" varchar not null,
    "description" varchar,
    "price" float,
    "category" varchar
  );

  CREATE TABLE "Location" (
    "location_id" varchar PRIMARY KEY,
    "name" varchar,
    "location_name" varchar,
    "floor" integer
  );

  CREATE TABLE "ProductLocation" (
    "item_id" varchar REFERENCES "Product",
    "location_id" varchar REFERENCES "Location",
    "quantity" integer,
    PRIMARY key ("item_id", "location_id")
  );

INSERT INTO "Product" VALUES ('1', 'Simple Bed', 'Comfy and cheap bed', '200.0', 'Bedroom');
INSERT INTO "Product" VALUES ('2', 'Honkermil', 'Best bed with worst name', '450.0', 'Bedroom');
INSERT INTO "Product" VALUES ('33', 'Sönkiler', 'A strange sink', '30.0', 'Bathroom');
 INSERT INTO "Product" VALUES ('409', 'Nordviken', 'Bar furniture', '300.0', 'Bar');
 
INSERT INTO "Location" ("location_id", "name", "location_name", "floor") VALUES (1, 'Bedroom Expositor', 'Zone A', 1);
INSERT INTO "Location" ("location_id", "name", "location_name", "floor") VALUES (2, 'Bathrooms', 'Zone D', 1);
INSERT INTO "Location" ("location_id", "name", "location_name", "floor") VALUES (3, 'Decoration', 'Zone C', 0);

INSERT INTO "ProductLocation" ("item_id", "location_id", "quantity") VALUES ('1', '1', '20');
INSERT INTO "ProductLocation" ("item_id", "location_id", "quantity") VALUES ('2', '1', '20');
INSERT INTO "ProductLocation" ("item_id", "location_id", "quantity") VALUES ('33', '2', '5');
INSERT INTO "ProductLocation" ("item_id", "location_id", "quantity") VALUES ('409', '3', '20');