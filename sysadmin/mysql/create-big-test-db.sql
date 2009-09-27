drop database if exists test_words;
create database test_words;
use test_words;

drop table if exists words;
create table words ( 
    id int not null auto_increment primary key, 
    word varchar(30) not null, 
    key (word)
    );

load data local infile '/usr/share/dict/words'
into table words (word);
