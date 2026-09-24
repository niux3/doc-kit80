--
-- PostgreSQL database dump
--

\restrict lkKcOlEsZxCyAmjEwmMVlUK37zd6EcGRqbUKXpNZUR5h1hz6JcHyhFhTFeiXjbu

-- Dumped from database version 17.11 (Debian 17.11-0+deb13u1)
-- Dumped by pg_dump version 17.11 (Debian 17.11-0+deb13u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: renaud
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO renaud;

--
-- Name: documentation_categories; Type: TABLE; Schema: public; Owner: renaud
--

CREATE TABLE public.documentation_categories (
    name character varying NOT NULL,
    description character varying,
    lft integer NOT NULL,
    rgt integer NOT NULL,
    parent_id integer,
    language_id integer,
    id integer NOT NULL
);


ALTER TABLE public.documentation_categories OWNER TO renaud;

--
-- Name: documentation_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: renaud
--

CREATE SEQUENCE public.documentation_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documentation_categories_id_seq OWNER TO renaud;

--
-- Name: documentation_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: renaud
--

ALTER SEQUENCE public.documentation_categories_id_seq OWNED BY public.documentation_categories.id;


--
-- Name: documentation_languages; Type: TABLE; Schema: public; Owner: renaud
--

CREATE TABLE public.documentation_languages (
    name character varying NOT NULL,
    abbr character varying NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.documentation_languages OWNER TO renaud;

--
-- Name: documentation_languages_id_seq; Type: SEQUENCE; Schema: public; Owner: renaud
--

CREATE SEQUENCE public.documentation_languages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documentation_languages_id_seq OWNER TO renaud;

--
-- Name: documentation_languages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: renaud
--

ALTER SEQUENCE public.documentation_languages_id_seq OWNED BY public.documentation_languages.id;


--
-- Name: documentation_posts; Type: TABLE; Schema: public; Owner: renaud
--

CREATE TABLE public.documentation_posts (
    title character varying NOT NULL,
    slug character varying NOT NULL,
    content text NOT NULL,
    online boolean NOT NULL,
    category_id integer,
    language_id integer,
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.documentation_posts OWNER TO renaud;

--
-- Name: documentation_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: renaud
--

CREATE SEQUENCE public.documentation_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documentation_posts_id_seq OWNER TO renaud;

--
-- Name: documentation_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: renaud
--

ALTER SEQUENCE public.documentation_posts_id_seq OWNED BY public.documentation_posts.id;


--
-- Name: registration_users; Type: TABLE; Schema: public; Owner: renaud
--

CREATE TABLE public.registration_users (
    username character varying NOT NULL,
    email character varying NOT NULL,
    is_active boolean NOT NULL,
    id integer NOT NULL,
    firstname character varying,
    lastname character varying,
    hashed_password character varying NOT NULL
);


ALTER TABLE public.registration_users OWNER TO renaud;

--
-- Name: registration_users_id_seq; Type: SEQUENCE; Schema: public; Owner: renaud
--

CREATE SEQUENCE public.registration_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.registration_users_id_seq OWNER TO renaud;

--
-- Name: registration_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: renaud
--

ALTER SEQUENCE public.registration_users_id_seq OWNED BY public.registration_users.id;


--
-- Name: documentation_categories id; Type: DEFAULT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_categories ALTER COLUMN id SET DEFAULT nextval('public.documentation_categories_id_seq'::regclass);


--
-- Name: documentation_languages id; Type: DEFAULT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_languages ALTER COLUMN id SET DEFAULT nextval('public.documentation_languages_id_seq'::regclass);


--
-- Name: documentation_posts id; Type: DEFAULT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_posts ALTER COLUMN id SET DEFAULT nextval('public.documentation_posts_id_seq'::regclass);


--
-- Name: registration_users id; Type: DEFAULT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.registration_users ALTER COLUMN id SET DEFAULT nextval('public.registration_users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: renaud
--

COPY public.alembic_version (version_num) FROM stdin;
d05ae707faa3
\.


--
-- Data for Name: documentation_categories; Type: TABLE DATA; Schema: public; Owner: renaud
--

COPY public.documentation_categories (name, description, lft, rgt, parent_id, language_id, id) FROM stdin;
\.


--
-- Data for Name: documentation_languages; Type: TABLE DATA; Schema: public; Owner: renaud
--

COPY public.documentation_languages (name, abbr, id) FROM stdin;
français	fr	1
english	en	2
\.


--
-- Data for Name: documentation_posts; Type: TABLE DATA; Schema: public; Owner: renaud
--

COPY public.documentation_posts (title, slug, content, online, category_id, language_id, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: registration_users; Type: TABLE DATA; Schema: public; Owner: renaud
--

COPY public.registration_users (username, email, is_active, id, firstname, lastname, hashed_password) FROM stdin;
\.


--
-- Name: documentation_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: renaud
--

SELECT pg_catalog.setval('public.documentation_categories_id_seq', 1, false);


--
-- Name: documentation_languages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: renaud
--

SELECT pg_catalog.setval('public.documentation_languages_id_seq', 2, true);


--
-- Name: documentation_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: renaud
--

SELECT pg_catalog.setval('public.documentation_posts_id_seq', 1, false);


--
-- Name: registration_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: renaud
--

SELECT pg_catalog.setval('public.registration_users_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: documentation_categories documentation_categories_name_key; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_categories
    ADD CONSTRAINT documentation_categories_name_key UNIQUE (name);


--
-- Name: documentation_categories documentation_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_categories
    ADD CONSTRAINT documentation_categories_pkey PRIMARY KEY (id);


--
-- Name: documentation_languages documentation_languages_name_key; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_languages
    ADD CONSTRAINT documentation_languages_name_key UNIQUE (name);


--
-- Name: documentation_languages documentation_languages_pkey; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_languages
    ADD CONSTRAINT documentation_languages_pkey PRIMARY KEY (id);


--
-- Name: documentation_posts documentation_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_posts
    ADD CONSTRAINT documentation_posts_pkey PRIMARY KEY (id);


--
-- Name: documentation_posts documentation_posts_slug_key; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_posts
    ADD CONSTRAINT documentation_posts_slug_key UNIQUE (slug);


--
-- Name: documentation_posts documentation_posts_title_key; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_posts
    ADD CONSTRAINT documentation_posts_title_key UNIQUE (title);


--
-- Name: registration_users registration_users_email_key; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.registration_users
    ADD CONSTRAINT registration_users_email_key UNIQUE (email);


--
-- Name: registration_users registration_users_pkey; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.registration_users
    ADD CONSTRAINT registration_users_pkey PRIMARY KEY (id);


--
-- Name: registration_users registration_users_username_key; Type: CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.registration_users
    ADD CONSTRAINT registration_users_username_key UNIQUE (username);


--
-- Name: ix_documentation_languages_abbr; Type: INDEX; Schema: public; Owner: renaud
--

CREATE INDEX ix_documentation_languages_abbr ON public.documentation_languages USING btree (abbr);


--
-- Name: documentation_categories documentation_categories_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_categories
    ADD CONSTRAINT documentation_categories_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.documentation_languages(id);


--
-- Name: documentation_categories documentation_categories_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_categories
    ADD CONSTRAINT documentation_categories_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.documentation_categories(id);


--
-- Name: documentation_posts documentation_posts_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_posts
    ADD CONSTRAINT documentation_posts_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.documentation_categories(id);


--
-- Name: documentation_posts documentation_posts_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: renaud
--

ALTER TABLE ONLY public.documentation_posts
    ADD CONSTRAINT documentation_posts_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.documentation_languages(id);


--
-- PostgreSQL database dump complete
--

\unrestrict lkKcOlEsZxCyAmjEwmMVlUK37zd6EcGRqbUKXpNZUR5h1hz6JcHyhFhTFeiXjbu

