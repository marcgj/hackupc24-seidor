// @generated automatically by Diesel CLI.

diesel::table! {
    List (id) {
        id -> Int4,
        item_id -> Varchar,
        quantity -> Int4,
        served -> Bool,
    }
}

diesel::table! {
    Location (location_id) {
        location_id -> Varchar,
        name -> Nullable<Varchar>,
        location_name -> Nullable<Varchar>,
        floor -> Nullable<Int4>,
    }
}

diesel::table! {
    Product (item_id) {
        item_id -> Varchar,
        name -> Varchar,
        description -> Nullable<Varchar>,
        price -> Nullable<Float8>,
        category -> Nullable<Varchar>,
    }
}

diesel::table! {
    ProductLocation (item_id, location_id) {
        item_id -> Varchar,
        location_id -> Varchar,
        quantity -> Nullable<Int4>,
    }
}

diesel::joinable!(List -> Product (item_id));
diesel::joinable!(ProductLocation -> Location (location_id));
diesel::joinable!(ProductLocation -> Product (item_id));

diesel::allow_tables_to_appear_in_same_query!(
    List,
    Location,
    Product,
    ProductLocation,
);
