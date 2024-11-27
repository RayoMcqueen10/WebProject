-- Migrations will appear here as you chat with AI

create table users (
  id bigint primary key generated always as identity,
  username text not null unique,
  email text not null unique,
  password_hash text not null,
  role text not null check (role in ('admin', 'user')),
  created_at timestamp with time zone default now(),
  last_login timestamp with time zone
);

create table games (
  id bigint primary key generated always as identity,
  title text not null,
  genre text not null,
  platform text not null check (platform in ('ps5', 'xbox')),
  price numeric(10, 2) not null,
  release_date date not null,
  stock int not null default 0
);

create table orders (
  id bigint primary key generated always as identity,
  user_id bigint not null references users (id),
  order_date timestamp with time zone default now(),
  total_amount numeric(10, 2) not null
);

create table order_items (
  id bigint primary key generated always as identity,
  order_id bigint not null references orders (id),
  game_id bigint not null references games (id),
  quantity int not null,
  price_at_purchase numeric(10, 2) not null
);

create table reviews (
  id bigint primary key generated always as identity,
  user_id bigint not null references users (id),
  game_id bigint not null references games (id),
  rating int not null check (
    rating >= 1
    and rating <= 5
  ),
  comment text,
  created_at timestamp with time zone default now()
);

alter table users
rename to usuarios;

alter table games
rename to juegos;

alter table orders
rename to ordenes;

alter table order_items
rename to articulos_orden;

alter table reviews
rename to "reseñas";