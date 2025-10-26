--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7
-- Dumped by pg_dump version 13.7

-- Started on 2025-10-26 13:46:22

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- TOC entry 203 (class 1259 OID 57533)
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    location_id integer NOT NULL,
    naziv character varying(150) NOT NULL,
    grad character varying(50),
    drzava character varying(50) DEFAULT 'Hrvatska'::character varying,
    gps_lat numeric(8,5),
    gps_lon numeric(8,5)
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 57531)
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_location_id_seq OWNER TO postgres;

--
-- TOC entry 3017 (class 0 OID 0)
-- Dependencies: 202
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_location_id_seq OWNED BY public.locations.location_id;


--
-- TOC entry 205 (class 1259 OID 57542)
-- Name: machines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.machines (
    machine_id integer NOT NULL,
    location_id integer NOT NULL,
    servicer_id integer,
    model character varying(50) NOT NULL,
    status character varying(20),
    datum_posljednjeg_servisa date,
    broj_porcioniranja_dnevno integer,
    napomena text,
    CONSTRAINT machines_status_check CHECK (((status)::text = ANY ((ARRAY['Ispravna'::character varying, 'Pokvarena'::character varying, 'U servisu'::character varying])::text[])))
);


ALTER TABLE public.machines OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 57540)
-- Name: machines_machine_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.machines_machine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.machines_machine_id_seq OWNER TO postgres;

--
-- TOC entry 3018 (class 0 OID 0)
-- Dependencies: 204
-- Name: machines_machine_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.machines_machine_id_seq OWNED BY public.machines.machine_id;


--
-- TOC entry 201 (class 1259 OID 57525)
-- Name: servicers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servicers (
    servicer_id integer NOT NULL,
    naziv character varying(100) NOT NULL,
    kontakt character varying(30)
);


ALTER TABLE public.servicers OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 57523)
-- Name: servicers_servicer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.servicers_servicer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.servicers_servicer_id_seq OWNER TO postgres;

--
-- TOC entry 3019 (class 0 OID 0)
-- Dependencies: 200
-- Name: servicers_servicer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servicers_servicer_id_seq OWNED BY public.servicers.servicer_id;


--
-- TOC entry 2864 (class 2604 OID 57536)
-- Name: locations location_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN location_id SET DEFAULT nextval('public.locations_location_id_seq'::regclass);


--
-- TOC entry 2866 (class 2604 OID 57545)
-- Name: machines machine_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machines ALTER COLUMN machine_id SET DEFAULT nextval('public.machines_machine_id_seq'::regclass);


--
-- TOC entry 2863 (class 2604 OID 57528)
-- Name: servicers servicer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicers ALTER COLUMN servicer_id SET DEFAULT nextval('public.servicers_servicer_id_seq'::regclass);


--
-- TOC entry 3009 (class 0 OID 57533)
-- Dependencies: 203
-- Data for Name: locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.locations (location_id, naziv, grad, drzava, gps_lat, gps_lon) FROM stdin;
1	McDonald's Zagreb - Jurišićeva	Zagreb	Hrvatska	45.81200	15.97700
2	McDonald's Split - City Center One	Split	Hrvatska	43.51000	16.47800
3	McDonald's Rijeka - ZTC	Rijeka	Hrvatska	45.32700	14.44100
4	McDonald's Osijek - Avenue Mall	Osijek	Hrvatska	45.55200	18.69500
5	McDonald's Varaždin - Supernova	Varaždin	Hrvatska	46.30700	16.33800
6	McDonald's Dubrovnik - Lapad	Dubrovnik	Hrvatska	42.65300	18.08600
7	McDonald's Karlovac - Retail Park	Karlovac	Hrvatska	45.48800	15.54700
8	McDonald's Zadar - Supernova	Zadar	Hrvatska	44.11900	15.25500
9	McDonald's Pula - City Mall	Pula	Hrvatska	44.87000	13.84900
10	McDonald's Sisak - Caprag	Sisak	Hrvatska	45.47700	16.37900
\.


--
-- TOC entry 3011 (class 0 OID 57542)
-- Dependencies: 205
-- Data for Name: machines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.machines (machine_id, location_id, servicer_id, model, status, datum_posljednjeg_servisa, broj_porcioniranja_dnevno, napomena) FROM stdin;
1	1	1	Taylor C602	Ispravna	2025-09-12	180	Redovito održavanje
2	2	2	Taylor C708	Pokvarena	2025-08-28	0	U tijeku narudžba rezervnog dijela
3	3	3	Taylor C606	U servisu	2025-10-10	0	Zamjena kompresora
4	4	1	Taylor C708	Ispravna	2025-09-03	210	Nova mašina
5	5	2	Taylor C706	Pokvarena	2025-07-21	0	Električni kvar – čeka se dijagnostika
6	6	4	Taylor C602	Ispravna	2025-09-30	160	Sve u redu
7	7	1	Taylor C606	U servisu	2025-10-05	0	Kvar na sustavu hlađenja
8	8	2	Taylor C708	Ispravna	2025-09-18	190	Stabilan rad
9	9	4	Taylor C602	Pokvarena	2025-08-15	0	Motor se pregrijava
10	10	1	Taylor C706	Ispravna	2025-10-01	170	Redoviti rad bez problema
\.


--
-- TOC entry 3007 (class 0 OID 57525)
-- Dependencies: 201
-- Data for Name: servicers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servicers (servicer_id, naziv, kontakt) FROM stdin;
1	ServisPlus d.o.o.	+38591222333
2	FrigoTech Servis	+38591555666
3	CoolServis Rijeka	+38591222999
4	Servis Jadran	+38591888777
\.


--
-- TOC entry 3020 (class 0 OID 0)
-- Dependencies: 202
-- Name: locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.locations_location_id_seq', 10, true);


--
-- TOC entry 3021 (class 0 OID 0)
-- Dependencies: 204
-- Name: machines_machine_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.machines_machine_id_seq', 10, true);


--
-- TOC entry 3022 (class 0 OID 0)
-- Dependencies: 200
-- Name: servicers_servicer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.servicers_servicer_id_seq', 4, true);


--
-- TOC entry 2871 (class 2606 OID 57539)
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (location_id);


--
-- TOC entry 2873 (class 2606 OID 57551)
-- Name: machines machines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machines
    ADD CONSTRAINT machines_pkey PRIMARY KEY (machine_id);


--
-- TOC entry 2869 (class 2606 OID 57530)
-- Name: servicers servicers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicers
    ADD CONSTRAINT servicers_pkey PRIMARY KEY (servicer_id);


--
-- TOC entry 2874 (class 2606 OID 57552)
-- Name: machines machines_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machines
    ADD CONSTRAINT machines_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(location_id) ON DELETE CASCADE;


--
-- TOC entry 2875 (class 2606 OID 57557)
-- Name: machines machines_servicer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machines
    ADD CONSTRAINT machines_servicer_id_fkey FOREIGN KEY (servicer_id) REFERENCES public.servicers(servicer_id);


-- Completed on 2025-10-26 13:46:22

--
-- PostgreSQL database dump complete
--

