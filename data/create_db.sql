--database creation */

drop table if exists news;
drop table if exists member;
drop table if exists comments;

--create tables

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

create table comments(
    comments_id integer primary key autoincrement not null,
    comments_content text not null unique,
    comments_date date not null,
    member_id integer not null,
    news_id integer not null,
    foreign key(member_id) references member(member_id),
    foreign key(news_id) references news(news_id)
);

insert into member(name, email, password, authorisation)
values('Mike', 'mike@gmail.com', 'temp', 0);
insert into member(name, email, password, authorisation)
values('Vanessa', 'vanessa@gmail.com', 'temp', 0);
insert into member(name, email, password, authorisation)
values('Olivia', 'olivia@gmail.com', 'temp', 1);
insert into member(name, email, password, authorisation)
values('Suzie', 'suize@gmail.com', 'temp', 1);

insert into news(title, subtitle, content, newsdate, member_id)
values ('Updates in queer news',
        'keep up to date with all the gender identities',
        'Not just male and female anymore, you can be anything you want' || char(10) ||
        'This new generation is all for being who you want to be',
        '2023-05-26 11:25:04',
        (select member_id from member where name = "Mike")
      );

insert into news(title, subtitle, content, newsdate, member_id)
values ('KEEP UP TO DATE',
        'news around pronouns with all the pronouns',
        'she/her, he/him, they/them' || char(10) ||
        'and more to your heart feels happy ',
        '2023-04-12 16:05:00',
        (select member_id from member where name = "Vanessa")
      );

insert into comments(comments_content, comments_date, member_id, news_id)
values ('This is comment',
        '2023-04-12 16:05:00',
        (select member_id from member where name = "Vanessa"),
        (select news_id from news where title = "KEEP UP TO DATE")

       )




