-- Adminer 4.8.1 PostgreSQL 13.5 (Debian 13.5-1.pgdg110+1) dump

DROP TABLE IF EXISTS "auteurs_bibliographie";
CREATE TABLE "public"."auteurs_bibliographie" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255),
    "prenom" character varying(255),
    CONSTRAINT "auteurs_bibliographie_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "auteurs_oeuvres";
CREATE TABLE "public"."auteurs_oeuvres" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    "alias" character varying(255),
    "lieu_de_deces" character varying(255),
    "date_de_deces" character varying(255),
    "lieu_de_naissance" character varying(255),
    "date_de_naissance" character varying(255),
    "commentaire" text,
    "lieu_dactivite" character varying(255),
    "date_dactivite" character varying(255),
    CONSTRAINT "auteurs_oeuvres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "auteurs_oeuvres_ecoles";
DROP SEQUENCE IF EXISTS auteurs_oeuvres_ecoles_id_seq;
CREATE SEQUENCE auteurs_oeuvres_ecoles_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."auteurs_oeuvres_ecoles" (
    "id" integer DEFAULT nextval('auteurs_oeuvres_ecoles_id_seq') NOT NULL,
    "auteur_oeuvres_id" uuid,
    "ecole_id" uuid,
    CONSTRAINT "auteurs_oeuvres_ecoles_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "auteurs_oeuvres_periodes";
DROP SEQUENCE IF EXISTS auteurs_oeuvres_periodes_id_seq1;
CREATE SEQUENCE auteurs_oeuvres_periodes_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."auteurs_oeuvres_periodes" (
    "id" integer DEFAULT nextval('auteurs_oeuvres_periodes_id_seq1') NOT NULL,
    "auteur_oeuvres_id" uuid,
    "periode_id" uuid,
    CONSTRAINT "auteurs_oeuvres_periodes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "auteurs_oeuvres_specialites";
DROP SEQUENCE IF EXISTS auteurs_oeuvres_specialites_id_seq1;
CREATE SEQUENCE auteurs_oeuvres_specialites_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."auteurs_oeuvres_specialites" (
    "id" integer DEFAULT nextval('auteurs_oeuvres_specialites_id_seq1') NOT NULL,
    "specialite_id" uuid,
    "auteur_oeuvres_id" uuid,
    CONSTRAINT "auteurs_oeuvres_specialites_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "bibliographie";
CREATE TABLE "public"."bibliographie" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "editeur" character varying(255),
    "nbre_n_de_pages" character varying(255),
    "lieu_de_publication" character varying(255),
    "n_revue_collection" character varying(255),
    "commentaire" text,
    "revue_colloque_collection" text,
    "titre" text,
    CONSTRAINT "bibliographie_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "bibliographie_auteurs_bibliographie";
DROP SEQUENCE IF EXISTS bibliographie_auteurs_bibliographie_id_seq1;
CREATE SEQUENCE bibliographie_auteurs_bibliographie_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."bibliographie_auteurs_bibliographie" (
    "id" integer DEFAULT nextval('bibliographie_auteurs_bibliographie_id_seq1') NOT NULL,
    "auteur_bibliographie_id" uuid,
    "bibliographie_id" uuid,
    CONSTRAINT "bibliographie_auteurs_bibliographie_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "chants";
CREATE TABLE "public"."chants" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255),
    CONSTRAINT "chants_pkey" PRIMARY KEY ("id")
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


DROP TABLE IF EXISTS "directus_notifications";
DROP SEQUENCE IF EXISTS directus_notifications_id_seq;
CREATE SEQUENCE directus_notifications_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."directus_notifications" (
    "id" integer DEFAULT nextval('directus_notifications_id_seq') NOT NULL,
    "timestamp" timestamptz NOT NULL,
    "status" character varying(255) DEFAULT 'inbox',
    "recipient" uuid NOT NULL,
    "sender" uuid NOT NULL,
    "subject" character varying(255) NOT NULL,
    "message" text,
    "collection" character varying(64),
    "item" character varying(255),
    CONSTRAINT "directus_notifications_pkey" PRIMARY KEY ("id")
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
    "project_color" character varying(10) DEFAULT '#00C897',
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
    "email_notifications" boolean DEFAULT true,
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


DROP TABLE IF EXISTS "domaines";
CREATE TABLE "public"."domaines" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    CONSTRAINT "domaines_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "domaines_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "ecoles";
CREATE TABLE "public"."ecoles" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    CONSTRAINT "ecoles_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP VIEW IF EXISTS "geography_columns";
CREATE TABLE "geography_columns" ("f_table_catalog" name, "f_table_schema" name, "f_table_name" name, "f_geography_column" name, "coord_dimension" integer, "srid" integer, "type" text);


DROP VIEW IF EXISTS "geometry_columns";
CREATE TABLE "geometry_columns" ("f_table_catalog" character varying(256), "f_table_schema" name, "f_table_name" name, "f_geometry_column" name, "coord_dimension" integer, "srid" integer, "type" character varying(30));


DROP TABLE IF EXISTS "instruments_de_musique";
CREATE TABLE "public"."instruments_de_musique" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    "parent" uuid,
    CONSTRAINT "instruments_de_musique_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "instruments_de_musique_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "lieux_de_conservation";
CREATE TABLE "public"."lieux_de_conservation" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    "coordonnees_geographiques" geometry(Point,4326),
    CONSTRAINT "lieux_de_conservation_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "lieux_de_conservation_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "notations_musicales";
CREATE TABLE "public"."notations_musicales" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255),
    "parent" uuid,
    CONSTRAINT "notations_musicales_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres";
CREATE TABLE "public"."oeuvres" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "titre" text NOT NULL,
    "titre_alternatif" text,
    "reference_iremus" character varying(255),
    "num_inventaire" character varying(255),
    "cote" character varying(255),
    "inscription" text,
    "technique" text,
    "oeuvre_en_rapport" text,
    "precision_oeuvre" text,
    "precision_instrument" text,
    "commentaire" text,
    "bibliographie" text,
    "reference_agence" text,
    "url" text,
    "diametre" character varying(255),
    "precision_musique" text,
    "source_litteraire" text,
    "date" character varying(255),
    "date_iso" integer,
    "miniature" uuid,
    "hauteur" real,
    "largeur" real,
    CONSTRAINT "oeuvres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_a_la_maniere_de";
DROP SEQUENCE IF EXISTS oeuvres_a_la_maniere_de_id_seq;
CREATE SEQUENCE oeuvres_a_la_maniere_de_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_a_la_maniere_de" (
    "id" integer DEFAULT nextval('oeuvres_a_la_maniere_de_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_a_la_maniere_de_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_anciennes_attributions";
DROP SEQUENCE IF EXISTS oeuvres_anciennes_attributions_id_seq;
CREATE SEQUENCE oeuvres_anciennes_attributions_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_anciennes_attributions" (
    "id" integer DEFAULT nextval('oeuvres_anciennes_attributions_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_anciennes_attributions_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_artistes";
DROP SEQUENCE IF EXISTS oeuvres_artistes_id_seq;
CREATE SEQUENCE oeuvres_artistes_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_artistes" (
    "id" integer DEFAULT nextval('oeuvres_artistes_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_artistes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_ateliers";
DROP SEQUENCE IF EXISTS oeuvres_ateliers_id_seq;
CREATE SEQUENCE oeuvres_ateliers_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_ateliers" (
    "id" integer DEFAULT nextval('oeuvres_ateliers_id_seq') NOT NULL,
    "auteur_oeuvre_id" uuid,
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_ateliers_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_attributions";
DROP SEQUENCE IF EXISTS oeuvres_attributions_id_seq;
CREATE SEQUENCE oeuvres_attributions_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_attributions" (
    "id" integer DEFAULT nextval('oeuvres_attributions_id_seq') NOT NULL,
    "auteur_oeuvre_id" uuid,
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_attributions_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_chants";
DROP SEQUENCE IF EXISTS oeuvres_chants_id_seq1;
CREATE SEQUENCE oeuvres_chants_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_chants" (
    "id" integer DEFAULT nextval('oeuvres_chants_id_seq1') NOT NULL,
    "oeuvre_id" uuid,
    "chant_id" uuid,
    CONSTRAINT "oeuvres_chants_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_copie_dapres";
DROP SEQUENCE IF EXISTS oeuvres_copie_dapres_id_seq;
CREATE SEQUENCE oeuvres_copie_dapres_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_copie_dapres" (
    "id" integer DEFAULT nextval('oeuvres_copie_dapres_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_copie_dapres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_dapres";
DROP SEQUENCE IF EXISTS oeuvres_dapres_id_seq;
CREATE SEQUENCE oeuvres_dapres_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_dapres" (
    "id" integer DEFAULT nextval('oeuvres_dapres_id_seq') NOT NULL,
    "auteur_oeuvre_id" uuid,
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_dapres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_domaines";
DROP SEQUENCE IF EXISTS oeuvres_domaines_id_seq1;
CREATE SEQUENCE oeuvres_domaines_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_domaines" (
    "id" integer DEFAULT nextval('oeuvres_domaines_id_seq1') NOT NULL,
    "domaine_id" uuid,
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_domaines_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_ecoles_auteurs_oeuvres";
DROP SEQUENCE IF EXISTS oeuvres_ecoles_auteurs_oeuvres_id_seq;
CREATE SEQUENCE oeuvres_ecoles_auteurs_oeuvres_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_ecoles_auteurs_oeuvres" (
    "id" integer DEFAULT nextval('oeuvres_ecoles_auteurs_oeuvres_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_ecoles_auteurs_oeuvres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_editeurs";
DROP SEQUENCE IF EXISTS oeuvres_editeurs_id_seq;
CREATE SEQUENCE oeuvres_editeurs_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_editeurs" (
    "id" integer DEFAULT nextval('oeuvres_editeurs_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_editeurs_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_graveurs";
DROP SEQUENCE IF EXISTS oeuvres_graveurs_id_seq;
CREATE SEQUENCE oeuvres_graveurs_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_graveurs" (
    "id" integer DEFAULT nextval('oeuvres_graveurs_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_graveurs_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_images";
DROP SEQUENCE IF EXISTS oeuvres_images_id_seq;
CREATE SEQUENCE oeuvres_images_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_images" (
    "id" integer DEFAULT nextval('oeuvres_images_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "image_id" uuid,
    CONSTRAINT "oeuvres_images_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_instruments_de_musique";
DROP SEQUENCE IF EXISTS oeuvres_instruments_de_musique_id_seq1;
CREATE SEQUENCE oeuvres_instruments_de_musique_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_instruments_de_musique" (
    "id" integer DEFAULT nextval('oeuvres_instruments_de_musique_id_seq1') NOT NULL,
    "oeuvre_id" uuid,
    "instrument_de_musique_id" uuid,
    CONSTRAINT "oeuvres_instruments_de_musique_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_inventeurs";
DROP SEQUENCE IF EXISTS oeuvres_inventeurs_id_seq;
CREATE SEQUENCE oeuvres_inventeurs_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_inventeurs" (
    "id" integer DEFAULT nextval('oeuvres_inventeurs_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "auteur_oeuvre_id" uuid,
    CONSTRAINT "oeuvres_inventeurs_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_lieux_de_conservation";
DROP SEQUENCE IF EXISTS oeuvres_lieux_de_conservation_id_seq1;
CREATE SEQUENCE oeuvres_lieux_de_conservation_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_lieux_de_conservation" (
    "id" integer DEFAULT nextval('oeuvres_lieux_de_conservation_id_seq1') NOT NULL,
    "lieu_de_conservation_id" uuid,
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_lieux_de_conservation_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_lyriques";
CREATE TABLE "public"."oeuvres_lyriques" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "titre" character varying(255) NOT NULL,
    "date_oeuvre" character varying(255),
    "commentaire" text,
    "type" uuid,
    CONSTRAINT "oeuvres_lyriques_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_lyriques_compositeurs";
DROP SEQUENCE IF EXISTS oeuvres_lyriques_compositeurs_id_seq;
CREATE SEQUENCE oeuvres_lyriques_compositeurs_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_lyriques_compositeurs" (
    "id" integer DEFAULT nextval('oeuvres_lyriques_compositeurs_id_seq') NOT NULL,
    "auteur_oeuvres_id" uuid,
    "oeuvre_lyrique_id" uuid,
    CONSTRAINT "oeuvres_lyriques_compositeurs_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_lyriques_librettistes";
DROP SEQUENCE IF EXISTS oeuvres_lyriques_librettistes_id_seq;
CREATE SEQUENCE oeuvres_lyriques_librettistes_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_lyriques_librettistes" (
    "id" integer DEFAULT nextval('oeuvres_lyriques_librettistes_id_seq') NOT NULL,
    "auteur_oeuvres_id" uuid,
    "oeuvre_lyrique_id" uuid,
    CONSTRAINT "oeuvres_lyriques_librettistes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_notations_musicales";
DROP SEQUENCE IF EXISTS oeuvres_notations_musicales_id_seq;
CREATE SEQUENCE oeuvres_notations_musicales_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_notations_musicales" (
    "id" integer DEFAULT nextval('oeuvres_notations_musicales_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "notation_musicale_id" uuid,
    CONSTRAINT "oeuvres_notations_musicales_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_oeuvres_representees";
DROP SEQUENCE IF EXISTS oeuvres_oeuvres_representees_id_seq;
CREATE SEQUENCE oeuvres_oeuvres_representees_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_oeuvres_representees" (
    "id" integer DEFAULT nextval('oeuvres_oeuvres_representees_id_seq') NOT NULL,
    "collection" character varying(255),
    "item" character varying(255),
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_oeuvres_representees_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_themes";
DROP SEQUENCE IF EXISTS oeuvres_themes_id_seq1;
CREATE SEQUENCE oeuvres_themes_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_themes" (
    "id" integer DEFAULT nextval('oeuvres_themes_id_seq1') NOT NULL,
    "theme_id" uuid,
    "oeuvre_id" uuid,
    CONSTRAINT "oeuvres_themes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "oeuvres_voir_aussi";
DROP SEQUENCE IF EXISTS oeuvres_voir_aussi_id_seq;
CREATE SEQUENCE oeuvres_voir_aussi_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."oeuvres_voir_aussi" (
    "id" integer DEFAULT nextval('oeuvres_voir_aussi_id_seq') NOT NULL,
    "oeuvre_id" uuid,
    "voir_aussi_id" uuid,
    CONSTRAINT "oeuvres_voir_aussi_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "periodes";
CREATE TABLE "public"."periodes" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    CONSTRAINT "periodes_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "periodes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP VIEW IF EXISTS "raster_columns";
CREATE TABLE "raster_columns" ("r_table_catalog" name, "r_table_schema" name, "r_table_name" name, "r_raster_column" name, "srid" integer, "scale_x" double precision, "scale_y" double precision, "blocksize_x" integer, "blocksize_y" integer, "same_alignment" boolean, "regular_blocking" boolean, "num_bands" integer, "pixel_types" text[], "nodata_values" double precision[], "out_db" boolean[], "extent" geometry, "spatial_index" boolean);


DROP VIEW IF EXISTS "raster_overviews";
CREATE TABLE "raster_overviews" ("o_table_catalog" name, "o_table_schema" name, "o_table_name" name, "o_raster_column" name, "r_table_catalog" name, "r_table_schema" name, "r_table_name" name, "r_raster_column" name, "overview_factor" integer);


DROP TABLE IF EXISTS "roles";
CREATE TABLE "public"."roles" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    CONSTRAINT "roles_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "roles_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "spatial_ref_sys";
CREATE TABLE "public"."spatial_ref_sys" (
    "srid" integer NOT NULL,
    "auth_name" character varying(256),
    "auth_srid" integer,
    "srtext" character varying(2048),
    "proj4text" character varying(2048),
    CONSTRAINT "spatial_ref_sys_pkey" PRIMARY KEY ("srid")
) WITH (oids = false);


DROP TABLE IF EXISTS "specialites";
CREATE TABLE "public"."specialites" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    CONSTRAINT "specialites_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "specialites_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "supports";
CREATE TABLE "public"."supports" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255) NOT NULL,
    CONSTRAINT "supports_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "supports_pkey" PRIMARY KEY ("id")
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
    "nom" character varying(255) NOT NULL,
    "parent" uuid,
    CONSTRAINT "themes_nom_unique" UNIQUE ("nom"),
    CONSTRAINT "themes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "types_oeuvres";
CREATE TABLE "public"."types_oeuvres" (
    "id" uuid NOT NULL,
    "status" character varying(255) DEFAULT 'draft' NOT NULL,
    "sort" integer,
    "user_created" uuid,
    "date_created" timestamptz,
    "user_updated" uuid,
    "date_updated" timestamptz,
    "nom" character varying(255),
    CONSTRAINT "types_oeuvres_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "us_gaz";
DROP SEQUENCE IF EXISTS us_gaz_id_seq;
CREATE SEQUENCE us_gaz_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."us_gaz" (
    "id" integer DEFAULT nextval('us_gaz_id_seq') NOT NULL,
    "seq" integer,
    "word" text,
    "stdword" text,
    "token" integer,
    "is_custom" boolean DEFAULT true NOT NULL,
    CONSTRAINT "pk_us_gaz" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "us_lex";
DROP SEQUENCE IF EXISTS us_lex_id_seq;
CREATE SEQUENCE us_lex_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."us_lex" (
    "id" integer DEFAULT nextval('us_lex_id_seq') NOT NULL,
    "seq" integer,
    "word" text,
    "stdword" text,
    "token" integer,
    "is_custom" boolean DEFAULT true NOT NULL,
    CONSTRAINT "pk_us_lex" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "us_rules";
DROP SEQUENCE IF EXISTS us_rules_id_seq;
CREATE SEQUENCE us_rules_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."us_rules" (
    "id" integer DEFAULT nextval('us_rules_id_seq') NOT NULL,
    "rule" text,
    "is_custom" boolean DEFAULT true NOT NULL,
    CONSTRAINT "pk_us_rules" PRIMARY KEY ("id")
) WITH (oids = false);


ALTER TABLE ONLY "public"."auteurs_oeuvres_ecoles" ADD CONSTRAINT "auteurs_oeuvres_ecoles_auteur_oeuvres_id_foreign" FOREIGN KEY (auteur_oeuvres_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."auteurs_oeuvres_ecoles" ADD CONSTRAINT "auteurs_oeuvres_ecoles_ecole_id_foreign" FOREIGN KEY (ecole_id) REFERENCES ecoles(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."auteurs_oeuvres_periodes" ADD CONSTRAINT "auteurs_oeuvres_periodes_auteur_oeuvres_id_foreign" FOREIGN KEY (auteur_oeuvres_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."auteurs_oeuvres_periodes" ADD CONSTRAINT "auteurs_oeuvres_periodes_periode_id_foreign" FOREIGN KEY (periode_id) REFERENCES periodes(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."auteurs_oeuvres_specialites" ADD CONSTRAINT "auteurs_oeuvres_specialites_auteurs_oeuvres_id_foreign" FOREIGN KEY (auteur_oeuvres_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."auteurs_oeuvres_specialites" ADD CONSTRAINT "auteurs_oeuvres_specialites_specialites_id_foreign" FOREIGN KEY (specialite_id) REFERENCES specialites(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."bibliographie_auteurs_bibliographie" ADD CONSTRAINT "bibliographie_auteurs_bibliographie_auteur_biblio__tntkm_foreig" FOREIGN KEY (auteur_bibliographie_id) REFERENCES auteurs_bibliographie(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."bibliographie_auteurs_bibliographie" ADD CONSTRAINT "bibliographie_auteurs_bibliographie_bibliographie_id_foreign" FOREIGN KEY (bibliographie_id) REFERENCES bibliographie(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."chants" ADD CONSTRAINT "chants_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."chants" ADD CONSTRAINT "chants_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_collections" ADD CONSTRAINT "directus_collections_group_foreign" FOREIGN KEY ("group") REFERENCES directus_collections(collection) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_dashboards" ADD CONSTRAINT "directus_dashboards_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_files" ADD CONSTRAINT "directus_files_folder_foreign" FOREIGN KEY (folder) REFERENCES directus_folders(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_files" ADD CONSTRAINT "directus_files_modified_by_foreign" FOREIGN KEY (modified_by) REFERENCES directus_users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_files" ADD CONSTRAINT "directus_files_uploaded_by_foreign" FOREIGN KEY (uploaded_by) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_folders" ADD CONSTRAINT "directus_folders_parent_foreign" FOREIGN KEY (parent) REFERENCES directus_folders(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_notifications" ADD CONSTRAINT "directus_notifications_recipient_foreign" FOREIGN KEY (recipient) REFERENCES directus_users(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_notifications" ADD CONSTRAINT "directus_notifications_sender_foreign" FOREIGN KEY (sender) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_panels" ADD CONSTRAINT "directus_panels_dashboard_foreign" FOREIGN KEY (dashboard) REFERENCES directus_dashboards(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_panels" ADD CONSTRAINT "directus_panels_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_permissions" ADD CONSTRAINT "directus_permissions_role_foreign" FOREIGN KEY (role) REFERENCES directus_roles(id) ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_presets" ADD CONSTRAINT "directus_presets_role_foreign" FOREIGN KEY (role) REFERENCES directus_roles(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_presets" ADD CONSTRAINT "directus_presets_user_foreign" FOREIGN KEY ("user") REFERENCES directus_users(id) ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_revisions" ADD CONSTRAINT "directus_revisions_activity_foreign" FOREIGN KEY (activity) REFERENCES directus_activity(id) ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_revisions" ADD CONSTRAINT "directus_revisions_parent_foreign" FOREIGN KEY (parent) REFERENCES directus_revisions(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_sessions" ADD CONSTRAINT "directus_sessions_user_foreign" FOREIGN KEY ("user") REFERENCES directus_users(id) ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_project_logo_foreign" FOREIGN KEY (project_logo) REFERENCES directus_files(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_public_background_foreign" FOREIGN KEY (public_background) REFERENCES directus_files(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_public_foreground_foreign" FOREIGN KEY (public_foreground) REFERENCES directus_files(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."directus_settings" ADD CONSTRAINT "directus_settings_storage_default_folder_foreign" FOREIGN KEY (storage_default_folder) REFERENCES directus_folders(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."directus_users" ADD CONSTRAINT "directus_users_role_foreign" FOREIGN KEY (role) REFERENCES directus_roles(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."ecoles" ADD CONSTRAINT "ecoles_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."ecoles" ADD CONSTRAINT "ecoles_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."instruments_de_musique" ADD CONSTRAINT "instruments_de_musique_parent_foreign" FOREIGN KEY (parent) REFERENCES instruments_de_musique(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."instruments_de_musique" ADD CONSTRAINT "instruments_de_musique_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."instruments_de_musique" ADD CONSTRAINT "instruments_de_musique_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."notations_musicales" ADD CONSTRAINT "notations_musicales_parent_foreign" FOREIGN KEY (parent) REFERENCES notations_musicales(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."notations_musicales" ADD CONSTRAINT "notations_musicales_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."notations_musicales" ADD CONSTRAINT "notations_musicales_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres" ADD CONSTRAINT "oeuvres_miniature_foreign" FOREIGN KEY (miniature) REFERENCES directus_files(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_a_la_maniere_de" ADD CONSTRAINT "oeuvres_a_la_maniere_de_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_a_la_maniere_de" ADD CONSTRAINT "oeuvres_a_la_maniere_de_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_anciennes_attributions" ADD CONSTRAINT "oeuvres_anciennes_attributions_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_anciennes_attributions" ADD CONSTRAINT "oeuvres_anciennes_attributions_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_artistes" ADD CONSTRAINT "oeuvres_artistes_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_artistes" ADD CONSTRAINT "oeuvres_artistes_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_ateliers" ADD CONSTRAINT "oeuvres_ateliers_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_ateliers" ADD CONSTRAINT "oeuvres_ateliers_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_attributions" ADD CONSTRAINT "oeuvres_attributions_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_attributions" ADD CONSTRAINT "oeuvres_attributions_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_chants" ADD CONSTRAINT "oeuvres_chants_chant_id_foreign" FOREIGN KEY (chant_id) REFERENCES chants(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_chants" ADD CONSTRAINT "oeuvres_chants_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_copie_dapres" ADD CONSTRAINT "oeuvres_copie_dapres_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_copie_dapres" ADD CONSTRAINT "oeuvres_copie_dapres_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_dapres" ADD CONSTRAINT "oeuvres_dapres_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_dapres" ADD CONSTRAINT "oeuvres_dapres_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_domaines" ADD CONSTRAINT "oeuvres_domaines_domaine_id_foreign" FOREIGN KEY (domaine_id) REFERENCES domaines(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_domaines" ADD CONSTRAINT "oeuvres_domaines_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_ecoles_auteurs_oeuvres" ADD CONSTRAINT "oeuvres_ecoles_auteurs_oeuvres_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_ecoles_auteurs_oeuvres" ADD CONSTRAINT "oeuvres_ecoles_auteurs_oeuvres_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_editeurs" ADD CONSTRAINT "oeuvres_editeurs_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_editeurs" ADD CONSTRAINT "oeuvres_editeurs_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_graveurs" ADD CONSTRAINT "oeuvres_graveurs_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_graveurs" ADD CONSTRAINT "oeuvres_graveurs_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_images" ADD CONSTRAINT "oeuvres_images_image_id_foreign" FOREIGN KEY (image_id) REFERENCES directus_files(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_images" ADD CONSTRAINT "oeuvres_images_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_instruments_de_musique" ADD CONSTRAINT "oeuvres_instruments_de_musique_instrument_de_musique_id_foreign" FOREIGN KEY (instrument_de_musique_id) REFERENCES instruments_de_musique(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_instruments_de_musique" ADD CONSTRAINT "oeuvres_instruments_de_musique_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_inventeurs" ADD CONSTRAINT "oeuvres_inventeurs_auteur_oeuvre_id_foreign" FOREIGN KEY (auteur_oeuvre_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_inventeurs" ADD CONSTRAINT "oeuvres_inventeurs_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_lieux_de_conservation" ADD CONSTRAINT "oeuvres_lieux_de_conservation_lieu_de_conservation_id_foreign" FOREIGN KEY (lieu_de_conservation_id) REFERENCES lieux_de_conservation(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_lieux_de_conservation" ADD CONSTRAINT "oeuvres_lieux_de_conservation_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_lyriques" ADD CONSTRAINT "oeuvres_lyriques_type_foreign" FOREIGN KEY (type) REFERENCES types_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_lyriques_compositeurs" ADD CONSTRAINT "oeuvres_lyriques_compositeurs_auteur_oeuvres_id_foreign" FOREIGN KEY (auteur_oeuvres_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_lyriques_compositeurs" ADD CONSTRAINT "oeuvres_lyriques_compositeurs_oeuvre_lyrique_id_foreign" FOREIGN KEY (oeuvre_lyrique_id) REFERENCES oeuvres_lyriques(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_lyriques_librettistes" ADD CONSTRAINT "oeuvres_lyriques_librettistes_auteur_oeuvres_id_foreign" FOREIGN KEY (auteur_oeuvres_id) REFERENCES auteurs_oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_lyriques_librettistes" ADD CONSTRAINT "oeuvres_lyriques_librettistes_oeuvre_lyrique_id_foreign" FOREIGN KEY (oeuvre_lyrique_id) REFERENCES oeuvres_lyriques(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_notations_musicales" ADD CONSTRAINT "oeuvres_notations_musicales_notation_musicale_id_foreign" FOREIGN KEY (notation_musicale_id) REFERENCES notations_musicales(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_notations_musicales" ADD CONSTRAINT "oeuvres_notations_musicales_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_oeuvres_representees" ADD CONSTRAINT "oeuvres_oeuvres_representees_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_themes" ADD CONSTRAINT "oeuvres_themes_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_themes" ADD CONSTRAINT "oeuvres_themes_theme_id_foreign" FOREIGN KEY (theme_id) REFERENCES themes(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."oeuvres_voir_aussi" ADD CONSTRAINT "oeuvres_voir_aussi_oeuvre_id_foreign" FOREIGN KEY (oeuvre_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."oeuvres_voir_aussi" ADD CONSTRAINT "oeuvres_voir_aussi_voir_aussi_id_foreign" FOREIGN KEY (voir_aussi_id) REFERENCES oeuvres(id) ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."themes" ADD CONSTRAINT "themes_parent_foreign" FOREIGN KEY (parent) REFERENCES themes(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."themes" ADD CONSTRAINT "themes_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."themes" ADD CONSTRAINT "themes_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."types_oeuvres" ADD CONSTRAINT "types_oeuvres_user_created_foreign" FOREIGN KEY (user_created) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."types_oeuvres" ADD CONSTRAINT "types_oeuvres_user_updated_foreign" FOREIGN KEY (user_updated) REFERENCES directus_users(id) ON DELETE SET NULL NOT DEFERRABLE;

DROP TABLE IF EXISTS "geography_columns";
CREATE VIEW "geography_columns" AS SELECT current_database() AS f_table_catalog,
    n.nspname AS f_table_schema,
    c.relname AS f_table_name,
    a.attname AS f_geography_column,
    postgis_typmod_dims(a.atttypmod) AS coord_dimension,
    postgis_typmod_srid(a.atttypmod) AS srid,
    postgis_typmod_type(a.atttypmod) AS type
   FROM pg_class c,
    pg_attribute a,
    pg_type t,
    pg_namespace n
  WHERE ((t.typname = 'geography'::name) AND (a.attisdropped = false) AND (a.atttypid = t.oid) AND (a.attrelid = c.oid) AND (c.relnamespace = n.oid) AND (c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND (NOT pg_is_other_temp_schema(c.relnamespace)) AND has_table_privilege(c.oid, 'SELECT'::text));

DROP TABLE IF EXISTS "geometry_columns";
CREATE VIEW "geometry_columns" AS SELECT (current_database())::character varying(256) AS f_table_catalog,
    n.nspname AS f_table_schema,
    c.relname AS f_table_name,
    a.attname AS f_geometry_column,
    COALESCE(postgis_typmod_dims(a.atttypmod), sn.ndims, 2) AS coord_dimension,
    COALESCE(NULLIF(postgis_typmod_srid(a.atttypmod), 0), sr.srid, 0) AS srid,
    (replace(replace(COALESCE(NULLIF(upper(postgis_typmod_type(a.atttypmod)), 'GEOMETRY'::text), st.type, 'GEOMETRY'::text), 'ZM'::text, ''::text), 'Z'::text, ''::text))::character varying(30) AS type
   FROM ((((((pg_class c
     JOIN pg_attribute a ON (((a.attrelid = c.oid) AND (NOT a.attisdropped))))
     JOIN pg_namespace n ON ((c.relnamespace = n.oid)))
     JOIN pg_type t ON ((a.atttypid = t.oid)))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            replace(split_part(s.consrc, ''''::text, 2), ')'::text, ''::text) AS type
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE (s.consrc ~~* '%geometrytype(% = %'::text)) st ON (((st.connamespace = n.oid) AND (st.conrelid = c.oid) AND (a.attnum = ANY (st.conkey)))))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            (replace(split_part(s.consrc, ' = '::text, 2), ')'::text, ''::text))::integer AS ndims
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE (s.consrc ~~* '%ndims(% = %'::text)) sn ON (((sn.connamespace = n.oid) AND (sn.conrelid = c.oid) AND (a.attnum = ANY (sn.conkey)))))
     LEFT JOIN ( SELECT s.connamespace,
            s.conrelid,
            s.conkey,
            (replace(replace(split_part(s.consrc, ' = '::text, 2), ')'::text, ''::text), '('::text, ''::text))::integer AS srid
           FROM ( SELECT pg_constraint.connamespace,
                    pg_constraint.conrelid,
                    pg_constraint.conkey,
                    pg_get_constraintdef(pg_constraint.oid) AS consrc
                   FROM pg_constraint) s
          WHERE (s.consrc ~~* '%srid(% = %'::text)) sr ON (((sr.connamespace = n.oid) AND (sr.conrelid = c.oid) AND (a.attnum = ANY (sr.conkey)))))
  WHERE ((c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND (NOT (c.relname = 'raster_columns'::name)) AND (t.typname = 'geometry'::name) AND (NOT pg_is_other_temp_schema(c.relnamespace)) AND has_table_privilege(c.oid, 'SELECT'::text));

DROP TABLE IF EXISTS "raster_columns";
CREATE VIEW "raster_columns" AS SELECT current_database() AS r_table_catalog,
    n.nspname AS r_table_schema,
    c.relname AS r_table_name,
    a.attname AS r_raster_column,
    COALESCE(_raster_constraint_info_srid(n.nspname, c.relname, a.attname), ( SELECT st_srid('010100000000000000000000000000000000000000'::geometry) AS st_srid)) AS srid,
    _raster_constraint_info_scale(n.nspname, c.relname, a.attname, 'x'::bpchar) AS scale_x,
    _raster_constraint_info_scale(n.nspname, c.relname, a.attname, 'y'::bpchar) AS scale_y,
    _raster_constraint_info_blocksize(n.nspname, c.relname, a.attname, 'width'::text) AS blocksize_x,
    _raster_constraint_info_blocksize(n.nspname, c.relname, a.attname, 'height'::text) AS blocksize_y,
    COALESCE(_raster_constraint_info_alignment(n.nspname, c.relname, a.attname), false) AS same_alignment,
    COALESCE(_raster_constraint_info_regular_blocking(n.nspname, c.relname, a.attname), false) AS regular_blocking,
    _raster_constraint_info_num_bands(n.nspname, c.relname, a.attname) AS num_bands,
    _raster_constraint_info_pixel_types(n.nspname, c.relname, a.attname) AS pixel_types,
    _raster_constraint_info_nodata_values(n.nspname, c.relname, a.attname) AS nodata_values,
    _raster_constraint_info_out_db(n.nspname, c.relname, a.attname) AS out_db,
    _raster_constraint_info_extent(n.nspname, c.relname, a.attname) AS extent,
    COALESCE(_raster_constraint_info_index(n.nspname, c.relname, a.attname), false) AS spatial_index
   FROM pg_class c,
    pg_attribute a,
    pg_type t,
    pg_namespace n
  WHERE ((t.typname = 'raster'::name) AND (a.attisdropped = false) AND (a.atttypid = t.oid) AND (a.attrelid = c.oid) AND (c.relnamespace = n.oid) AND (c.relkind = ANY (ARRAY['r'::"char", 'v'::"char", 'm'::"char", 'f'::"char", 'p'::"char"])) AND (NOT pg_is_other_temp_schema(c.relnamespace)) AND has_table_privilege(c.oid, 'SELECT'::text));

DROP TABLE IF EXISTS "raster_overviews";
CREATE VIEW "raster_overviews" AS SELECT current_database() AS o_table_catalog,
    n.nspname AS o_table_schema,
    c.relname AS o_table_name,
    a.attname AS o_raster_column,
    current_database() AS r_table_catalog,
    (split_part(split_part(s.consrc, '''::name'::text, 1), ''''::text, 2))::name AS r_table_schema,
    (split_part(split_part(s.consrc, '''::name'::text, 2), ''''::text, 2))::name AS r_table_name,
    (split_part(split_part(s.consrc, '''::name'::text, 3), ''''::text, 2))::name AS r_raster_column,
    (btrim(split_part(s.consrc, ','::text, 2)))::integer AS overview_factor
   FROM pg_class c,
    pg_attribute a,
    pg_type t,
    pg_namespace n,
    ( SELECT pg_constraint.connamespace,
            pg_constraint.conrelid,
            pg_constraint.conkey,
            pg_get_constraintdef(pg_constraint.oid) AS consrc
           FROM pg_constraint) s
  WHERE ((t.typname = 'raster'::name) AND (a.attisdropped = false) AND (a.atttypid = t.oid) AND (a.attrelid = c.oid) AND (c.relnamespace = n.oid) AND ((c.relkind)::text = ANY ((ARRAY['r'::character(1), 'v'::character(1), 'm'::character(1), 'f'::character(1)])::text[])) AND (s.connamespace = n.oid) AND (s.conrelid = c.oid) AND (s.consrc ~~ '%_overview_constraint(%'::text) AND (NOT pg_is_other_temp_schema(c.relnamespace)) AND has_table_privilege(c.oid, 'SELECT'::text));

-- 2022-01-21 10:16:16.168983+00
