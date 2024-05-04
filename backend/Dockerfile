FROM rust:slim


ENV CARGO_INCREMENTAL=0

WORKDIR /backend

RUN apt-get update
RUN apt install pkg-config libssl-dev libpq-dev -y
RUN cargo install diesel_cli --no-default-features --features postgres

COPY . .
RUN cargo build

CMD ["bash", "./start.sh"]

