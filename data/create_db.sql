/* database creation script */

drop table if exists news;
drop table if exists member;

/* create tables */

create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

insert into member( name, email, password, authorisation)
values('Sophie', 'sophie.mcc@gmail.com', 'temp', 0 );
insert into member( name, email, password, authorisation)
values('Arushi', 'arushi.bgs@gmail.co.nz', 'temp', 0 );
insert into member( name, email, password, authorisation)
values('Angela', 'angela.liu@marsden.school.nz', 'temp', 1 );
insert into member( name, email, password, authorisation)
values('Phoebe', 'phoebe.coles@gmail.co', 'temp', 1 );

insert into news(title, subtitle, content, newsdate, member_id)
values('Guitar Group sing along!',
      'Wednesday Morning Tea from 10:30 to 10:40',
      'Come along to jam out to your favourite song!',
      '2023-05-17 12:10:00',
      (select member_id from member where name='Sophie' )
      );

insert into news(title, subtitle, content, newsdate, member_id)
values('Music Quiz!',
      'Thursday lunch from 12:45 to 1:25',
      'Music Quiz held in the music room, win some prizes and have fun!',
      '2023-05-22 14:30:00',
      (select member_id from member where name='Arushi' )
      );