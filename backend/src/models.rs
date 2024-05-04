use diesel::{
    prelude::Insertable, query_builder::AsChangeset, ExpressionMethods, PgTextExpressionMethods,
    QueryDsl, Queryable, RunQueryDsl, Selectable,
};
use serde::{Deserialize, Serialize};

use crate::db::connection;

#[derive(Queryable, Selectable, Deserialize, Serialize, Clone)]
#[diesel(table_name = crate::schema::Product)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Product {
    pub item_id: String,
    pub name: String,
    pub description: Option<String>,
    pub price: Option<f64>,
    pub category: Option<String>,
}

#[derive(Queryable, Selectable, Deserialize, Serialize, Clone)]
#[diesel(table_name = crate::schema::Location)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Location {
    pub location_id: String,
    pub name: Option<String>,
    pub location_name: Option<String>,
    pub floor: Option<i32>,
}

#[derive(Queryable, Selectable, Deserialize, Serialize)]
#[diesel(table_name = crate::schema::ProductLocation)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct ProductLocation {
    item_id: String,
    location_id: String,
    quantity: Option<i32>,
}

impl Product {
    pub async fn get_by_query(_query: crate::Query) -> Result<Vec<Product>, diesel::result::Error> {
        use crate::schema::Product::dsl::*;

        let mut conn = connection().unwrap();
        let mut query = crate::schema::Product::table.into_boxed();

        if let Some(_item_id) = _query.item_id {
            query = query.filter(item_id.eq(_item_id));
        }

        if let Some(_name) = _query.name {
            query = query.filter(name.ilike(format!("%{}%", _name)));
        }
        if let Some(_desc) = _query.description {
            query = query.filter(description.ilike(format!("%{}%", _desc)));
        }

        if let Some(_categeory) = _query.category {
            query = query.filter(category.ilike(format!("%{}%", _categeory)));
        }

        if let Some(_location) = _query.location {
            query = query.filter(
                crate::schema::Product::item_id.eq_any(
                    crate::schema::ProductLocation::table
                        .inner_join(crate::schema::Location::table)
                        .filter(crate::schema::Location::name.ilike(format!("%{}%", _location)))
                        .select(crate::schema::ProductLocation::item_id),
                ),
            );
        }

        if let Some(_location_name) = _query.location_name {
            query = query.filter(
                crate::schema::Product::item_id.eq_any(
                    crate::schema::ProductLocation::table
                        .inner_join(crate::schema::Location::table)
                        .filter(
                            crate::schema::Location::location_name
                                .ilike(format!("%{}%", _location_name)),
                        )
                        .select(crate::schema::ProductLocation::item_id),
                ),
            );
        }

        query.load::<self::Product>(&mut conn)
    }
}

#[derive(Serialize)]
pub struct LocationQuantity {
    pub location: Location,
    pub quantity: Option<i32>,
}

#[derive(Serialize)]
pub struct ProductLocations {
    pub product: Product,
    pub locations: Vec<LocationQuantity>,
}

impl From<Product> for ProductLocations {
    fn from(_product: Product) -> Self {
        let mut conn = connection().unwrap();

        let locations = crate::schema::ProductLocation::table
            .inner_join(crate::schema::Location::table)
            .filter(crate::schema::ProductLocation::item_id.eq(_product.clone().item_id))
            .select((
                crate::schema::Location::all_columns,
                crate::schema::ProductLocation::quantity,
            ))
            .load::<(Location, Option<i32>)>(&mut conn)
            .unwrap()
            .iter()
            .map(|(location, quantity)| LocationQuantity {
                location: location.clone(),
                quantity: quantity.clone(),
            })
            .collect();

        ProductLocations {
            product: _product,
            locations,
        }
    }
}

#[derive(Queryable, Selectable, AsChangeset, Deserialize, Serialize)]
#[diesel(table_name = crate::schema::List)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct List {
    pub id: i32,
    pub item_id: String,
    pub quantity: i32,
    pub served: bool,
}

#[derive(Insertable)]
#[diesel(table_name = crate::schema::List)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct ListWithoutId {
    pub item_id: String,
    pub quantity: i32,
    pub served: bool,
}

impl List {
    pub async fn get_all() -> Result<Vec<List>, diesel::result::Error> {
        let mut conn = connection().unwrap();
        let query = crate::schema::List::table.into_boxed();

        query.load::<self::List>(&mut conn)
    }

    pub async fn mark_served(_id: i32, status: bool) -> Result<List, diesel::result::Error> {
        use crate::schema::List::dsl::*;

        let mut conn = connection().unwrap();
        diesel::update(crate::schema::List::dsl::List)
            .filter(id.eq(_id))
            .set(served.eq(status))
            .get_result::<self::List>(&mut conn)
    }

    pub async fn create(_new_list: List) -> Result<List, diesel::result::Error> {
        let mut conn = connection().unwrap();

        // If already exists just sum the quantity
        let existing = crate::schema::List::table
            .filter(crate::schema::List::item_id.eq(_new_list.item_id.clone()))
            .get_result::<self::List>(&mut conn);

        if let Ok(mut existing) = existing {
            existing.quantity += _new_list.quantity;
            return diesel::update(crate::schema::List::table)
                .filter(crate::schema::List::item_id.eq(_new_list.item_id))
                .set(existing)
                .get_result::<self::List>(&mut conn);
        }

        let new_list = ListWithoutId {
            item_id: _new_list.item_id,
            quantity: _new_list.quantity,
            served: _new_list.served,
        };

        diesel::insert_into(crate::schema::List::table)
            .values(new_list)
            .get_result::<self::List>(&mut conn)
    }

    pub async fn delete(_id: i32) -> Result<usize, diesel::result::Error> {
        use crate::schema::List::dsl::*;

        let mut conn = connection().unwrap();
        diesel::delete(crate::schema::List::table.filter(id.eq(_id))).execute(&mut conn)
    }

    pub async fn delete_all() -> Result<usize, diesel::result::Error> {
        let mut conn = connection().unwrap();
        diesel::delete(crate::schema::List::table).execute(&mut conn)
    }
}
