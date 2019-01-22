
USE gyft_db;
-- DROP table freelancers;

CREATE TABLE users (
 id smallint unsigned not null auto_increment, 
 username varchar(20) not null,
 email varchar(20) not null, 
 password varchar(200) not null,
 primary key (id) );
 
 
 Select * from users;

CREATE TABLE freelancers (
  id int(11) NOT NULL auto_increment,
  first_name varchar(255) NOT NULL,
  last_name varchar(255) NOT NULL,

  email varchar(255) NOT NULL unique,
  domain varchar(500) NOT NULL,
  experience varchar(500) NOT NULL,

   primary key (id)
); 

-- DROP TABLE  freelancers;

CREATE TABLE projects (
  id int(11) NOT NULL auto_increment,
  project_title varchar(255) NOT NULL,
  contact_email  varchar(255) NOT NULL,
  project_des varchar(1000) NOT NULL,
  skill_level  varchar(255) NOT NULL,

   primary key (id)
);

CREATE TABLE messages(
  id int(11) NOT NULL auto_increment,
  full_name varchar(255) NOT NULL,
  contact_email  varchar(255) NOT NULL,
  message varchar(1000) NOT NULL,
   primary key (id)
);
 Select * from users;

SELECT DOMAIN, COUNT(*) AS Domain FROM freelancers GROUP BY DOMAIN

-- ALTER TABLE freelancers
-- ADD COLUMN resume MEDIUMBLOB NOT NULL AFTER experience;

-- ALTER TABLE freelancers
-- DROP COLUMN  resume;


 Select * from freelancers;
