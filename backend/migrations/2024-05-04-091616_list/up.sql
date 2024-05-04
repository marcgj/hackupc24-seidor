-- Your SQL goes here
create table "List"(
    id serial primary key,
    item_id VARCHAR not null REFERENCES "Product",
    quantity int not null,
    served boolean not null default false
);

insert into "List" VALUES (1, '1', 2, false); 
insert into "List" VALUES (2, '2', 2, false); 

