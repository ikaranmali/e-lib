create database elib;
use elib;
create table borrow(
	id  int primary key auto_increment,
	S_Name char(150),
	B_title varchar(150),
	date timestamp default CURRENT_TIMESTAMP,
	token_no varchar(15),
	B_Ed varchar(150),
    B_Pub varchar(150),
	due varchar(12));
    
create table b_return(
	id  int primary key auto_increment,
	St_Name char(150),
	Bo_title varchar(150),
	date timestamp default CURRENT_TIMESTAMP,
	token_no varchar(15),
    due_date varchar(12),
	charges int);
    
create table students(
	id int primary key auto_increment,
	Name char(50),
	Department char(100),
	contact varchar(13),
	gender char(7),
	date timestamp default CURRENT_TIMESTAMP);
    
create table books(
	id int primary key auto_increment,
	Title varchar(150),
	Edition varchar(150),
    Publication varchar(150),
	Author varchar(50));