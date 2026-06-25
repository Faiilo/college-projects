BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "dataset_otchet" (
	"id_dataset"	INTEGER,
	"familia"	TEXT,
	"name"	TEXT,
	"otchestvo"	TEXT,
	"prac_type_id"	INTEGER,
	"module"	TEXT,
	"specialization"	TEXT,
	"kurs"	INTEGER,
	"group"	TEXT,
	"date_begin"	TEXT,
	"date_finish"	TEXT,
	"head1"	TEXT,
	"head2"	TEXT,
	"ruc_pract"	TEXT,
	"year"	INTEGER,
	"user_id"	INTEGER,
	PRIMARY KEY("id_dataset")
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "document" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "prac_type" (
	"id_prac_type"	INTEGER NOT NULL,
	"type_name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id_prac_type" AUTOINCREMENT)
);
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$1000000$TtqdF3Goki5feagYhkwM5i$MzNjh5adUrvCda88309JEGkdgpwQZ2fBvwsVXguxKuQ=','2026-03-16 08:16:15.326944',1,'sds','Салыкин','sds@test.ru',1,1,'2026-03-05 09:28:00','Дмитрий');
INSERT INTO "auth_user" VALUES (2,'pbkdf2_sha256$1000000$rMS2MIXdOooOfjdfsf8szu$pDyoH7+GSGlHrquEmJIaqdIqdksDmospk0iYwKZe224=',NULL,0,'rev','','',0,1,'2026-03-05 10:24:38.850869','');
INSERT INTO "auth_user" VALUES (3,'pbkdf2_sha256$1000000$zMKlQACJSV4vUeCLEBG3r8$recGVOQsc4q0SMzRSlLND5iV4KEaryRjsNJ6282JlhE=',NULL,0,'абас','','',0,1,'2026-03-06 10:17:52.073949','');
INSERT INTO "auth_user" VALUES (4,'pbkdf2_sha256$1000000$nYoOioJifjdfcAQeaHRwmQ$Ugjzywf4OwbjNaY91KNH9lCGAFcrFzkP7nKU25sRTx8=',NULL,0,'bibas','','',0,1,'2026-03-06 10:18:58.945634','');
INSERT INTO "auth_user" VALUES (5,'pbkdf2_sha256$1000000$Jjnd14fUnZ0pjQfnIxXUQP$pDhtD0GXM5Y/jdaK/PTmo2PkFmCBrJtmnyagV+Jcr2s=',NULL,0,'никита','','',0,1,'2026-03-06 10:20:58.199064','');
INSERT INTO "auth_user" VALUES (6,'pbkdf2_sha256$1000000$f03yDviJy0tmJ243w3jBns$Vdc7UCPFesJvQwQdDWc31KRzRZZEwXpZKg5CueWhDD0=',NULL,0,'rfrf','','',0,1,'2026-03-11 07:46:07.048122','');
INSERT INTO "auth_user" VALUES (7,'pbkdf2_sha256$1000000$lBzhPh6eu4EqkZimoUncrw$baBiIRuz0nJYppnEMYM/6cWekBdAznmAcOjm7f28d54=',NULL,0,'999','','',0,1,'2026-03-11 07:54:29.292161','');
INSERT INTO "auth_user" VALUES (8,'pbkdf2_sha256$1000000$Y4umrW6SYK5K6gFmsHV2D8$8RqijodnDfMPUS7aMnOxNZQu7i+zn27HuCF1mHTwhdA=',NULL,0,'777','','',0,1,'2026-03-11 07:56:49.889745','');
INSERT INTO "auth_user" VALUES (9,'pbkdf2_sha256$1000000$ckQUO3hz6R9SQprUzDXaTM$75owDzd1EDyFe+JF9A7A9agtprKbB1Ya4L3Ccuo+ktE=',NULL,0,'фа','','',0,1,'2026-03-13 09:22:02.876016','');
INSERT INTO "auth_user" VALUES (10,'pbkdf2_sha256$1000000$SdN7UXwkM4pmDezYAIH8yk$Dod9aGHL8K1YjOBGSrauQ4hSF7Er8GHB4yHIY4OOiIw=','2026-03-16 08:30:39.938533',0,'66','','',0,1,'2026-03-13 09:34:47.838004','');
INSERT INTO "auth_user" VALUES (11,'pbkdf2_sha256$1000000$7Y4dQtxzdPaVkSVBhDV8ak$8b1SlCcJIHNzqVn016bkcecvPNxWyF1y+fvOy3IjiMQ=',NULL,0,'gd','','',0,1,'2026-03-13 09:41:00.839310','');
INSERT INTO "auth_user" VALUES (12,'pbkdf2_sha256$1000000$5cDoHIhHxJThgYRF02bhAO$pPwkgYE3SeX8aIVQlaxS6UC2ugSb+AintmuchqMS1lE=',NULL,0,'mmm','','',0,1,'2026-03-13 09:55:43.750326','');
INSERT INTO "auth_user" VALUES (13,'pbkdf2_sha256$1000000$JcKkiqOf1paTjv8HBlLFUr$Qmun3FdzckZM545pcum3um8yTNCpZIC/L9DJkNMfsDY=',NULL,0,'13','','',0,1,'2026-03-16 07:20:33.788699','');
INSERT INTO "dataset_otchet" VALUES (1,'Иванов','Иван','Иванович',2,'Модуль 2','09.02.07 "Информационные системы и программирование"',4,'ИС-24','10.06.2025','25.06.2025','Сидоров Сидор Сидорович','Иванова Мария Петровна','Смирнов Алексей Владимирович',2026,NULL);
INSERT INTO "dataset_otchet" VALUES (2,'Петрова','Анна','Сергеевна',1,'Модуль 2','09.02.07 "Информационные системы и программирование"',4,'ИС-25','10.06.2025','25.06.2025','Петров Петр Петрович','Сидорова Анна Ивановна','Козлова Елена Дмитриевна',2026,NULL);
INSERT INTO "django_admin_log" VALUES (1,'1','sds',2,'[{"changed": {"fields": ["First name", "Last name"]}}]',4,1,'2026-03-05 09:36:26.907994');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'auth','user');
INSERT INTO "django_content_type" VALUES (5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (6,'sessions','session');
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2026-03-05 09:26:12.499358');
INSERT INTO "django_migrations" VALUES (2,'auth','0001_initial','2026-03-05 09:26:12.515798');
INSERT INTO "django_migrations" VALUES (3,'admin','0001_initial','2026-03-05 09:26:12.526372');
INSERT INTO "django_migrations" VALUES (4,'admin','0002_logentry_remove_auto_add','2026-03-05 09:26:12.535394');
INSERT INTO "django_migrations" VALUES (5,'admin','0003_logentry_add_action_flag_choices','2026-03-05 09:26:12.542528');
INSERT INTO "django_migrations" VALUES (6,'contenttypes','0002_remove_content_type_name','2026-03-05 09:26:12.555913');
INSERT INTO "django_migrations" VALUES (7,'auth','0002_alter_permission_name_max_length','2026-03-05 09:26:12.563947');
INSERT INTO "django_migrations" VALUES (8,'auth','0003_alter_user_email_max_length','2026-03-05 09:26:12.573248');
INSERT INTO "django_migrations" VALUES (9,'auth','0004_alter_user_username_opts','2026-03-05 09:26:12.580214');
INSERT INTO "django_migrations" VALUES (10,'auth','0005_alter_user_last_login_null','2026-03-05 09:26:12.590866');
INSERT INTO "django_migrations" VALUES (11,'auth','0006_require_contenttypes_0002','2026-03-05 09:26:12.594017');
INSERT INTO "django_migrations" VALUES (12,'auth','0007_alter_validators_add_error_messages','2026-03-05 09:26:12.600233');
INSERT INTO "django_migrations" VALUES (13,'auth','0008_alter_user_username_max_length','2026-03-05 09:26:12.608556');
INSERT INTO "django_migrations" VALUES (14,'auth','0009_alter_user_last_name_max_length','2026-03-05 09:26:12.617690');
INSERT INTO "django_migrations" VALUES (15,'auth','0010_alter_group_name_max_length','2026-03-05 09:26:12.625720');
INSERT INTO "django_migrations" VALUES (16,'auth','0011_update_proxy_permissions','2026-03-05 09:26:12.631854');
INSERT INTO "django_migrations" VALUES (17,'auth','0012_alter_user_first_name_max_length','2026-03-05 09:26:12.639628');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2026-03-05 09:26:12.647031');
INSERT INTO "django_session" VALUES ('hcysvwc5z9iwuak2y8l2iro3pemic1ga','.eJxVjMsOwiAQAP9lz4YUKCA9eu83NMvuIlUDSR8n47-bJj3odWYyb5hw38q0r7JMM8MAGi6_LCE9pR6CH1jvTVGr2zIndSTqtKsaG8vrdrZ_g4JrgQEsUq-ljyai6ay3TntjDLJYRtZXG1zIEoQlGXFCmSLGiNT5IMFlR_D5At0bOGc:1vy56o:rM5a0MuvI657y8pORitRkyZIJWZlV1S4b6ZVXtgXxpw','2026-03-19 09:35:06.085754');
INSERT INTO "django_session" VALUES ('jmunepwxvlc4f2lfqw4mmh179wq14zug','.eJxVjMsOwiAQAP9lz4YUKCA9eu83NMvuIlUDSR8n47-bJj3odWYyb5hw38q0r7JMM8MAGi6_LCE9pR6CH1jvTVGr2zIndSTqtKsaG8vrdrZ_g4JrgQEsUq-ljyai6ay3TntjDLJYRtZXG1zIEoQlGXFCmSLGiNT5IMFlR_D5At0bOGc:1vySFv:_Ns48RndNSnJlwI884zUD0C0LpzJDxle8X7kmz_2y3s','2026-03-20 10:18:03.925490');
INSERT INTO "django_session" VALUES ('g2py9wqhas57n1l2eo922usn0zv351ud','.eJxVjEEKwyAQRe_iuogTHTVddp8zhBk1NW1RiMmq9O5FyKKFv_rv8d5ipmPP89HSNq9RXAUocfk9mcIzlU7ig8q9ylDLvq0suyJP2uRUY3rdTvcvkKnl3iUkHGK0TNGy86BGp5wxhMBhVGD6NC5ggDUheq9p8U6DGtAykfh8AecSNuk:1w23LT:5tuNOsX_W3QBzGT2QBi4E1mHVb3xRxVz8RI__5KM4ZA','2026-03-30 08:30:39.966489');
INSERT INTO "document" VALUES (1,'Титульный лист');
INSERT INTO "document" VALUES (2,'Дневник');
INSERT INTO "prac_type" VALUES (1,'Учебная');
INSERT INTO "prac_type" VALUES (2,'Производственная');
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
COMMIT;
