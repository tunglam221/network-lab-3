drop table if exists entries;
create table movies (
  id integer primary key autoincrement,
  title text not null,
  description text not null,
  director text not null,
  year integer not null,
  rating real not null
);

create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);