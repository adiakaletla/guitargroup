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
        values('Sophie','McClintock','sophie.mcclintock@marsden.school.nz','temp','0');

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
      (select member_id from member where first_name='Sophie' )
      );

insert into news(title, subtitle, content, newsdate, member_id)
values('Sophies Solo Show',
      'Sophie McClintock performs at Marsden Gala Fundraiser.',
      'Our very own guitar group member, Sophie McClintock, performs a solo guitar piece at Marsden Old Girls fundraiser. Sophie will be performing the piece ''Riptide'' by Vance Joy in the Marsden Auditorium. This show includes various performers from different clubs in Marsden. This show begins at 7.30 pm and ends at 10 pm. Contact us to receive FREE tickets if you are a member of guitar group!',
      '2023-05-22 14:30:00',
      (select member_id from member where first_name='Adia' )
      );

insert into news(title, subtitle, content, newsdate, member_id)
values('Cultural Awards',
      'First performance at Cultural Awards',
      'Come along to Cultural Awards to enjoy a night of music and celebration. Bring a friend.',
      '2023-05-22 14:30:00',
      (select member_id from member where first_name='Sophie' )
      );

/* --------------Insert into Comments table --------------------------------------*/
insert into comments(comment, comment_date, commenter_id, news_tag_id)
values('Sounds cool! Can I bring a friend?',
      '2023-05-25 14:30:00',
      (select member_id from member where first_name='Abhi'),
       1
      );

insert into comments(comment, comment_date, commenter_id, news_tag_id)
values('Cannot wait',
      '2023-05-25 14:30:00',
      (select member_id from member where first_name='Abhi'),
       1
      );

/* --------------Insert data into Schedule table --------------------------------------*/

insert into schedule(event_name,location,date_time, notes , member_id)
      values ('Guitar Session', 'Music Room', '2023-05-17 12:10:00', 'Bring a capo along.',
              (select member_id from member where first_name='Adia' )
      );

insert into schedule(event_name,location,date_time, notes, member_id )
      values ('Audition Session', 'Lilburn Room', '2023-08-17 12:10:00', 'Guitars will be available.',
              (select member_id from member where first_name='Abhi' )
      );

insert into schedule(event_name,location,date_time, notes, member_id )
      values ('Showcase Trial', 'Auditorium', '2023-10-17 12:10:00', 'Bring your sheet music. Limited spares available.',
              (select member_id from member where first_name='Adia' )
      );