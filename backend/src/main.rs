use std::vec;

use actix_web::{
    delete, get, middleware::Logger, post, put, web, App, HttpResponse, HttpServer, Responder,
};
use dotenvy::dotenv;
use env_logger::Env;

mod db;
mod models;
mod schema;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    env_logger::init_from_env(Env::default().default_filter_or("info"));

    // Dotenv load
    dotenv().ok();

    // Init DB
    db::init();
    print!("STARTING SERVER\n");
    HttpServer::new(move || {
        {
            // Auth
            App::new()
                .service(warehouse)
                .service(get_list)
                .service(mark_served)
                .service(mark_not_served)
                .service(add_list_item)
                .service(delete_list_item)
                .service(delete_all_list_items)
        }
        .wrap(Logger::default())
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}

#[derive(Debug, serde::Deserialize)]
pub struct Query {
    pub name: Option<String>,
    pub item_id: Option<String>,
    pub category: Option<String>,
    pub location: Option<String>,
    pub location_name: Option<String>,
    pub description: Option<String>,
}

#[get("/warehouse")]
async fn warehouse(query: web::Query<Query>) -> impl Responder {
    let products = models::Product::get_by_query(query.into_inner())
        .await
        .unwrap();

    let mut product_locations: Vec<models::ProductLocations> = vec![];
    for product in products {
        product_locations.push(models::ProductLocations::from(product));
    }

    HttpResponse::Ok().json(product_locations)
}

#[get("/list")]
async fn get_list() -> impl Responder {
    let list_items = models::List::get_all().await.unwrap();
    HttpResponse::Ok().json(list_items)
}

#[put("/list/{id}/served")]
async fn mark_served(path: web::Path<i32>) -> impl Responder {
    let id = path.into_inner();
    let list_item = models::List::mark_served(id, true).await.unwrap();
    HttpResponse::Ok().json(list_item)
}

#[put("/list/{id}/not_served")]
async fn mark_not_served(path: web::Path<i32>) -> impl Responder {
    let id = path.into_inner();
    let list_item = models::List::mark_served(id, true).await.unwrap();
    HttpResponse::Ok().json(list_item)
}

#[post("/list")]
async fn add_list_item(list_item: web::Json<models::List>) -> impl Responder {
    let res = models::List::create(list_item.into_inner()).await;

    match res {
        Ok(item) => HttpResponse::Ok().json(item),
        Err(err) => HttpResponse::InternalServerError().json(err.to_string()),
    }
}

#[delete("/list/{id}")]
async fn delete_list_item(path: web::Path<i32>) -> impl Responder {
    let id = path.into_inner();
    let res = models::List::delete(id).await;

    match res {
        Ok(_) => HttpResponse::Ok().finish(),
        Err(err) => HttpResponse::InternalServerError().json(err.to_string()),
    }
}

#[delete("/list")]
async fn delete_all_list_items() -> impl Responder {
    let res = models::List::delete_all().await;

    match res {
        Ok(_) => HttpResponse::Ok().finish(),
        Err(err) => HttpResponse::InternalServerError().json(err.to_string()),
    }
}
