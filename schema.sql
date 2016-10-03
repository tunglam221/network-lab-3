# Lim Zhi Han Ryan, 1000985
# Nguyen Tung Lam, 1001289

drop table if exists entries;
create table movies (
  id integer primary key autoincrement,
  title text not null,
  description text not null,
  director text not null,
  year integer not null,
  rating real not null,
  number_of_votes integer not null
);

create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);