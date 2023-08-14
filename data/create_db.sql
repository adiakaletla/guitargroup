/* database creation script */

drop table if exists news;
drop table if exists member;
drop table if exists schedule;
drop table if exists comments;

/* create tables */

create table member(
    member_id integer primary key autoincrement not null,
    first_name text not null,
    last_name text not null,
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
    member_id integer,
    foreign key(member_id) references member(member_id)
);

create table comments(
   comment_id integer primary key autoincrement not null,
   comment text not null,
   comment_date date not null,
   commenter_id integer,
   news_tag_id integer,
   foreign key (commenter_id) references member(member_id),
   foreign key (news_tag_id) references news(news_id)
);

create table schedule(
    schedule_id integer primary key autoincrement not null,
    event_name text not null,
    location text not null,
    date_time date not null,
    notes text,
    member_id integer,
    foreign key(member_id) references member(member_id)
);

/* --------------Insert data into Member table --------------------------------------*/

insert into member( first_name, last_name, email, password, authorisation)
        values('Adia','Janice','adiajanice@gmail.com','temp','0');

insert into member( first_name, last_name, email, password, authorisation)
        values('Abhi','Joan','abhijoan@gmail.com','temp','1');

/* --------------Insert into News table --------------------------------------*/

insert into news(title, subtitle, content, newsdate, member_id)
values('Guitar Group sing along!',
      'Wednesday Morning Tea from 10:30 to 10:40',
      'Come along to jam out to your favourite song!',
      '2023-05-17 12:10:00',
      (select member_id from member where first_name='Adia' )
      );

insert into news(title, subtitle, content, newsdate, member_id)
values('Music Quiz!',
      'Thursday lunch from 12:45 to 1:25',
      'Music Quiz held in the music room, win some prizes and have fun!',
      '2023-05-22 14:30:00',
      (select member_id from member where first_name='Abhi' )
      );

/* --------------Insert into Comments table --------------------------------------*/
insert into comments(comment, comment_date, commenter_id, news_tag_id)
values('Why is it held during short morning tea time?',
      '2023-05-25 14:30:00',
      (select member_id from member where first_name='Abhi'),
       1
      );

/* --------------Insert data into Schedule table --------------------------------------*/

insert into schedule(event_name,location,date_time, notes , member_id)
      values ('Guitar Session', 'Marsden Room 12', '2023-05-17 12:10:00', 'Bring your guitar',
              (select member_id from member where first_name='Adia' )
      );

insert into schedule(event_name,location,date_time, notes, member_id )
      values ('Audition Session', 'Marsden Room 34', '2023-08-17 12:10:00', 'Guitars will be available',
              (select member_id from member where first_name='Abhi' )
      );