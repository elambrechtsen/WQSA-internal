--database creation */

drop table if exists news;
drop table if exists member;
drop table if exists comments;
drop table if exists events;
drop table if exists email;

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

create table events(
    events_id integer primary key autoincrement not null,
    events_title text not null unique,
    events_content text not null unique,
    events_date date not null,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

create table email(
    email_address text not null unique,
    email_date date not null
);


insert into member(name, email, password, authorisation)
values('James', 'james@gmail.com', 'temp', 0);
insert into member(name, email, password, authorisation)
values('Tilly', 'Tilly@gmail.com', 'temp', 0);
insert into member(name, email, password, authorisation)
values('Abbie', 'abbie@gmail.com', 'temp', 1);
insert into member(name, email, password, authorisation)
values('Sacha', 'sacha@gmail.com', 'temp', 1);

insert into news(title, subtitle, content, newsdate, member_id)
values ('Updates in queer news',
        'keep up to date with all the gender identities',
        'Not just male and female anymore, you can be anything you want' || char(10) ||
        'This new generation is all for being who you want to be',
        '2023-05-26 11:25:04',
        (select member_id from member where name = 'Tilly')
      );

insert into news(title, subtitle, content, newsdate, member_id)
values ('KEEP UP TO DATE',
        'news around pronouns with all the pronouns',
        'she/her, he/him, they/them' || char(10) ||
        'and more to your heart feels happy ',
        '2023-04-12 16:05:00',
        (select member_id from member where name = 'James')
      );

insert into comments(comments_content, comments_date, member_id, news_id)
values ('This is comment',
        '2023-04-12 16:05:00',
        (select member_id from member where name = 'Abbie'),
        (select news_id from news where title = 'KEEP UP TO DATE')

       );

insert into events(events_title, events_content, events_date, member_id)
values ('Charity event!',
        'We will be hosting a ball on the 2nd of November to raise money for Rainbow charities across NZ',
        '2023-13-08 21:11:04',
        (select member_id from member where name = 'James')
       );

insert into events(events_title, events_content, events_date, member_id)
values ('Picnic for queer youth',
        'Our team has collaborated to make an inter school queer picnic on Saturday the 16th of September. Make sure you come along and you can bring some friends and shared Kai for everyone to enjoy!' ||
        'It will be a great opportunity for you to meet queer youth across Wellington',
        '2023-06-08 13:25:10',
        (select member_id from member where name = 'Tilly')
       );

insert into events(events_title, events_content, events_date, member_id)
values ('Zoom call to talk about queer topics',
        'We will be having a zoom call to discuss how we can make Wellington a safer place for queer youth and how we can help. We want everyones ideas sp please cme alone! Date is tbd.',
        '2023-06-29 08:32:00',
        (select member_id from member where name = 'James')
       );

insert into email(email_address, email_date)
values ('Mikey@gmail.com',
        '2023-06-05'
       )


