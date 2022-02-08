-- Adminer 4.8.1 PostgreSQL 13.5 (Debian 13.5-1.pgdg110+1) dump

DROP TABLE IF EXISTS "airs";
CREATE TABLE "public"."airs" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "air_normalise" character varying(255),
    "surnom_1" character varying(255),
    "surnom_2" character varying(255),
    "surnom_3" character varying(255),
    "surnom_4" character varying(255),
    "surnom_5" character varying(255),
    "enregistrement_air" character varying(255),
    "surnom_6" character varying(255),
    "surnom_7" character varying(255),
    "surnom_8" character varying(255),
    "surnom_9" character varying(255),
    "surnom_10" character varying(255),
    "surnom_11" character varying(255),
    "surnom_12" character varying(255),
    "surnom_13" character varying(255),
    "surnom_14" character varying(255),
    "notes_critiques_air" character varying(255),
    "sources_information_air" character varying(255),
    "sources_musicales" text,
    CONSTRAINT "airs_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "airs_references_externes";
CREATE TABLE "public"."airs_references_externes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "references_externes" uuid,
    "airs" uuid,
    CONSTRAINT "airs_references_externes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_activity";
DROP SEQUENCE IF EXISTS directus_activity_id_seq;
CREATE SEQUENCE directus_activity_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_activity" (
    "id" integer DEFAULT nextval('directus_activity_id_seq') NOT NULL,
    "action" character varying(45) NOT NULL,
    "user" uuid,
    "timestamp" timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "ip" character varying(50) NOT NULL,
    "user_agent" character varying(255),
    "collection" character varying(64) NOT NULL,
    "item" character varying(255) NOT NULL,
    "comment" text,
    CONSTRAINT "directus_activity_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_collections";
CREATE TABLE "public"."directus_collections" (
    "collection" character varying(64) NOT NULL,
    "icon" character varying(30),
    "note" text,
    "display_template" character varying(255),
    "hidden" boolean DEFAULT false NOT NULL,
    "singleton" boolean DEFAULT false NOT NULL,
    "translations" json,
    "archive_field" character varying(64),
    "archive_app_filter" boolean DEFAULT true NOT NULL,
    "archive_value" character varying(255),
    "unarchive_value" character varying(255),
    "sort_field" character varying(64),
    "accountability" character varying(255) DEFAULT 'all',
    "color" character varying(255),
    "item_duplication_fields" json,
    "sort" integer,
    "group" character varying(64),
    "collapse" character varying(255) DEFAULT 'open' NOT NULL,
    CONSTRAINT "directus_collections_pkey" PRIMARY KEY ("collection")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_dashboards";
CREATE TABLE "public"."directus_dashboards" (
    "id" uuid NOT NULL,
    "name" character varying(255) NOT NULL,
    "icon" character varying(30) DEFAULT 'dashboard' NOT NULL,
    "note" text,
    "date_created" timestamptz DEFAULT CURRENT_TIMESTAMP,
    "user_created" uuid,
    CONSTRAINT "directus_dashboards_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_fields";
DROP SEQUENCE IF EXISTS directus_fields_id_seq;
CREATE SEQUENCE directus_fields_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_fields" (
    "id" integer DEFAULT nextval('directus_fields_id_seq') NOT NULL,
    "collection" character varying(64) NOT NULL,
    "field" character varying(64) NOT NULL,
    "special" character varying(64),
    "interface" character varying(64),
    "options" json,
    "display" character varying(64),
    "display_options" json,
    "readonly" boolean DEFAULT false NOT NULL,
    "hidden" boolean DEFAULT false NOT NULL,
    "sort" integer,
    "width" character varying(30) DEFAULT 'full',
    "translations" json,
    "note" text,
    "conditions" json,
    "required" boolean DEFAULT false,
    "group" character varying(64),
    CONSTRAINT "directus_fields_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_files";
CREATE TABLE "public"."directus_files" (
    "id" uuid NOT NULL,
    "storage" character varying(255) NOT NULL,
    "filename_disk" character varying(255),
    "filename_download" character varying(255) NOT NULL,
    "title" character varying(255),
    "type" character varying(255),
    "folder" uuid,
    "uploaded_by" uuid,
    "uploaded_on" timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "modified_by" uuid,
    "modified_on" timestamptz DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "charset" character varying(50),
    "filesize" bigint,
    "width" integer,
    "height" integer,
    "duration" integer,
    "embed" character varying(200),
    "description" text,
    "location" text,
    "tags" text,
    "metadata" json,
    CONSTRAINT "directus_files_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_folders";
CREATE TABLE "public"."directus_folders" (
    "id" uuid NOT NULL,
    "name" character varying(255) NOT NULL,
    "parent" uuid,
    CONSTRAINT "directus_folders_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_migrations";
CREATE TABLE "public"."directus_migrations" (
    "version" character varying(255) NOT NULL,
    "name" character varying(255) NOT NULL,
    "timestamp" timestamptz DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "directus_migrations_pkey" PRIMARY KEY ("version")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_panels";
CREATE TABLE "public"."directus_panels" (
    "id" uuid NOT NULL,
    "dashboard" uuid NOT NULL,
    "name" character varying(255),
    "icon" character varying(30) DEFAULT 'insert_chart',
    "color" character varying(10),
    "show_header" boolean DEFAULT false NOT NULL,
    "note" text,
    "type" character varying(255) NOT NULL,
    "position_x" integer NOT NULL,
    "position_y" integer NOT NULL,
    "width" integer NOT NULL,
    "height" integer NOT NULL,
    "options" json,
    "date_created" timestamptz DEFAULT CURRENT_TIMESTAMP,
    "user_created" uuid,
    CONSTRAINT "directus_panels_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_permissions";
DROP SEQUENCE IF EXISTS directus_permissions_id_seq;
CREATE SEQUENCE directus_permissions_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_permissions" (
    "id" integer DEFAULT nextval('directus_permissions_id_seq') NOT NULL,
    "role" uuid,
    "collection" character varying(64) NOT NULL,
    "action" character varying(10) NOT NULL,
    "permissions" json,
    "validation" json,
    "presets" json,
    "fields" text,
    CONSTRAINT "directus_permissions_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_presets";
DROP SEQUENCE IF EXISTS directus_presets_id_seq;
CREATE SEQUENCE directus_presets_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_presets" (
    "id" integer DEFAULT nextval('directus_presets_id_seq') NOT NULL,
    "bookmark" character varying(255),
    "user" uuid,
    "role" uuid,
    "collection" character varying(64),
    "search" character varying(100),
    "layout" character varying(100) DEFAULT 'tabular',
    "layout_query" json,
    "layout_options" json,
    "refresh_interval" integer,
    "filter" json,
    CONSTRAINT "directus_presets_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_relations";
DROP SEQUENCE IF EXISTS directus_relations_id_seq;
CREATE SEQUENCE directus_relations_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_relations" (
    "id" integer DEFAULT nextval('directus_relations_id_seq') NOT NULL,
    "many_collection" character varying(64) NOT NULL,
    "many_field" character varying(64) NOT NULL,
    "one_collection" character varying(64),
    "one_field" character varying(64),
    "one_collection_field" character varying(64),
    "one_allowed_collections" text,
    "junction_field" character varying(64),
    "sort_field" character varying(64),
    "one_deselect_action" character varying(255) DEFAULT 'nullify' NOT NULL,
    CONSTRAINT "directus_relations_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_revisions";
DROP SEQUENCE IF EXISTS directus_revisions_id_seq;
CREATE SEQUENCE directus_revisions_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_revisions" (
    "id" integer DEFAULT nextval('directus_revisions_id_seq') NOT NULL,
    "activity" integer NOT NULL,
    "collection" character varying(64) NOT NULL,
    "item" character varying(255) NOT NULL,
    "data" json,
    "delta" json,
    "parent" integer,
    CONSTRAINT "directus_revisions_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_roles";
CREATE TABLE "public"."directus_roles" (
    "id" uuid NOT NULL,
    "name" character varying(100) NOT NULL,
    "icon" character varying(30) DEFAULT 'supervised_user_circle' NOT NULL,
    "description" text,
    "ip_access" text,
    "enforce_tfa" boolean DEFAULT false NOT NULL,
    "admin_access" boolean DEFAULT false NOT NULL,
    "app_access" boolean DEFAULT true NOT NULL,
    CONSTRAINT "directus_roles_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_sessions";
CREATE TABLE "public"."directus_sessions" (
    "token" character varying(64) NOT NULL,
    "user" uuid NOT NULL,
    "expires" timestamptz NOT NULL,
    "ip" character varying(255),
    "user_agent" character varying(255),
    "data" json,
    CONSTRAINT "directus_sessions_pkey" PRIMARY KEY ("token")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_settings";
DROP SEQUENCE IF EXISTS directus_settings_id_seq;
CREATE SEQUENCE directus_settings_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_settings" (
    "id" integer DEFAULT nextval('directus_settings_id_seq') NOT NULL,
    "project_name" character varying(100) DEFAULT 'Directus' NOT NULL,
    "project_url" character varying(255),
    "project_color" character varying(10),
    "project_logo" uuid,
    "public_foreground" uuid,
    "public_background" uuid,
    "public_note" text,
    "auth_login_attempts" integer DEFAULT '25',
    "auth_password_policy" character varying(100),
    "storage_asset_transform" character varying(7) DEFAULT 'all',
    "storage_asset_presets" json,
    "custom_css" text,
    "storage_default_folder" uuid,
    "basemaps" json,
    "mapbox_key" character varying(255),
    "module_bar" json,
    CONSTRAINT "directus_settings_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_users";
CREATE TABLE "public"."directus_users" (
    "id" uuid NOT NULL,
    "first_name" character varying(50),
    "last_name" character varying(50),
    "email" character varying(128),
    "password" character varying(255),
    "location" character varying(255),
    "title" character varying(50),
    "description" text,
    "tags" json,
    "avatar" uuid,
    "language" character varying(8) DEFAULT 'en-US',
    "theme" character varying(20) DEFAULT 'auto',
    "tfa_secret" character varying(255),
    "status" character varying(16) DEFAULT 'active' NOT NULL,
    "role" uuid,
    "token" character varying(255),
    "last_access" timestamptz,
    "last_page" character varying(255),
    "provider" character varying(128) DEFAULT 'default' NOT NULL,
    "external_identifier" character varying(255),
    "auth_data" json,
    CONSTRAINT "directus_users_email_unique" UNIQUE ("email"),
    CONSTRAINT "directus_users_external_identifier_unique" UNIQUE ("external_identifier"),
    CONSTRAINT "directus_users_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "directus_users_token_unique" UNIQUE ("token")
) WITH (oids = false);


DROP TABLE IF EXISTS "directus_webhooks";
DROP SEQUENCE IF EXISTS directus_webhooks_id_seq;
CREATE SEQUENCE directus_webhooks_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_webhooks" (
    "id" integer DEFAULT nextval('directus_webhooks_id_seq') NOT NULL,
    "name" character varying(255) NOT NULL,
    "method" character varying(10) DEFAULT 'POST' NOT NULL,
    "url" text NOT NULL,
    "status" character varying(10) DEFAULT 'active' NOT NULL,
    "data" boolean DEFAULT true NOT NULL,
    "actions" character varying(100) NOT NULL,
    "collections" text NOT NULL,
    "headers" json,
    CONSTRAINT "directus_webhooks_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "editions";
CREATE TABLE "public"."editions" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "provenance" character varying(255),
    "groupe_ouvrage" character varying(255),
    "titre_ouvrage" character varying(255),
    "auteur" character varying(255),
    "nombre_pieces" character varying(255),
    "ville_conservation_exemplaire_1" character varying(255),
    "ville_conservation_exemplaire_2" character varying(255),
    "ville_conservation_exemplaire_3" character varying(255),
    "ville_conservation_exemplaire_4" character varying(255),
    "ville_conservation_exemplaire_5" character varying(255),
    "depot_conservation_exemplaire_1" character varying(255),
    "depot_conservation_exemplaire_2" character varying(255),
    "depot_conservation_exemplaire_3" character varying(255),
    "depot_conservation_exemplaire_4" character varying(255),
    "depot_conservation_exemplaire_5" character varying(255),
    "prefixe_cote" character varying(255),
    "numero_cote" character varying(255),
    "annee_indiquee" character varying(255),
    "annee_estimee" character varying(255),
    "format" character varying(255),
    "manuscrit_imprime" character varying(255),
    "forme_editoriale" character varying(255),
    "lieu_edition_indique" character varying(255),
    "lieu_edition_reel" character varying(255),
    "lieu_edition_source_information" character varying(255),
    "editeur_libraire_imprimeur" character varying(255),
    "editeur" character varying(255),
    "libraire" character varying(255),
    "imprimeur" character varying(255),
    "editeur_source_information" character varying(255),
    "religion" character varying(255),
    "notes_provenance" character varying(255),
    "editions_modernes" character varying(255),
    CONSTRAINT "editions_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "editions_references_externes";
CREATE TABLE "public"."editions_references_externes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "description_reference" character varying(255),
    "editions" uuid,
    "references_externes" uuid,
    CONSTRAINT "editions_references_externes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "references_externes";
CREATE TABLE "public"."references_externes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "titre" character varying(255),
    "annee" character varying(255),
    "editeur" character varying(255),
    "auteur" character varying(255),
    "lien" character varying(255),
    CONSTRAINT "references_externes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "textes_publies";
CREATE TABLE "public"."textes_publies" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "provenance" character varying(255),
    "groupe_texte" character varying(255),
    "nature_texte" character varying(255),
    "titre" character varying(255),
    "sur_l_air_de" character varying(255),
    "incipit" character varying(255),
    "incipit_normalise" character varying(255),
    "deux_premiers_vers_premier_couplet" character varying(255),
    "deux_premiers_vers_premier_couplet_normalises" character varying(255),
    "refrain" character varying(255),
    "refrain_normalise" character varying(255),
    "variante" character varying(255),
    "variante_normalise" character varying(255),
    "auteur" character varying(255),
    "auteur_statut_source" character varying(255),
    "auteur_source_information" character varying(255),
    "page" character varying(255),
    "lien_web_visualisation" character varying(255),
    "contenu_analytique" character varying(255),
    "contenu_texte" character varying(255),
    "forme_poetique" character varying(255),
    "notes_forme_poetique" character varying(255),
    "numero_d_ordre" character varying(255),
    "edition" uuid,
    CONSTRAINT "textes_publies_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "textes_publies_references_externes";
CREATE TABLE "public"."textes_publies_references_externes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "description_reference" character varying(255),
    "references_externes" uuid,
    "textes_publies" uuid,
    CONSTRAINT "textes_publies_references_externes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "textes_publies_themes";
CREATE TABLE "public"."textes_publies_themes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "themes" uuid,
    "textes_publies" uuid,
    CONSTRAINT "textes_publies_themes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "themes";
CREATE TABLE "public"."themes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "theme" character varying(255),
    "type" character varying(255),
    CONSTRAINT "themes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "timbres";
CREATE TABLE "public"."timbres" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "textes_publies" uuid,
    "airs" uuid,
    "enregistrement_web" character varying(255),
    "enregistrement_sherlock" character varying(255),
    CONSTRAINT "timbres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "timbres" ("id", "status", "sort", "user_created", "date_created", "user_updated", "date_updated", "textes_publies", "airs", "enregistrement_web", "enregistrement_sherlock") VALUES
('1205dc83-2b06-4f97-a8d1-f89bb7a26eb3',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:30.084+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:46.676+00',	'30e7a3a6-08e3-4f9d-a6da-bb22c6d65155',	'188e1264-ef9b-4712-ba23-2ae01f208174',	'',	''),
('2cf3e80f-dbe9-463a-ad61-8b86051c1a26',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:30.247+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:46.963+00',	'e11f0b00-dfbd-4a6c-9731-d836a6933496',	'da5ef440-0654-4243-9fa7-3569c6b6022e',	'',	''),
('45d8ca6d-978b-44c5-bb48-637a2a8d5187',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:30.395+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:47.232+00',	'204c8060-98bc-444b-a88d-14e9caaf5c49',	'b9e2574d-4e10-4f8a-a04f-267275d32a56',	'',	''),
('f167823a-8753-43ea-b403-fa2481d85a6d',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:30.551+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:47.483+00',	'a9cc9e03-3f17-4dfd-8d7c-93a54ebe4729',	'73f611d7-8e4b-470b-afa3-212765670bbf',	'',	''),
('634530af-067e-4aaa-90f5-a5baac53f75e',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:30.742+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:47.746+00',	'637c6f6c-7f95-4c7b-8fa9-045631c15ae9',	'02202b7f-1d34-4ec0-adac-ca233b3ccd48',	'',	''),
('4319ae27-2d3f-4715-8b0e-5f7a9ab8b22f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.035+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:48.251+00',	'8b821a16-4578-4a9e-912a-44ed990989af',	'58bc3066-26dc-4703-a2eb-b36b644a8042',	'',	''),
('704642e0-cd5f-4013-a83f-50499ef20d1a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.191+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:48.494+00',	'21ad17ab-fb3a-4f23-8138-d1ee17bfe313',	'b4dedc8c-55d5-457a-a99d-b803032a68d3',	'',	''),
('7dca2cf5-8387-4987-bd46-2a04535d7b12',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.363+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:48.768+00',	'0cfd637f-d9a3-4a19-bf7a-e9b622f8b6ff',	'5f74d3a2-7b80-4f6d-94ec-566be66e9d2d',	'',	''),
('a87ba729-2965-4277-8086-7391699c5393',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.521+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:49.038+00',	'c397c722-b637-461d-8ebb-fd8223e3034d',	'afedfa1e-beb2-45c4-9e9f-0c5f666cb83f',	'',	''),
('da3410fd-90a2-4ab3-8356-7e5a7b35f385',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.83+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:49.591+00',	'ad8e4eaf-54ec-4392-aed6-43a5fb0631c1',	'8422a61d-e0fc-4f90-81bd-cb17240c781b',	'',	''),
('c9f2e77e-1e13-441a-8c9d-717517092b83',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.994+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:49.87+00',	'ea2fb02d-86b7-4949-b634-59e3bc0a23ce',	'94b5f12b-fa1c-4786-8663-9a53db39bfdd',	'',	''),
('70df1d1e-c115-4fdb-b9a3-6a7379e4397d',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:32.146+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:50.134+00',	'5b5b8359-bb1c-42c5-9090-6be8e19fa252',	'edf762c7-0d5b-473f-9738-1a9157304c9a',	'',	''),
('523b2536-3ab5-477c-87f3-4994c11c148a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:32.3+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:50.465+00',	'f87ee0b5-7d74-41fe-a672-48e16595da58',	'6d3ccf7b-f648-4176-83ed-31f72ab52569',	'',	''),
('e507f7b0-35a0-4387-b20a-4c29eba3737f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:32.579+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:51.058+00',	'a1d3f6ac-a36e-43df-a58a-0c36a2e2d17d',	'7175a8b0-1c8d-4172-a090-47bcfe38abc5',	'',	''),
('f03c944d-f5c2-4289-8b50-f5b63f9221ee',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:32.711+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:51.363+00',	'95517d97-0907-4117-8d1d-e89f0cfcc69b',	'104e39fd-7fcc-46b0-9694-3af828f437de',	'',	''),
('aa1b03d7-2b0e-4650-9fc0-58a395536d4b',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:32.839+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:51.643+00',	'd31f1267-85cf-4d7a-9223-533d3a3044e8',	'1e32e8a7-c3ca-4b5a-b9e6-a987cb7f2c6b',	'',	''),
('e7a433d2-aae7-4d4f-9a1d-918b0cb43bad',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.009+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:51.934+00',	'50872b95-8a5b-4637-8988-631edac0c774',	'2ba26db6-657a-40ef-8df8-3172de54785a',	'',	''),
('f7807778-d23b-4368-b12d-74a3bcc5e302',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.141+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:52.229+00',	'91a57167-9b1b-4015-a6c5-31b2d4174212',	'6c9c3a69-72b2-40bf-a125-b267c0bc4da8',	'',	''),
('643dce85-a008-4d2d-8361-2b6927cd7e93',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.438+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:52.766+00',	'8fc54478-6485-447c-a078-75715d8a395f',	'a9399fa2-689c-46cb-8a55-d701016f18c4',	'',	''),
('8f3531cc-b3fc-41b8-bf9a-bd169c8256a3',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.601+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:53.258+00',	'e2da2357-89d6-406e-a574-71c9587ae3a7',	'99bf500f-6e29-4481-8d78-5cca42ea00aa',	'',	''),
('37d1600e-8b26-40bb-8fa9-931753f6d487',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.761+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:53.526+00',	'5780b9dd-4cae-4199-aa7f-fa3c8a0a0e5f',	'8b842d8c-9aec-4f36-bb1d-882633195f1b',	'',	''),
('2dba3871-506b-4f8a-aa12-d02a256f805d',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.932+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:53.791+00',	'e6a49a0a-f85c-4bae-920d-4f6d285e0032',	'1a002884-78b2-4e4e-aa12-648a55066485',	'',	''),
('47913125-2048-46f6-9ccd-ed765087bc68',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:34.257+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:54.332+00',	'1827ebbe-22bd-4ebb-b950-ededc345908b',	'57fff004-b2d5-4d64-ac6c-c45f700c7cb2',	'',	''),
('25ff86e7-1cb9-4df5-92e1-574ab94ecae1',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:34.435+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:54.586+00',	'ac0f526d-9afb-4bd6-b788-3303203c047d',	'5ac08457-685e-46db-9b0a-e61de0965c5e',	'',	''),
('507ec509-3675-420b-a2d4-3ee08dc7bb6c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:34.572+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:54.853+00',	'e02c0362-86ce-4158-b172-93319f705b87',	'1e32e8a7-c3ca-4b5a-b9e6-a987cb7f2c6b',	'',	''),
('101e7dd9-996c-45d1-88f4-d3671c5e3cf6',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:34.735+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:55.12+00',	'1b882216-9695-4366-a187-e79a6f77908c',	'b21e5bb9-c8dd-4817-9025-7cde157e713c',	'',	''),
('29cc3367-5132-47fe-960b-000134a91689',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:35.072+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:55.666+00',	'9a11b0e5-f0f4-48c8-8962-822936445ebc',	'a6aa7347-59e8-4f8e-a36f-ac8fe24ff806',	'',	''),
('0108a95d-37e4-40b6-9a7c-a3c00209b8c8',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:35.236+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:55.972+00',	'2d36fbf9-2587-4260-9519-f1c27822c198',	'6353dcda-3862-4ff0-b09d-fdfcf7fdcff9',	'',	''),
('46b04407-ffd4-4266-9b82-2a40202281db',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:35.406+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:56.256+00',	'8d8bfc6f-e49c-4855-9df2-9569b4ca6813',	'983c25ef-6c52-4bd1-a0f5-fb04efbc06ca',	'',	''),
('f6796074-5fdb-4fa1-b945-1640f16f7838',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:35.567+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:56.524+00',	'5e55b1bb-79e3-4cb8-8dc2-78d5aad61e74',	'74dc24bc-7fd7-41f4-82bd-409916ae7ba3',	'',	''),
('b82d6bd5-d4c2-436c-ba3c-ce10d51d4413',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:35.9+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:57.307+00',	'7cbc619e-ba50-4a14-be8a-2141ee50ed55',	'ac17969e-9ae7-461e-a978-fbd74ab2a602',	'',	''),
('9742e02c-06b9-4ef7-94cf-bfc77b1c07bf',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.07+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:57.563+00',	'982e570c-c420-4e25-a18d-7dca9ff5cce3',	'22252483-5b13-4cb7-8d03-eb38b62ec714',	'',	''),
('d86d9df0-8f1f-4f8e-b359-3e18ddd41f44',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.228+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:57.818+00',	'22a07469-7776-4e1b-82e7-caf8812df559',	'343ccde4-d74a-47db-ae28-d7f0d0c7d54a',	'',	''),
('82f39687-c7f4-455a-93d8-37469e67b6f9',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.38+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:58.082+00',	'9e3fed2c-3e85-436a-addc-64c9bf187519',	'4e881e25-e936-4c14-be32-b472a1ffafc4',	'',	''),
('bd5872bb-adc2-4ef6-89fb-da05ac360bdb',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.518+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:58.37+00',	'50ffd1af-b02b-46b6-b460-207d18104ffb',	'6353dcda-3862-4ff0-b09d-fdfcf7fdcff9',	'',	''),
('ace51ef9-baf0-4837-9693-0ea84762f340',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.838+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:58.891+00',	'6595ff45-c86d-4496-897d-1d9d5b9752dc',	'1aa574be-77f6-4382-8f5c-c3ceae19ee61',	'',	''),
('644bb6b4-eac9-450e-97ab-2e0c812f379c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.976+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:59.138+00',	'e7332680-f471-4bb8-a14d-db68c1f485dc',	'4b8dacc6-f7c5-4ef2-af3b-6c988acc0062',	'',	''),
('3533569a-83a8-4bc3-a611-173e22c4c1de',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:37.116+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:59.403+00',	'9f96146b-739c-4d90-a142-681e08a25613',	'07c4bb86-8886-4538-b9a6-96a098f9690d',	'',	''),
('295f82f1-5b17-46cd-8a01-9286c0b67606',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:37.255+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:59.673+00',	'd1352ed3-7940-4cdb-a0d4-9a00e9c830a0',	'ae9d5d75-55b9-42c2-92ff-6514524813cb',	'',	''),
('dd1c53b4-da40-45a7-902a-2cf3b7e1c133',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:37.589+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:00.187+00',	'c4f77ea6-4d9f-4939-b569-55f8c1918259',	'd4868fa4-2fb1-4c55-9f1c-0279b90b291a',	'',	''),
('2918892d-620e-402f-83e8-49ab5c11b853',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:37.755+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:00.493+00',	'9635d466-4bc8-4c78-a661-e0134e8d9153',	'24c39a3a-630c-4d38-b7b2-b9597223f387',	'',	''),
('8074bee6-0c9e-45b9-a672-db14445d417a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:37.899+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:00.755+00',	'99214788-e472-4b88-a504-1c61895d6617',	'1a44cc73-72c4-4b20-a2f4-1ad89a2ca283',	'',	''),
('324a1aab-2a19-4307-9630-48ed26160c82',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:38.051+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:01.013+00',	'a968418b-a8f6-4b01-a7cb-f9dd9afe52f3',	'7867b810-35be-499a-a269-495bdced0c74',	'',	''),
('97b11989-6f40-4c7b-9fe8-e0c6c55f3f5f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:38.382+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:01.628+00',	'61fbad35-4dcb-46a3-9cfc-559af1f9e637',	'b2f3ff7a-2fd0-49bd-9088-8504307a1c4a',	'',	''),
('cbdd12a0-0fbd-4312-8dc6-66f16ada2fdf',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:38.54+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:01.945+00',	'b1265835-c647-4df6-bc4c-6503573e450c',	'f34a9725-51d6-41d8-bfd4-9c9dfc7c1e87',	'',	''),
('ff55578f-3206-475c-a728-4db5d2fdd2f4',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:38.714+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:02.238+00',	'2f0cf734-3c45-4406-874e-d566d472991b',	'f660af0a-04e4-4494-999e-7a9a4ab03e3f',	'',	''),
('4d66c9e8-2804-4a69-af04-cfedcb7a9b9a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:38.869+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:02.531+00',	'72151acd-e7b9-4e0e-bf33-8df6e7fa19ea',	'8140b6b1-ea01-4361-bedc-b4c608e680bf',	'',	''),
('9c64e44f-cdd8-4a6d-8b3b-ba14ff353346',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.018+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:02.814+00',	'05f74002-593f-48df-b66b-bb3ff2700b9d',	'c8c8ace1-1c21-4d24-ba88-b55afd6815d0',	'',	''),
('231c88ed-484f-4f44-b241-c159f66bfb09',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.293+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:03.44+00',	'bcf1f209-fd73-4a2f-871f-acfc9301ca0e',	'0a93d4e6-c93a-4f8d-b6e4-1503051e221e',	'',	''),
('63ecd1d2-96e2-4f0c-9d20-c737a553f439',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:29.415+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:45.584+00',	'd31f1267-85cf-4d7a-9223-533d3a3044e8',	'bd0d7a0b-10e6-4b2b-a148-0c22456f6885',	'',	''),
('e4d8ecc8-d9c0-40ee-8247-b3ffaaa7c60f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:29.59+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:45.851+00',	'a839b3db-aa46-43e6-957a-e2f3f947ab47',	'f3560b59-cc6a-4a42-bd51-31071ec47849',	'',	''),
('14f2da04-5cd2-4112-bfa3-d558131b18ae',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:29.764+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:46.128+00',	'8b821a16-4578-4a9e-912a-44ed990989af',	'82fdde47-02f4-4efc-b766-ac91a3a79175',	'',	''),
('23772259-e50e-4f83-85ec-65c0d5e6d66a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:40.287+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:05.447+00',	'37991c22-16c0-4ff6-8cbc-e2cb92b2212d',	'1aa574be-77f6-4382-8f5c-c3ceae19ee61',	'',	''),
('f9997f9e-f042-4ac2-adbd-6f91bd921746',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:40.453+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:05.791+00',	'37ff3dc0-71d4-414c-bb3b-ba0dc4c3af57',	'1aa574be-77f6-4382-8f5c-c3ceae19ee61',	'',	''),
('729af7bf-36f5-45f6-8db8-779fbcdff756',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:40.601+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:06.33+00',	'90355d88-5d70-4561-9444-1405a0e0b1e4',	'6353dcda-3862-4ff0-b09d-fdfcf7fdcff9',	'',	''),
('1365c038-cbd2-4b99-9f53-d4908f8e7319',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:40.749+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:06.628+00',	'49d54c1f-0299-44ad-bacb-1e75e465cc0b',	'bd68703c-f421-402b-a6fe-c5dda0be31ac',	'',	''),
('50c1ee8e-0091-4372-963c-b5aa136615b6',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:40.893+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:06.902+00',	'c2d0827e-e76b-4f91-a4a8-f858c35d3407',	'99bf500f-6e29-4481-8d78-5cca42ea00aa',	'',	''),
('facb07d5-ec1f-42e7-a2d9-70de7bbca2e9',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:41.214+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:07.446+00',	'b1a99103-2879-4054-8d71-8e0c29978530',	'6fdc4ebf-88d0-4d7b-aaff-330c4893947c',	'',	''),
('a50fefe5-45d5-493c-9afd-e8ccbdad31d3',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:41.4+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:07.723+00',	'2b0580b8-cf5a-4a3f-997a-7fbc801f953e',	'1a344442-b6be-4ffd-8d97-bbd38d8045e1',	'',	''),
('135439f1-3f37-41fe-9129-760cdaae27af',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:41.566+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:07.991+00',	'3d47d8bb-6ff5-4a18-807a-a5caa855d8d6',	'0890eda4-9ea9-49a5-a27a-e60e72f5dac0',	'',	''),
('8df27949-34d3-4068-baa8-ca9a3bd2869b',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:41.741+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:08.265+00',	'444ee1f5-df12-458e-88f6-b60c74a33f6d',	'93a712b2-dd19-4083-89ae-f03c3e202a5f',	'',	''),
('674c3162-647b-4234-9366-50aa782f420d',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.061+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:08.805+00',	'cf081ebe-aa93-4937-97d3-cfc02e1dac48',	'b21e5bb9-c8dd-4817-9025-7cde157e713c',	'',	''),
('b97490ea-2dc7-4825-8a53-3500ca44c798',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.225+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:09.078+00',	'db6c3aa4-f8ee-4afe-9230-d288be57b567',	'dbe083ee-0102-4d04-8835-5b04b36e6654',	'',	''),
('2dcdcb53-06c0-408e-b4af-43fa3e2cd725',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.385+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:09.357+00',	'f0979230-4827-460b-8c67-f53671b87fe1',	'6353dcda-3862-4ff0-b09d-fdfcf7fdcff9',	'',	''),
('bf84c260-4c8c-4913-b27e-6931c76be3f8',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.547+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:09.615+00',	'c6c66b66-b098-4cba-ad06-3aba7a88b69a',	'983c25ef-6c52-4bd1-a0f5-fb04efbc06ca',	'',	''),
('33189dfb-5ac5-466f-8a1d-db648b1d83f2',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.837+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:10.42+00',	'8d6665c1-03a2-4e02-8a8c-c6760ad805ed',	'57fff004-b2d5-4d64-ac6c-c45f700c7cb2',	'',	''),
('53f207c3-01ae-48da-b7ac-db5652ab312b',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.984+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:10.69+00',	'7cb49a59-5523-4753-b33d-2cdf0e6053ca',	'22252483-5b13-4cb7-8d03-eb38b62ec714',	'',	''),
('06ad913b-c8c7-455f-9719-23a00aa0015c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:43.142+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:11.002+00',	'f43c05ea-71e1-41f4-a080-7758908338f2',	'343ccde4-d74a-47db-ae28-d7f0d0c7d54a',	'',	''),
('ca4504a3-e33a-40d2-9517-18c9962bd6f2',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:43.302+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:11.361+00',	'a73328c7-1737-461e-9bd3-dc3b4021405a',	'4e881e25-e936-4c14-be32-b472a1ffafc4',	'',	''),
('4cf0375d-b63b-449d-aef6-3201d11b7d8c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:43.447+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:11.651+00',	'e6884752-a953-4f35-b780-30d95caf5fec',	'4b8dacc6-f7c5-4ef2-af3b-6c988acc0062',	'',	''),
('bf5efe59-3dba-4bbe-b2c7-f936774c344a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:43.717+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:12.252+00',	'2c96522c-4d79-47db-9659-0662fc04f7d6',	'07c4bb86-8886-4538-b9a6-96a098f9690d',	'',	''),
('9a1df91b-c86d-4704-a97d-c6eadaef59fb',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:43.892+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:12.514+00',	'4150e53d-6406-4067-9eff-a47251ab9608',	'ae9d5d75-55b9-42c2-92ff-6514524813cb',	'',	''),
('15049f3e-c36f-484f-aafb-c2b0bcbd0eed',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.048+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:12.78+00',	'dbd4d80b-6da5-4be8-9b35-e663f20d4234',	'7e6a7a9c-afb1-4b6a-9584-779120825cf1',	'',	''),
('107e0d9e-c511-46c2-83eb-15ef40edebe2',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.195+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:13.051+00',	'6a4e5866-40e9-4c9d-be40-551bd62d10eb',	'd4868fa4-2fb1-4c55-9f1c-0279b90b291a',	'',	''),
('1541fadd-5249-4df6-8043-5376c6b5d14f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.498+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:13.683+00',	'0d3b432c-c34a-4b2e-a745-1542b57d2630',	'1a44cc73-72c4-4b20-a2f4-1ad89a2ca283',	'',	''),
('5ab236da-08ce-40a9-9697-4df05267d4ab',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.655+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:13.981+00',	'452cf3d7-5d6f-4d68-b42a-d39170fc65f5',	'7867b810-35be-499a-a269-495bdced0c74',	'',	''),
('da1ef892-656b-47ec-ae41-51ed2771ed37',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.787+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:14.27+00',	'1b71174e-d0ff-4900-b872-8f28e6466cc3',	'6d0ced04-43dc-41ef-8501-0034b4875ac6',	'',	''),
('dca14069-b02a-4b8f-9200-1b2ae43d81e9',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.92+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:14.528+00',	'9c5acc82-62e7-4089-980c-cba261102aa5',	'cbdabc3b-bac9-4918-bddc-8ecd94b22064',	'',	''),
('c4622dfd-ad91-4a9d-a450-d763fd29d0be',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:45.231+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:15.092+00',	'01e0e5ae-c919-4fcc-ad4c-103d5d64d2c3',	'b2f3ff7a-2fd0-49bd-9088-8504307a1c4a',	'',	''),
('5555b3db-053e-4256-a64c-91e4463c369f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:45.395+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:15.409+00',	'926607ed-f9c1-4959-9de0-63678bc42b97',	'f34a9725-51d6-41d8-bfd4-9c9dfc7c1e87',	'',	''),
('6b88d13c-8748-49ba-8155-cfad7bcb1f0c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:45.55+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:16.317+00',	'36b85df9-e6f3-4994-b9e2-2ba40625bc18',	'f660af0a-04e4-4494-999e-7a9a4ab03e3f',	'',	''),
('4f07805c-d7e1-4c25-8fd9-9410daaea13f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:45.721+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:17.013+00',	'cd917df1-d019-455b-ab3c-b754cc66b15b',	'8140b6b1-ea01-4361-bedc-b4c608e680bf',	'',	''),
('789459f8-efc2-433c-8eee-be35b704c901',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:46.023+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:19.703+00',	'a7f7bfc5-94ca-4d47-84ed-0fea70a30279',	'9680d03c-4b60-4ed6-b591-afed1a8fae09',	'',	''),
('2735d4d5-59df-46f5-b2ad-bd11afa0d42d',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:46.189+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:20.529+00',	'515489d0-8f48-4484-bbff-f0a0d20009c0',	'1e32e8a7-c3ca-4b5a-b9e6-a987cb7f2c6b',	'',	''),
('49705de9-57c0-41f9-b7e4-67d833b37096',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:46.354+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:20.792+00',	'c2cd2c61-6a72-4349-8174-048307d1b4fe',	'778aaa51-6be4-4d78-8b72-361c135f4eb1',	'',	''),
('60e7a33c-4718-4a2f-9b77-9870ce5370ff',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:46.543+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:21.059+00',	'e3a1a891-ac64-4ee8-8d41-0177063a363f',	'd48043ab-cd5a-4c77-9f0b-6ef34552ccfe',	'',	''),
('04228967-9f88-4726-9cd5-f64dc5b4c1e6',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:46.718+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:21.323+00',	'e659c1c2-65a1-4815-9930-7d9683cd06ff',	'b21e5bb9-c8dd-4817-9025-7cde157e713c',	'',	''),
('61177ed6-f0b3-4049-8d64-b9d40fd6a2d1',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.042+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:21.865+00',	'61acf1dd-2b40-469a-b425-46504f42c44f',	'dbe083ee-0102-4d04-8835-5b04b36e6654',	'',	''),
('e0e2afc2-9246-4370-8560-066dc1822ad7',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.196+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:22.132+00',	'f7ffd829-d499-4c2c-a541-e4f71128b829',	'4500088e-da8c-4c00-8a74-b05ede5bff6f',	'',	''),
('775dc799-b288-4fd1-b505-1886ae3da6c7',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.382+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:22.405+00',	'c6a3c523-1083-4546-b3a9-85d8f0845359',	'a6aa7347-59e8-4f8e-a36f-ac8fe24ff806',	'',	''),
('31f1d355-d25c-49fd-ab58-32db14afa263',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.514+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:22.669+00',	'4f3bc0d1-03e4-4870-bd83-2ddb4be264a9',	'f75016a8-9fba-45cb-93f5-9dc9baee6b83',	'',	''),
('711f567d-3e17-48da-a743-2d4a22d228c0',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.795+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:23.189+00',	'c791de2d-a703-4333-affc-20feb807a12f',	'4b8dacc6-f7c5-4ef2-af3b-6c988acc0062',	'',	''),
('7166243e-34af-4724-9f44-fc3e21a45353',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.935+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:23.457+00',	'7d0e768c-3a4a-4156-b6b9-3a8ffce17b12',	'573f285f-16dc-4385-b759-ac8617be203c',	'',	''),
('837bd976-bc86-4f0d-a9d7-b3527525c346',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:48.079+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:23.717+00',	'9987ff9c-23c7-43b2-abd3-b996c3350246',	'd4868fa4-2fb1-4c55-9f1c-0279b90b291a',	'',	''),
('e51db8f8-f172-4255-ad5a-d8a360d93721',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:48.221+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:23.993+00',	'bc724a88-da5e-458b-ba59-1b78bc80ea5d',	'24c39a3a-630c-4d38-b7b2-b9597223f387',	'',	''),
('d723b3d4-7add-49da-a0f7-6e030af2cd6d',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:48.562+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:26.052+00',	'bc43e094-723f-47e7-8d83-10080932fe64',	'c438b2a8-8456-4abd-8f38-ce0267a08b4b',	'',	''),
('ff296c6c-ade3-4337-837a-cdd53b2b578e',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:48.724+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:27.185+00',	'ac9025c2-1ba2-4dea-a10c-c0d9c4e1f61e',	'25d2e346-66ed-4d1a-865b-8dc4f6509f2c',	'',	''),
('bdca0824-5aff-4143-968a-d2c6257ddf3c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:48.872+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:28.113+00',	'e703f643-9858-493d-a535-cd5cf043b798',	'baaeae48-d5fd-4ced-8c0b-418460930160',	'',	''),
('51a685a9-8d6f-47e0-891e-45f6729a8f1e',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.021+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:28.615+00',	'90117c5d-5d3d-48b6-87e4-3dcf95553e42',	'aecd4879-09b0-4b68-9388-21f871093cff',	'',	''),
('6fc6196d-5d77-44e8-8c01-556d9b567649',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.156+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:28.891+00',	'6698a358-02da-48ca-aa9a-7c3d8e62aa19',	'1a44cc73-72c4-4b20-a2f4-1ad89a2ca283',	'',	''),
('30b81e0e-a904-4285-a96d-bd3e48e781b8',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.444+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:29.415+00',	'b4ded9d3-3d4d-4c68-8918-53494e76f482',	'7867b810-35be-499a-a269-495bdced0c74',	'',	''),
('bc7b84e8-4fb2-4274-acf4-8914cd0b0049',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.618+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:04.23+00',	'99739358-6482-414f-9b01-3ab9ac6d9bef',	'56fb40ce-333e-4277-8b82-6e3b2728faaf',	'',	''),
('127ceac6-eb19-468d-97ec-10612e25ae4f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.779+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:04.525+00',	'd5ff7272-ed1c-4973-9a97-555486dee5b8',	'856d4447-6ff2-4290-8efb-f1aa8fc87566',	'',	''),
('8185394f-755e-419a-9aa2-01a83882a682',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.938+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:04.929+00',	'e8084038-92a9-44a5-ae74-61f1afcad12e',	'04ff7564-b5b4-4eb1-83d9-ea5083bad2f9',	'',	''),
('ddb44bbd-f0f6-413d-ae94-da51e43a35f3',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:51.956+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:34.598+00',	'db23c362-99d7-4179-8244-5e5742704a81',	'b2f3ff7a-2fd0-49bd-9088-8504307a1c4a',	'',	''),
('710c26c6-e36c-4c28-8bcb-53242655feb3',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:52.112+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:34.855+00',	'1fd175a7-e4da-4820-9bfa-049f0db43931',	'f34a9725-51d6-41d8-bfd4-9c9dfc7c1e87',	'',	''),
('18b20f21-2c89-41f5-8b99-595e58fd32ea',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:41.911+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:08.526+00',	'fa8006fa-25ee-463f-b6ed-84c1249c3e0b',	'1e32e8a7-c3ca-4b5a-b9e6-a987cb7f2c6b',	'',	''),
('42dc714a-7965-4e97-9681-8a253aa9f373',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:29.231+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:45.328+00',	'a839b3db-aa46-43e6-957a-e2f3f947ab47',	'bd0d7a0b-10e6-4b2b-a148-0c22456f6885',	'',	''),
('d8ef850f-3d63-4856-bd40-93db7edd4c0c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:29.93+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:46.4+00',	'3c772cf3-de32-4612-ba02-38babbf50fd4',	'1a62ccd5-4e5c-44bb-a994-d8a0850889aa',	'',	''),
('0fca2590-cdc5-4400-860a-18a4eaba57d4',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:32.443+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:50.755+00',	'c462a9d6-f5fb-482a-880c-559a66e1ec75',	'9da00325-dc0d-4061-8159-c2898bae6f61',	'',	''),
('a21805ab-1913-450f-8995-f7139919b85b',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:33.288+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:52.5+00',	'7ac4c135-7479-4f64-ac3e-9dada2622aa5',	'0be1e770-e0a3-4253-bb90-2ec8510ef78c',	'',	''),
('be45731d-53d4-489a-bb90-48897fbf2645',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:34.103+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:54.069+00',	'f1f749d7-2b83-4c54-9013-eecc6f0c5b13',	'303dca43-f1ea-42dc-9b57-882ad957aace',	'',	''),
('0863dd1f-842f-4a73-9fae-532defe44f3c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:34.899+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:55.378+00',	'7df92cab-e848-44d9-83c6-4aa936132c43',	'dbe083ee-0102-4d04-8835-5b04b36e6654',	'',	''),
('6157db56-d486-47ea-b9a3-b3d6f3af7726',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:35.726+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:57.032+00',	'60407360-525a-4439-bc6c-27af4c438143',	'a8a5296b-7f2d-44f3-b6d3-a519d5f7dcf8',	'',	''),
('5a07cf63-83ee-49b3-b59f-8257616ee8f8',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:36.679+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:58.636+00',	'c8065315-ae5b-42f6-a095-432f5df301d8',	'cb501c42-6b3a-48fb-a527-a5375687c4b0',	'',	''),
('f4f9fdcc-7318-4d3f-a4d0-d9a46231fa99',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:37.407+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:59.93+00',	'0db2739e-e469-4296-958d-e4395d02ebdf',	'7e6a7a9c-afb1-4b6a-9584-779120825cf1',	'',	''),
('ac1615a8-7032-4c2f-b693-e72c6c61f110',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:38.207+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:01.278+00',	'5b5ffc51-67e2-442f-898e-8318930140a1',	'6d0ced04-43dc-41ef-8501-0034b4875ac6',	'',	''),
('47f75fa5-792c-4468-8c2e-6c6240bf9c8a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.162+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:03.157+00',	'dc4317c9-75f5-449c-8c3c-2d9fe80c773b',	'0cc9d67f-0764-4c12-9e03-f5869beb6c1a',	'',	''),
('0415d85b-0166-4e7a-93a3-de6934a1fb1c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:39.448+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:03.73+00',	'5fa465df-6be2-4473-a427-e092af5abfc9',	'de4b7720-ffb0-493e-9ace-1bf4dddf821f',	'',	''),
('3c2665e8-94ae-4fcd-acf0-27f27f94195a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:40.124+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:05.18+00',	'ec6ff16a-f749-498e-aad0-319a31bb285d',	'502221ea-af37-49cb-9cba-2d7b87e40014',	'',	''),
('2a0be939-cd63-4db8-a969-17aa56c352ed',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:41.06+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:07.182+00',	'8e8a46f7-c0f5-4d2d-bad8-66cf7722364b',	'8b842d8c-9aec-4f36-bb1d-882633195f1b',	'',	''),
('7cb31b60-f14b-494b-8854-0db66da5ec14',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:42.695+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:10.136+00',	'e985407f-198a-49ba-bbb3-d829d571d06b',	'74dc24bc-7fd7-41f4-82bd-409916ae7ba3',	'',	''),
('c2396dde-80d5-4dcc-816d-40455cde3457',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:43.58+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:11.979+00',	'66d30c4f-777d-4540-b0d5-51bf2e0e7e6a',	'573f285f-16dc-4385-b759-ac8617be203c',	'',	''),
('05e54c40-c93d-4dee-9241-890e044e7e57',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:44.351+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:13.313+00',	'e1ac51b2-883f-4811-998c-c7eb48c99b36',	'24c39a3a-630c-4d38-b7b2-b9597223f387',	'',	''),
('12f4110d-5f33-4cb6-b72d-742a06140b2e',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:45.067+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:14.813+00',	'61e22ae5-1977-43ef-8616-78613c7767b5',	'652c9988-d654-4007-a70e-6b10714b2bca',	'',	''),
('cbbfd12b-5ba8-4a85-9886-6e63bb12df8f',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:46.89+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:21.596+00',	'f2966699-d527-4964-9ca9-baf2480d4bc6',	'6f5a4bca-1645-4acf-93c1-8331907a5c75',	'',	''),
('08be2f30-a12a-4893-b151-f4be571c1bb7',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:47.657+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:22.93+00',	'b8c05b7e-3a8e-476b-8932-f2690777e68a',	'6353dcda-3862-4ff0-b09d-fdfcf7fdcff9',	'',	''),
('1bfbf46f-6d84-4c16-808d-5460a1d8f433',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:48.379+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:24.715+00',	'0e14e114-9b1b-4e83-ae80-0047993f68f5',	'9f103926-7a2e-4be0-ab04-5236f834a015',	'',	''),
('5f2486e3-1067-4779-9b10-03b9ebc4f5fa',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.295+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:29.158+00',	'a2083b9e-96b2-4785-b76c-5c035be6f60e',	'e504fb14-8b3c-4b15-a471-e8900b72c146',	'',	''),
('1c1e94bf-50fd-4a31-90ae-d444886dc957',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.592+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:29.686+00',	'26df045d-896e-429f-af58-c9953aa377a6',	'f3560b59-cc6a-4a42-bd51-31071ec47849',	'',	''),
('a93f4a7e-0c8e-46d3-b247-29bd6954088b',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.73+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:29.947+00',	'eafa9c0c-68d9-434b-a4c3-5f71011d5d7b',	'c0cf3ca5-81ab-40e1-b833-8b8544f7f603',	'',	''),
('ff225140-77b2-4fe5-983a-e5049d8b1e06',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:49.888+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:30.415+00',	'75ed2ffe-660b-4883-b394-79d4465fe6c8',	'f8d226a2-3c29-409a-b63a-cda7d0fc6d83',	'',	''),
('82bf9478-0516-42e8-87b3-b854f4bcc153',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:50.033+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:30.675+00',	'1d4ef9ff-95ce-4ede-9258-79f471c46ad5',	'2ba26db6-657a-40ef-8df8-3172de54785a',	'',	''),
('00bb7386-4e6e-4802-be7e-b995560609f3',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:50.341+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:30.932+00',	'2b0f141e-57f8-46cd-a267-6801315ae74c',	'6d0ced04-43dc-41ef-8501-0034b4875ac6',	'',	''),
('2df4804e-481b-4117-9eb8-4c4bc20b3a14',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:50.498+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:31.198+00',	'5c7d0e1f-fabc-4ba6-ab2e-1e7b6aa85d86',	'a65b9809-3af0-4828-a0a5-f9385b56363e',	'',	''),
('013f1c77-8e28-4942-b0ee-778201eafcff',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:50.637+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:31.45+00',	'bbec21b2-1884-4e8a-bea7-1de47c1ff705',	'cbdabc3b-bac9-4918-bddc-8ecd94b22064',	'',	''),
('e6439d6e-93db-474f-b532-97404fe2de79',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:50.829+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:31.698+00',	'39eca1f3-2595-4a86-8116-ddb51d70f55d',	'c172aafe-283f-4db6-950d-5b8da90fced9',	'',	''),
('eebd0466-c257-4531-a1de-18a9597190ec',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:50.964+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:31.974+00',	'262f3fda-90f4-4367-9e0f-042a7114a2c8',	'07c4bb86-8886-4538-b9a6-96a098f9690d',	'',	''),
('db2370e0-90e6-4db9-a36c-88f5300ed63c',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:51.136+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:32.299+00',	'db14498f-1d45-42ad-84ec-7d3c1f0c16e2',	'07c4bb86-8886-4538-b9a6-96a098f9690d',	'',	''),
('52060197-47b5-45bd-971c-9c272f2e7e43',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:51.304+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:33.113+00',	'64dcd2ed-4c7d-4c30-b1bf-9be2d06d32b0',	'9a5812e8-c8cb-40d3-bf56-1d3e9aa54719',	'',	''),
('3ff0e8a2-9b23-4ad0-a67d-32bb1685d059',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:51.469+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:33.713+00',	'98c603a8-f895-4a8f-9b59-437e1e78182a',	'da6aa501-59c1-4478-8c14-ef673c669e58',	'',	''),
('418dcadb-b97a-442f-a910-5d7d017af32a',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:51.644+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:34.041+00',	'6b34abe2-cb17-4319-a1c2-ef4c3e7541d0',	'b1d9eab9-b6d8-452d-91ae-13fcf056e399',	'',	''),
('422d77b8-aeb5-48b0-a179-a5ee6924afa6',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:51.791+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:34.341+00',	'2c3dfda6-cfe2-4a32-853b-25bf613bd7c6',	'e69e1f8f-c5b0-4809-b20e-231c74b7f0df',	'',	''),
('1136759c-b599-4246-90ff-90175ad1d5fa',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:30.889+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:48.005+00',	'8b821a16-4578-4a9e-912a-44ed990989af',	'82fdde47-02f4-4efc-b766-ac91a3a79175',	'',	''),
('f8f7ed23-e537-4196-9af7-8c217acc1597',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:31.676+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:31:49.3+00',	'4a95e8fb-e8c7-4639-a073-22eec11eafc2',	'506d55b6-1493-4390-9c1a-d03de403875c',	'',	''),
('d643a589-6682-4226-abf3-40765496ca6b',	'draft',	NULL,	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-05-14 10:35:45.871+00',	'5aa9f9a0-59c6-436d-bcb1-569cf4c3edf8',	'2021-07-11 21:32:17.966+00',	'0ad35ca7-3de4-4d78-b6f7-fcdd81966405',	'b570d002-894b-48c7-b9e9-8f1dd0728fbf',	'',	'');

ALTER TABLE ONLY "public"."airs" ADD CONSTRAINT "airs_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."airs" ADD CONSTRAINT "airs_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."airs_references_externes" ADD CONSTRAINT "airs_references_externes_airs_foreign" FOREIGN KEY (airs) REFERENCES airs(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."airs_references_externes" ADD CONSTRAINT "airs_references_externes_references_externes_foreign" FOREIGN KEY (references_externes) REFERENCES references_externes(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."airs_references_externes" ADD CONSTRAINT "airs_references_externes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."airs_references_externes" ADD CONSTRAINT "airs_references_externes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_collections" ADD CONSTRAINT "directus_collections_group_foreign" FOREIGN KEY ("group") REFERENCES directus_collections(collection) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_dashboards" ADD CONSTRAINT "directus_dashboards_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_files" ADD CONSTRAINT "directus_files_folder_foreign" FOREIGN KEY (folder) REFERENCES directus_folders(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_files" ADD CONSTRAINT "directus_files_modified_by_foreign" FOREIGN KEY (modified_by) REFERENCES directus_users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_files" ADD CONSTRAINT "directus_files_uploaded_by_foreign" FOREIGN KEY (uploaded_by) REFERENCES directus_users(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_folders" ADD CONSTRAINT "directus_folders_parent_foreign" FOREIGN KEY (parent) REFERENCES directus_folders(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_panels" ADD CONSTRAINT "directus_panels_dashboard_foreign" FOREIGN KEY (dashboard) REFERENCES directus_dashboards(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_panels" ADD CONSTRAINT "directus_panels_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_permissions" ADD CONSTRAINT "directus_permissions_role_foreign" FOREIGN KEY (role) REFERENCES directus_roles(id) ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_presets" ADD CONSTRAINT "directus_presets_role_foreign" FOREIGN KEY (role) REFERENCES directus_roles(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_presets" ADD CONSTRAINT "directus_presets_user_foreign" FOREIGN KEY ("user") REFERENCES directus_users(id) ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_revisions" ADD CONSTRAINT "directus_revisions_activity_foreign" FOREIGN KEY (activity) REFERENCES directus_activity(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_revisions" ADD CONSTRAINT "directus_revisions_parent_foreign" FOREIGN KEY (parent) REFERENCES directus_revisions(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_sessions" ADD CONSTRAINT "directus_sessions_user_foreign" FOREIGN KEY ("user") REFERENCES directus_users(id) ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_project_logo_foreign" FOREIGN KEY (project_logo) REFERENCES directus_files(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_public_background_foreign" FOREIGN KEY (public_background) REFERENCES directus_files(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_public_foreground_foreign" FOREIGN KEY (public_foreground) REFERENCES directus_files(id) ON UPDATE CASCADE ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_storage_default_folder_foreign" FOREIGN KEY (storage_default_folder) REFERENCES directus_folders(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_users" ADD CONSTRAINT "directus_users_role_foreign" FOREIGN KEY (role) REFERENCES directus_roles(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."editions" ADD CONSTRAINT "editions_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."editions" ADD CONSTRAINT "editions_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."editions_references_externes" ADD CONSTRAINT "editions_references_externes_editions_foreign" FOREIGN KEY (editions) REFERENCES editions(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."editions_references_externes" ADD CONSTRAINT "editions_references_externes_references_externes_foreign" FOREIGN KEY (references_externes) REFERENCES references_externes(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."editions_references_externes" ADD CONSTRAINT "editions_references_externes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."editions_references_externes" ADD CONSTRAINT "editions_references_externes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."references_externes" ADD CONSTRAINT "references_externes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."references_externes" ADD CONSTRAINT "references_externes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."textes_publies" ADD CONSTRAINT "textes_publies_edition_foreign" FOREIGN KEY (edition) REFERENCES editions(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies" ADD CONSTRAINT "textes_publies_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies" ADD CONSTRAINT "textes_publies_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."textes_publies_references_externes" ADD CONSTRAINT "textes_publies_references_externes_referen__64dd56db_foreign" FOREIGN KEY (references_externes) REFERENCES references_externes(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies_references_externes" ADD CONSTRAINT "textes_publies_references_externes_textes_publies_foreign" FOREIGN KEY (textes_publies) REFERENCES textes_publies(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies_references_externes" ADD CONSTRAINT "textes_publies_references_externes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies_references_externes" ADD CONSTRAINT "textes_publies_references_externes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."textes_publies_themes" ADD CONSTRAINT "textes_publies_themes_textes_publies_foreign" FOREIGN KEY (textes_publies) REFERENCES textes_publies(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies_themes" ADD CONSTRAINT "textes_publies_themes_themes_foreign" FOREIGN KEY (themes) REFERENCES themes(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies_themes" ADD CONSTRAINT "textes_publies_themes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."textes_publies_themes" ADD CONSTRAINT "textes_publies_themes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."themes" ADD CONSTRAINT "themes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."themes" ADD CONSTRAINT "themes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."timbres" ADD CONSTRAINT "timbres_airs_foreign" FOREIGN KEY (airs) REFERENCES airs(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."timbres" ADD CONSTRAINT "timbres_textes_publies_foreign" FOREIGN KEY (textes_publies) REFERENCES textes_publies(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."timbres" ADD CONSTRAINT "timbres_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."timbres" ADD CONSTRAINT "timbres_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

-- 2022-02-08 14:25:34.709468+00
