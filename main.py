 import re
import time
import streamlit as st

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="centered")

st.title("SkillBridge AI")
st.caption("Personalized Career Roadmap Generator & AI-Driven Job Scam Detector")

tab1, tab2 = st.tabs(["🗺️ Career Roadmap Generator", "🛡️ Job Scam Detector"])

# -------------------- TAB 1: CAREER ROADMAP GENERATOR --------------------
DETAILED_ROLES = {
    "full_stack": {
        "keywords": ["full stack", "fullstack", "web dev", "mern", "mean"],
        "title": "Full-Stack Developer",
        "overview": "End-to-end web application development covering responsive frontend UI, RESTful APIs, relational/NoSQL databases, authentication, and deployment.",
        "stack": {
            "Frontend": "HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6+), React, Tailwind CSS",
            "Backend": "Python (FastAPI) or Node.js (Express.js), REST APIs, JWT Auth",
            "Database & Tools": "PostgreSQL / MongoDB, Git, GitHub, Postman, Docker",
        },
        "phases": [
            ("Weeks 1–3: Web & JavaScript Foundations", [
                "**HTML5 & CSS3:** Semantic tags, forms, Flexbox, CSS Grid, and responsive layouts.",
                "**Modern JavaScript:** `let/const`, arrow functions, destructuring, array methods, Promises, `async/await`, and Fetch API.",
                "**Version Control:** Git branching, pull requests, and clean GitHub READMEs.",
                "**Mini Project:** Build a responsive portfolio + an API-powered web app."
            ]),
            ("Weeks 4–6: Frontend Engineering with React", [
                "**React Core:** Components, JSX, props, `useState`, `useEffect`, conditional rendering, and lists.",
                "**Routing & Forms:** React Router, controlled forms, validation, and loading/error states.",
                "**API Integration:** Connecting React UI to backend APIs cleanly.",
                "**Mini Project:** Build a multi-page Task & Expense Tracker with filters."
            ]),
            ("Weeks 7–9: Backend APIs & Database Design", [
                "**Backend Framework:** Build REST APIs in FastAPI or Express.js with validation and status codes.",
                "**Auth & Security:** Password hashing, JWT authentication, protected routes, and `.env` secrets.",
                "**Databases:** Schema design, CRUD queries, and relationships in PostgreSQL or MongoDB.",
                "**Mini Project:** Build a REST API with user authentication and API docs."
            ]),
            ("Weeks 10–12: Full-Stack Capstones & Deployment", [
                "**Capstone 1:** Full-stack web app with frontend, backend, database, and auth.",
                "**Capstone 2:** Interactive dashboard/portal with search, filters, and live deployment.",
                "**Testing & Deployment:** Add API checks, configure environment variables, and deploy live.",
                "**Portfolio Polish:** Add architecture notes, live links, and project outcomes on GitHub."
            ]),
        ],
        "checklist": [
            "JavaScript event loop, closures, promises, and `==` vs `===`.",
            "React hooks rules, state management, and component re-renders.",
            "REST API design, HTTP status codes, and JWT vs session auth.",
            "SQL vs NoSQL trade-offs, joins, and indexing."
        ]
    },
    "frontend": {
        "keywords": ["frontend", "front end", "front-end", "react", "angular", "vue", "html", "css", "javascript"],
        "title": "Frontend Developer",
        "overview": "Building fast, accessible, responsive user interfaces with modern HTML, CSS, JavaScript, and component frameworks.",
        "stack": {
            "Core Web": "HTML5, CSS3, Tailwind CSS, JavaScript (ES6+), TypeScript",
            "Frameworks": "React / Next.js, State Management (Redux/Zustand), React Router",
            "Quality & Tools": "Git, Vite, Chrome DevTools, Accessibility (WCAG), Lighthouse",
        },
        "phases": [
            ("Weeks 1–3: Semantic HTML, Modern CSS & Responsive UI", [
                "**HTML & CSS:** Semantic elements, Flexbox, CSS Grid, animations, and mobile-first breakpoints.",
                "**Tailwind CSS:** Utility-first styling, dark/light themes, and reusable design tokens.",
                "**Mini Project:** Clone a modern SaaS landing page with full mobile responsiveness."
            ]),
            ("Weeks 4–6: Deep JavaScript & Browser APIs", [
                "**Core JS:** Closures, prototypes, `this`, async/await, event delegation, and localStorage.",
                "**DOM & Fetch:** Dynamic rendering, debouncing search inputs, and error handling.",
                "**Mini Project:** Build an interactive E-commerce product filter & cart app in vanilla JS."
            ]),
            ("Weeks 7–9: React & TypeScript Engineering", [
                "**React Hooks:** `useState`, `useEffect`, `useMemo`, `useCallback`, custom hooks, and Context API.",
                "**TypeScript:** Interfaces, typed props, API response types, and reusable UI components.",
                "**Mini Project:** Build a real-time Movie/Crypto explorer with pagination and caching."
            ]),
            ("Weeks 10–12: Performance, Testing & Portfolio", [
                "**Optimization:** Lazy loading, code splitting, image optimization, and Core Web Vitals.",
                "**Capstone Project:** Deploy a polished multi-page React + TypeScript web application.",
                "**Portfolio:** Publish live links, Lighthouse scores, and clean component architecture."
            ]),
        ],
        "checklist": [
            "CSS specificity, box model, Flexbox vs Grid.",
            "Event loop, microtasks vs macrotasks, and debouncing/throttling.",
            "React rendering optimization and state management patterns.",
            "Web accessibility (ARIA) and cross-browser debugging."
        ]
    },
    "backend": {
        "keywords": ["backend", "back end", "back-end", "api", "node", "express", "django", "spring"],
        "title": "Backend Developer",
        "overview": "Designing scalable server-side systems, secure REST/GraphQL APIs, databases, caching, and deployment pipelines.",
        "stack": {
            "Languages & Frameworks": "Python (FastAPI/Django) or Node.js (Express) or Java (Spring Boot)",
            "Databases & Caching": "PostgreSQL, MySQL, MongoDB, Redis",
            "Infra & Security": "JWT/OAuth2, Docker, Nginx, Git, Pytest/Jest",
        },
        "phases": [
            ("Weeks 1–3: Server Fundamentals & Databases", [
                "**HTTP & REST:** Request/response lifecycle, headers, status codes, and RESTful resource modeling.",
                "**Relational Databases:** Normalization, primary/foreign keys, joins, indexes, and transactions.",
                "**Mini Project:** Design a normalized database schema and SQL queries for an order system."
            ]),
            ("Weeks 4–6: Building Production APIs", [
                "**API Development:** Routing, middleware, DTO/Pydantic validation, pagination, and rate limiting.",
                "**Error Handling:** Centralized exception handlers and structured JSON logging.",
                "**Mini Project:** Build a full CRUD Inventory & Order REST API."
            ]),
            ("Weeks 7–9: Authentication, Caching & Async Jobs", [
                "**Security:** Password hashing, JWT access/refresh tokens, RBAC, and SQL injection/XSS prevention.",
                "**Caching & Queues:** Redis caching for hot queries and background task workers.",
                "**Mini Project:** Add role-based auth and Redis caching to your API."
            ]),
            ("Weeks 10–12: Testing, Docker & Deployment", [
                "**Automated Testing:** Unit and API integration tests.",
                "**Docker & Deploy:** Containerize app + database with Docker Compose and deploy live.",
                "**Documentation:** Complete OpenAPI/Swagger specs and architecture diagrams."
            ]),
        ],
        "checklist": [
            "ACID properties, database indexing, and N+1 query resolution.",
            "JWT vs session authentication and refresh token rotation.",
            "Caching strategies (cache-aside) and rate limiting.",
            "Horizontal vs vertical scaling and load balancing basics."
        ]
    },
    "python": {
        "keywords": ["python"],
        "title": "Python Developer",
        "overview": "Backend engineering, automation, API development, data processing, and testing in Python.",
        "stack": {
            "Core Language": "Python 3.11+, OOP, Decorators, Generators, AsyncIO",
            "Frameworks & DB": "FastAPI / Django, SQLAlchemy, PostgreSQL, SQLite",
            "Testing & Tools": "Pytest, Git, Docker, Linux CLI",
        },
        "phases": [
            ("Weeks 1–3: Core Python & Problem Solving", [
                "**Data Structures:** Lists, tuples, sets, dicts, comprehensions, and `collections`.",
                "**OOP & Clean Code:** Classes, inheritance, dunder methods, type hints, exceptions, and `venv`.",
                "**Problem Solving:** Practice strings, arrays, hash maps, and recursion.",
                "**Mini Project:** CLI file organizer and log/CSV report generator."
            ]),
            ("Weeks 4–6: Web APIs & Database Integration", [
                "**FastAPI / Django:** Routes, Pydantic schemas, validation, and dependency injection.",
                "**Database & ORM:** Models, migrations, and CRUD operations with SQLAlchemy.",
                "**Auth & Security:** Token auth, rate limiting, and environment configs.",
                "**Mini Project:** RESTful API with CRUD endpoints and interactive docs."
            ]),
            ("Weeks 7–9: Async, Testing & Automation", [
                "**Async & APIs:** `async/await`, external API calls, and background tasks.",
                "**Testing:** Unit and integration tests using `pytest`.",
                "**Automation:** File/JSON/Excel processing and scheduled scripts.",
                "**Mini Project:** Automated alert or data-sync utility script."
            ]),
            ("Weeks 10–12: Packaging, Deployment & Capstones", [
                "**Containerization:** `Dockerfile` and clean environment setup.",
                "**Capstone Project:** End-to-end Python service or web app deployed live.",
                "**Documentation:** Clear setup steps, usage examples, and README."
            ]),
        ],
        "checklist": [
            "Mutable vs immutable types, memory management, and GIL.",
            "Decorators, generators (`yield`), and context managers.",
            "Sync vs async endpoints and database query optimization.",
            "Writing unit tests and debugging exceptions."
        ]
    },
    "java": {
        "keywords": ["java", "spring boot", "j2ee"],
        "title": "Java Backend Developer",
        "overview": "Enterprise application development using Core Java, Collections, Multithreading, Spring Boot, JPA/Hibernate, and SQL.",
        "stack": {
            "Core Java": "Java 17+, OOP, Collections, Streams API, Multithreading",
            "Spring Ecosystem": "Spring Boot, Spring MVC, Spring Data JPA, Spring Security",
            "Database & Tools": "MySQL / PostgreSQL, Maven/Gradle, Git, Postman, Docker",
        },
        "phases": [
            ("Weeks 1–3: Core Java & OOP Mastery", [
                "**Java Fundamentals:** OOP principles, interfaces, abstract classes, exception handling, and `final/static`.",
                "**Collections & Streams:** `List`, `Set`, `Map`, `Comparable/Comparator`, Lambdas, and Stream API.",
                "**Mini Project:** Console Banking or Library Management System using OOP & Collections."
            ]),
            ("Weeks 4–6: Spring Boot & REST APIs", [
                "**Spring Core:** Dependency Injection, IoC container, annotations, and application properties.",
                "**REST Controllers:** Request mapping, validation (`@Valid`), and global exception handling (`@ControllerAdvice`).",
                "**Mini Project:** Employee/Product Management REST API with Postman collection."
            ]),
            ("Weeks 7–9: Databases, JPA & Security", [
                "**Spring Data JPA:** Entity relationships (`@OneToMany`, `@ManyToMany`), JPQL, and pagination.",
                "**Spring Security:** JWT authentication, password encoding, and role-based endpoints.",
                "**Mini Project:** Secure E-commerce or Hospital Booking backend API."
            ]),
            ("Weeks 10–12: Testing, Microservices Intro & Deployment", [
                "**Testing:** JUnit 5 and Mockito unit tests for service layers.",
                "**Capstone Project:** Deploy a full Spring Boot + SQL project with Docker and Swagger docs."
            ]),
        ],
        "checklist": [
            "JVM memory model (Heap vs Stack), Garbage Collection, and `equals`/`hashCode`.",
            "HashMap internal working and ConcurrentHashMap.",
            "Spring Boot auto-configuration and JPA lazy vs eager loading.",
            "Exception handling and transaction management (`@Transactional`)."
        ]
    },
    "ai_ml": {
        "keywords": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "nlp", "llm", "generative ai", "gen ai"],
        "title": "AI & Machine Learning Engineer",
        "overview": "Building predictive ML models, neural networks, NLP/LLM applications, RAG pipelines, and deploying AI services.",
        "stack": {
            "Programming & Math": "Python, NumPy, Pandas, Linear Algebra, Probability & Statistics",
            "ML & Deep Learning": "Scikit-learn, PyTorch / TensorFlow, Hugging Face",
            "GenAI & Deployment": "LangChain / LlamaIndex, Vector DBs (FAISS/Chroma), FastAPI, Streamlit",
        },
        "phases": [
            ("Weeks 1–3: Python Data Stack & Math Basics", [
                "**Python & Data:** NumPy vectorization, Pandas data manipulation, and Matplotlib visualization.",
                "**Math Foundations:** Vectors/matrices, gradients, probability distributions, and evaluation metrics.",
                "**Mini Project:** Feature engineering & EDA pipeline on a structured dataset."
            ]),
            ("Weeks 4–6: Classical Machine Learning", [
                "**Supervised Learning:** Linear/Logistic Regression, Decision Trees, Random Forests, XGBoost, SVM.",
                "**Model Tuning:** Cross-validation, hyperparameter tuning, overfitting/regularization, and precision/recall.",
                "**Mini Project:** Fraud Detection or House Price Prediction model with full evaluation report."
            ]),
            ("Weeks 7–9: Deep Learning & Generative AI / LLMs", [
                "**Neural Networks:** Backpropagation, CNNs for vision, Transformers, and transfer learning.",
                "**LLM & RAG Apps:** Prompt engineering, embeddings, vector search, and Retrieval-Augmented Generation.",
                "**Mini Project:** Build a PDF/Document Q&A Assistant using embeddings and vector search."
            ]),
            ("Weeks 10–12: Model Deployment & Capstone", [
                "**AI Serving:** Wrap ML/LLM models inside a FastAPI or Streamlit web interface.",
                "**Capstone Project:** Deploy an end-to-end AI application with clear latency/accuracy metrics."
            ]),
        ],
        "checklist": [
            "Bias-variance trade-off, regularization (L1/L2), and cross-validation.",
            "Choosing metrics (ROC-AUC, F1, RMSE) for imbalanced vs balanced data.",
            "How embeddings, attention mechanisms, and RAG pipelines work.",
            "Handling hallucinations, prompt injection, and model drift."
        ]
    },
    "data": {
        "keywords": ["data analyst", "data science", "data scientist", "analytics", "power bi", "tableau", "sql"],
        "title": "Data Analyst / Data Scientist",
        "overview": "Turning raw datasets into actionable business insights using SQL, Python, statistics, BI dashboards, and modeling.",
        "stack": {
            "SQL & Spreadsheets": "SQL (PostgreSQL/MySQL), Advanced Excel (Pivot Tables, XLOOKUP, Power Query)",
            "Python & ML": "Python, Pandas, NumPy, Matplotlib/Seaborn, Scikit-learn",
            "BI & Reporting": "Power BI / Tableau, KPI Design, A/B Testing",
        },
        "phases": [
            ("Weeks 1–3: SQL & Excel Foundations", [
                "**SQL Mastery:** `SELECT`, `WHERE`, `GROUP BY`, `JOIN`s, CTEs, and Window Functions (`ROW_NUMBER`, `RANK`).",
                "**Excel & Stats:** Pivot tables, dynamic formulas, descriptive stats, and hypothesis testing.",
                "**Mini Project:** E-commerce revenue & customer cohort SQL analysis."
            ]),
            ("Weeks 4–6: Python Data Analysis & Visualization", [
                "**Pandas & NumPy:** Handling missing/duplicate data, merges, aggregations, and time-series.",
                "**Visual Storytelling:** Clear charts and outlier analysis with Matplotlib & Seaborn.",
                "**Mini Project:** Clean and analyze a real-world Telecom Churn or Healthcare dataset."
            ]),
            ("Weeks 7–9: BI Dashboards & Predictive Modeling", [
                "**Power BI / Tableau:** Data modeling, DAX measures, slicers, and executive KPI layouts.",
                "**Predictive Basics:** Regression, classification, train/test split, and error metrics.",
                "**Mini Project:** Interactive Sales & Retention Dashboard in Power BI/Tableau."
            ]),
            ("Weeks 10–12: Case Studies & Portfolio", [
                "**Capstone 1:** Full SQL + Python + Dashboard business case study.",
                "**Capstone 2:** Second domain case study with clear business recommendations.",
                "**Portfolio:** Publish clean notebooks, SQL scripts, and dashboard screenshots on GitHub."
            ]),
        ],
        "checklist": [
            "Writing SQL queries with Window Functions and CTEs.",
            "Handling missing values, outliers, and class imbalance.",
            "Defining product KPIs and evaluating A/B test significance.",
            "Explaining business impact clearly from your case studies."
        ]
    },
    "cybersecurity": {
        "keywords": ["cyber", "security", "ethical hacking", "pentest", "soc", "network security", "infosec"],
        "title": "Cybersecurity Analyst / Ethical Hacker",
        "overview": "Protecting networks, web applications, and systems through threat analysis, vulnerability assessment, and defensive monitoring.",
        "stack": {
            "Networking & OS": "TCP/IP, DNS, HTTP/S, Linux CLI, Windows Server, Wireshark",
            "Security Tools": "Nmap, Burp Suite, OWASP ZAP, Metasploit, Splunk / SIEM",
            "Concepts": "OWASP Top 10, Cryptography, IAM, Incident Response",
        },
        "phases": [
            ("Weeks 1–3: Networking & Linux Fundamentals", [
                "**Networking:** OSI/TCP-IP layers, subnetting, ports/protocols, DNS, ARP, and packet inspection in Wireshark.",
                "**Linux & Scripting:** File permissions, processes, bash scripting, and Python basics for automation.",
                "**Lab Goal:** Capture and analyze HTTP/DNS traffic safely in a local lab."
            ]),
            ("Weeks 4–6: Web Security & OWASP Top 10", [
                "**Vulnerabilities:** SQL Injection, XSS, CSRF, IDOR, broken authentication, and security misconfigurations.",
                "**Testing Tools:** Intercepting and analyzing requests in Burp Suite on legal labs (DVWA / PortSwigger).",
                "**Lab Goal:** Complete 15+ hands-on web vulnerability labs with remediation notes."
            ]),
            ("Weeks 7–9: Network Scanning & Defensive Monitoring (SOC)", [
                "**Recon & Scanning:** Host discovery and service enumeration using Nmap.",
                "**Blue Team / SIEM:** Log analysis, detecting brute-force/phishing alerts, and incident triage.",
                "**Lab Goal:** Write a structured vulnerability assessment and incident report."
            ]),
            ("Weeks 10–12: CTF Practice & Portfolio", [
                "**Practice:** Solve beginner-to-intermediate rooms on TryHackMe / Hack The Box.",
                "**Portfolio:** Publish sanitized write-ups, scripts, and hardening checklists on GitHub."
            ]),
        ],
        "checklist": [
            "Explaining TCP 3-way handshake, TLS/HTTPS, and DNS resolution.",
            "How SQLi and XSS happen and exact code fixes to prevent them.",
            "Symmetric vs asymmetric encryption and hashing vs encryption.",
            "Incident response lifecycle (Preparation, Detection, Containment, Recovery)."
        ]
    },
    "cloud_devops": {
        "keywords": ["devops", "cloud", "aws", "azure", "gcp", "kubernetes", "docker", "ci/cd", "sre"],
        "title": "Cloud & DevOps Engineer",
        "overview": "Automating software delivery, container orchestration, cloud infrastructure, CI/CD pipelines, and production monitoring.",
        "stack": {
            "OS & Scripting": "Linux Administration, Bash, Python, Git",
            "Containers & CI/CD": "Docker, Kubernetes, GitHub Actions / Jenkins",
            "Cloud & IaC": "AWS (EC2, S3, IAM, VPC, RDS), Terraform, Prometheus & Grafana",
        },
        "phases": [
            ("Weeks 1–3: Linux, Networking & Git", [
                "**Linux Mastery:** Users/permissions, systemd services, networking (`netstat/ss/curl`), and SSH.",
                "**Scripting:** Bash automation scripts for backups, log rotation, and health checks.",
                "**Mini Project:** Write an automated server health & disk-alert bash script."
            ]),
            ("Weeks 4–6: Docker & CI/CD Pipelines", [
                "**Docker:** Multi-stage Dockerfiles, images, volumes, networks, and Docker Compose.",
                "**CI/CD:** Build automated test, lint, and container build pipelines in GitHub Actions.",
                "**Mini Project:** Containerize a multi-tier web app + database with automated CI checks."
            ]),
            ("Weeks 7–9: Cloud Infrastructure (AWS) & Terraform", [
                "**Cloud Core:** IAM least-privilege policies, VPC subnets/security groups, EC2, S3, and RDS.",
                "**Infrastructure as Code:** Provision cloud resources reproducibly using Terraform.",
                "**Mini Project:** Deploy a web service on AWS using Terraform scripts."
            ]),
            ("Weeks 10–12: Kubernetes & Observability", [
                "**Kubernetes:** Pods, Deployments, Services, ConfigMaps, Secrets, and Ingress.",
                "**Monitoring:** Set up metrics and alerts with Prometheus + Grafana.",
                "**Capstone:** End-to-end CI/CD pipeline deploying a containerized app with monitoring."
            ]),
        ],
        "checklist": [
            "Docker image layers, container networking, and volume persistence.",
            "CI vs CD and zero-downtime deployment strategies (blue/green, canary).",
            "AWS VPC public vs private subnets, NAT gateway, and IAM roles.",
            "Kubernetes Pod lifecycle and debugging `CrashLoopBackOff`."
        ]
    },
    "mobile": {
        "keywords": ["mobile", "android", "ios", "flutter", "react native", "kotlin", "swift", "app dev"],
        "title": "Mobile App Developer",
        "overview": "Building smooth, responsive Android/iOS mobile applications with clean navigation, local storage, APIs, and store readiness.",
        "stack": {
            "Frameworks": "Flutter (Dart) or React Native (TypeScript) or Kotlin (Android)",
            "State & Storage": "Provider/Riverpod or Redux, SQLite / Hive / AsyncStorage",
            "Backend & Tools": "REST APIs, Firebase Auth/Firestore, Git, Android Studio / Xcode",
        },
        "phases": [
            ("Weeks 1–3: Language & Mobile UI Layouts", [
                "**Language Core:** Dart / TypeScript / Kotlin fundamentals, async programming, and null safety.",
                "**Mobile UI:** Responsive layouts, lists, forms, themes, and adaptive screen sizes.",
                "**Mini Project:** Build a clean Habit Tracker or Expense Calculator mobile UI."
            ]),
            ("Weeks 4–6: Navigation, State & Local Persistence", [
                "**Navigation:** Stack, tab, and drawer navigation with passing parameters.",
                "**State & Offline Data:** Managing app state cleanly and saving offline data locally.",
                "**Mini Project:** Offline-first Notes or To-Do app with categories and search."
            ]),
            ("Weeks 7–9: APIs, Auth & Device Features", [
                "**Networking:** Fetching REST APIs, loading spinners, pagination, and error retry states.",
                "**Firebase / Auth:** User login, push notifications, and camera/location permissions.",
                "**Mini Project:** Weather, News, or Job Alert mobile app connected to live APIs."
            ]),
            ("Weeks 10–12: Performance, Testing & Release Build", [
                "**Optimization:** Reducing widget re-renders, image caching, and smooth 60fps scrolling.",
                "**Capstone App:** Complete multi-screen mobile app packaged as a signed APK/AAB with demo video."
            ]),
        ],
        "checklist": [
            "Mobile app lifecycle states (foreground, background, paused).",
            "Managing local vs global state and avoiding unnecessary UI rebuilds.",
            "Handling offline mode, API timeouts, and secure token storage.",
            "App signing, permissions, and Play Store / App Store release steps."
        ]
    },
    "embedded": {
        "keywords": ["embedded", "iot", "ece", "microcontroller", "stm32", "esp32", "arduino", "firmware", "rtos"],
        "title": "Embedded Systems & IoT Engineer",
        "overview": "Firmware development in Embedded C/C++, peripherals, communication protocols, RTOS, and cloud-connected hardware.",
        "stack": {
            "Languages & OS": "Embedded C, C++, Python, FreeRTOS",
            "Hardware & MCUs": "ESP32, STM32 / ARM Cortex-M, Sensors, Multimeter / Logic Analyzer",
            "Protocols & Cloud": "UART, I2C, SPI, CAN, MQTT, HTTP",
        },
        "phases": [
            ("Weeks 1–3: Embedded C & Microcontroller Basics", [
                "**Embedded C:** Pointers, bitwise ops, `volatile`, `const`, `static`, structs, and memory sections.",
                "**Peripherals:** GPIO, timers, PWM, and ADC reading.",
                "**Interrupts:** External/timer interrupts, debouncing, and clean ISR design.",
                "**Mini Project:** PWM controller with sensor/button interrupt handling."
            ]),
            ("Weeks 4–6: Communication Protocols & Sensors", [
                "**UART:** Serial framing, baud rates, ring buffers, and serial debugging.",
                "**I2C & SPI:** Device addressing, bus timing, and sensor/display interfacing.",
                "**Bus Basics:** CAN/serial framing concepts and hardware troubleshooting.",
                "**Mini Project:** Multi-sensor data logger reading I2C/SPI devices."
            ]),
            ("Weeks 7–9: RTOS & Telemetry", [
                "**FreeRTOS:** Tasks, queues, semaphores, and mutexes.",
                "**Connectivity:** Wi-Fi/BLE/MQTT payloads and live monitoring dashboards.",
                "**Mini Project:** Real-time sensor monitor sending telemetry packets."
            ]),
            ("Weeks 10–12: Reliability & Capstone", [
                "**Reliability:** Watchdog timers, low-power modes, and fault recovery.",
                "**Capstone Project:** Complete hardware + firmware system with circuit/block diagrams and demo.",
                "**Documentation:** Pinouts, state machine flow, and test results."
            ]),
        ],
        "checklist": [
            "Role of `volatile` in registers and ISRs.",
            "UART vs I2C vs SPI wiring, speed, and addressing.",
            "Stack overflow causes, memory layout, and interrupt safety.",
            "Mutex vs semaphore in RTOS."
        ]
    },
    "vlsi": {
        "keywords": ["vlsi", "verilog", "systemverilog", "fpga", "asic", "rtl", "digital design", "cmos"],
        "title": "VLSI & RTL Design Engineer",
        "overview": "Digital logic design, Verilog/SystemVerilog RTL coding, simulation/verification, FPGA prototyping, and ASIC flow basics.",
        "stack": {
            "HDLs & Verification": "Verilog, SystemVerilog, UVM Basics, Tcl",
            "EDA & Hardware": "Vivado / Quartus, ModelSim / QuestaSim, GTKWave, FPGA Boards",
            "Core Concepts": "FSMs, Static Timing Analysis (STA), CMOS Logic, Synthesis",
        },
        "phases": [
            ("Weeks 1–3: Digital Electronics & CMOS Foundations", [
                "**Combinational & Sequential:** Muxes, decoders, flip-flops, latches, setup/hold time, and metastability.",
                "**CMOS Basics:** Inverter characteristics, static vs dynamic power, and propagation delay.",
                "**Mini Exercise:** Solve timing analysis problems (slack, max clock frequency)."
            ]),
            ("Weeks 4–6: Verilog RTL Design & FSMs", [
                "**Synthesizable Verilog:** Blocking vs non-blocking assignments, combinational/sequential coding styles, and avoiding unintended latches.",
                "**Finite State Machines:** Mealy vs Moore FSMs, gray counters, and FIFO buffers.",
                "**Mini Project:** Design and simulate a parameterized Synchronous FIFO and Traffic/Sequence FSM."
            ]),
            ("Weeks 7–9: Protocols & Verification Testbenches", [
                "**Bus Protocols:** UART, SPI, and AMBA APB/AXI protocol basics.",
                "**Self-Checking Testbenches:** Writing SystemVerilog testbenches, assertions, and waveform debugging.",
                "**Mini Project:** Design and verify a UART Transmitter/Receiver with testbench."
            ]),
            ("Weeks 10–12: Synthesis, STA & FPGA Capstone", [
                "**Synthesis & Timing:** Understanding synthesis reports, area/power/timing constraints (SDC).",
                "**Capstone Project:** Implement a RISC-V single-cycle core or SPI/APB peripheral on simulator/FPGA."
            ]),
        ],
        "checklist": [
            "Setup time vs hold time violations and how to fix each.",
            "Blocking (`=`) vs non-blocking (`<=`) assignments in Verilog.",
            "Mealy vs Moore state machines and synchronous vs asynchronous reset.",
            "Clock Domain Crossing (CDC) and 2-flip-flop synchronizers."
        ]
    },
    "ui_ux": {
        "keywords": ["ui/ux", "ui ux", "ux", "ui design", "product design", "figma", "graphic design"],
        "title": "UI/UX & Product Designer",
        "overview": "User research, wireframing, visual design systems, interactive prototyping in Figma, and usability testing.",
        "stack": {
            "Design & Prototyping": "Figma, FigJam, Auto Layout, Design Systems, Variables",
            "UX Research": "User Personas, User Flows, Information Architecture, Usability Testing",
            "Principles": "Typography, Color Theory, Spacing/Grids, Accessibility (Contrast)",
        },
        "phases": [
            ("Weeks 1–3: Visual Design Principles & Figma Basics", [
                "**Visual Foundations:** Typography hierarchy, 8pt grid spacing, color contrast, and alignment.",
                "**Figma Mastery:** Frames, Auto Layout, constraints, components, variants, and styles.",
                "**Mini Project:** Redesign 3 screens of a popular mobile app with cleaner hierarchy."
            ]),
            ("Weeks 4–6: UX Research & Information Architecture", [
                "**UX Process:** Problem framing, user interviews, empathy maps, personas, and user journeys.",
                "**Wireframing:** Low-fidelity sketches, sitemaps, and task flows.",
                "**Mini Project:** Create complete user flows and wireframes for a local service or study app."
            ]),
            ("Weeks 7–9: Design Systems & Interactive Prototyping", [
                "**Design Systems:** Reusable buttons, inputs, cards, icons, and responsive web/mobile components.",
                "**Prototyping:** Smart animate, micro-interactions, overlays, and clickable flows.",
                "**Mini Project:** Build a clickable interactive prototype with a mini component library."
            ]),
            ("Weeks 10–12: Usability Testing & Case Studies", [
                "**Testing:** Run usability tests with 5 users, log friction points, and iterate.",
                "**Portfolio Case Studies:** Publish 2 detailed end-to-end UX case studies (Problem → Research → Wireframes → Final UI)."
            ]),
        ],
        "checklist": [
            "Difference between UI and UX with concrete examples.",
            "How you validate a design decision using user feedback/testing.",
            "Accessibility contrast ratios, touch target sizes, and responsive grids.",
            "Walking through a case study trade-off from start to finish."
        ]
    },
    "digital_marketing": {
        "keywords": ["digital marketing", "marketing", "seo", "social media", "content marketing", "ads", "sem"],
        "title": "Digital Marketing Specialist",
        "overview": "Growing traffic, leads, and brand conversions through SEO, content strategy, paid ads, social media, and analytics.",
        "stack": {
            "Organic & Content": "SEO (On-Page, Off-Page, Technical), Keyword Research, Copywriting",
            "Paid & Social": "Google Ads, Meta Ads Manager, Instagram/LinkedIn Marketing, Email Funnels",
            "Analytics": "Google Analytics 4 (GA4), Google Search Console, UTM Tracking",
        },
        "phases": [
            ("Weeks 1–3: Marketing Funnels & Content Copywriting", [
                "**Funnel Strategy:** Awareness, consideration, conversion, and retention stages.",
                "**Copywriting:** Hooks, value propositions, landing page headlines, and clear CTAs.",
                "**Mini Project:** Write a complete landing page copy and email welcome sequence for a mock product."
            ]),
            ("Weeks 4–6: Search Engine Optimization (SEO)", [
                "**Keyword Research:** Search intent, long-tail keywords, and competitor gap analysis.",
                "**On-Page & Technical SEO:** Meta tags, heading structure, internal linking, page speed, and Search Console.",
                "**Mini Project:** Publish 3 SEO-optimized blog/guide articles and audit a website's SEO."
            ]),
            ("Weeks 7–9: Social Media & Paid Advertising", [
                "**Organic Social:** Content calendars, short-form video hooks, and community engagement.",
                "**Paid Campaigns:** Campaign objectives, audience targeting, ad creatives, A/B testing, and ROAS/CPC.",
                "**Mini Project:** Design a mock Meta + Google Search ad campaign plan with budget & targeting."
            ]),
            ("Weeks 10–12: Analytics, CRO & Portfolio", [
                "**GA4 & Tracking:** Conversion events, UTM parameters, and funnel drop-off analysis.",
                "**Capstone:** Run a live micro-campaign/blog/page and document traffic & conversion metrics."
            ]),
        ],
        "checklist": [
            "CTR, CPC, CPA, ROAS, and conversion rate definitions and how to improve each.",
            "On-page vs technical SEO fixes.",
            "Structuring an A/B test for ad creatives or landing pages.",
            "Using GA4 and UTM tags to attribute leads accurately."
        ]
    },
    "finance": {
        "keywords": ["finance", "accounting", "financial analyst", "tally", "gst", "tax", "investment", "banking"],
        "title": "Finance & Accounting Analyst",
        "overview": "Financial statement analysis, budgeting, Excel financial modeling, taxation/compliance basics, and business reporting.",
        "stack": {
            "Core Tools": "Advanced Excel (XLOOKUP, Pivot Tables, Macros), Tally / ERP, Power BI",
            "Accounting & Tax": "P&L, Balance Sheet, Cash Flow Statement, GST / TDS Basics",
            "Analysis": "Ratio Analysis, Budgeting & Forecasting, Valuation Basics",
        },
        "phases": [
            ("Weeks 1–3: Accounting Foundations & Statements", [
                "**Core Accounting:** Journal entries, ledger, trial balance, accruals, and depreciation.",
                "**3 Financial Statements:** Income Statement (P&L), Balance Sheet, and Cash Flow linkage.",
                "**Mini Project:** Build a clean 3-statement summary from raw transaction entries."
            ]),
            ("Weeks 4–6: Excel for Financial Analysis", [
                "**Excel Mastery:** `SUMIFS`, `XLOOKUP`, `INDEX-MATCH`, Pivot Tables, and dynamic charts.",
                "**Ratio Analysis:** Liquidity, profitability, solvency, and working capital ratios.",
                "**Mini Project:** Analyze 3 years of a public company's financial statements in Excel."
            ]),
            ("Weeks 7–9: Budgeting, Forecasting & Compliance", [
                "**FP&A:** Variance analysis (Budget vs Actual), cash runway, and unit economics.",
                "**Compliance Basics:** GST invoicing/reconciliation, TDS basics, and audit trails.",
                "**Mini Project:** Build a 12-month startup/business budget & cash-flow forecast model."
            ]),
            ("Weeks 10–12: Financial Modeling & Case Study", [
                "**Valuation Basics:** DCF intuition, multiples, and sensitivity tables.",
                "**Capstone:** Present an executive financial health report with charts and recommendations."
            ]),
        ],
        "checklist": [
            "How the P&L, Balance Sheet, and Cash Flow Statement connect.",
            "Working capital cycle and why profitable companies can run out of cash.",
            "Key profitability and liquidity ratios.",
            "Variance analysis and Excel modeling best practices."
        ]
    },
    "teaching": {
        "keywords": ["teaching", "teacher", "educator", "trainer", "spoken english", "communication", "public speaking"],
        "title": "Educator / Communication & Training Specialist",
        "overview": "Curriculum planning, clear concept delivery, interactive classroom/online engagement, and learner assessment.",
        "stack": {
            "Instructional Skills": "Lesson Planning, Bloom's Taxonomy, Active Learning, Storytelling",
            "Digital Tools": "Google Workspace, Canva / Slides, OBS / Zoom, Quiz & LMS Tools",
            "Assessment": "Formative Quizzes, Rubrics, Constructive Feedback",
        },
        "phases": [
            ("Weeks 1–3: Lesson Structuring & Clear Explanation", [
                "**Lesson Design:** Setting clear learning objectives, hook → concept → example → practice flow.",
                "**Clarity & Delivery:** Pacing, vocal clarity, simplifying complex topics with relatable analogies.",
                "**Practice Task:** Design and record a crisp 10-minute micro-lesson."
            ]),
            ("Weeks 4–6: Visual Aids & Interactive Engagement", [
                "**Visual Storytelling:** Clean slides, diagrams, and zero-clutter handouts.",
                "**Active Participation:** Questioning techniques, group exercises, and handling doubts calmly.",
                "**Practice Task:** Deliver an interactive 25-minute session and collect learner feedback."
            ]),
            ("Weeks 7–9: Assessments & Differentiated Support", [
                "**Assessment Design:** Creating fair MCQs, practical tasks, and grading rubrics.",
                "**Feedback:** Identifying struggling learners and giving actionable improvement steps.",
                "**Practice Task:** Build a complete module quiz + rubric."
            ]),
            ("Weeks 10–12: Full Course Module & Demo Portfolio", [
                "**Capstone:** Build a complete 4-lesson mini-course with slides, worksheets, and demo video."
            ]),
        ],
        "checklist": [
            "Structuring a lesson for beginners vs advanced learners.",
            "Checking whether students actually understood (beyond 'any doubts?').",
            "Handling difficult questions or disengaged participants.",
            "Delivering a clear 10-minute live demo lesson."
        ]
    },
    "driving": {
        "keywords": ["driving", "driver", "car driving", "road safety", "license"],
        "title": "Professional Driving & Road Safety",
        "overview": "Safe vehicle control, traffic rules, defensive driving habits, basic vehicle checks, and road test readiness.",
        "stack": {
            "Vehicle Control": "Clutch/Brake/Accelerator/Steering control, gear shifting, parking, reversing",
            "Rules & Safety": "Traffic signals, road signs, right-of-way, blind spots, defensive driving",
            "Vehicle Care": "Tyre pressure, fluid/oil/coolant checks, lights/brakes inspection, emergency kit",
        },
        "phases": [
            ("Weeks 1–3: Vehicle Controls & Low-Speed Basics", [
                "**Controls & Posture:** Mirror/seat adjustment, steering hand positions, smooth braking, and gear control.",
                "**Low-Speed Practice:** Moving off smoothly, stopping, turning, and judging vehicle corners in open areas.",
                "**Vehicle Checks:** Checking tyres, mirrors, indicators, horn, and dashboard lights before starting.",
                "**Practical Goal:** Smooth starts/stops and controlled turns without jerking or stalling."
            ]),
            ("Weeks 4–6: Traffic Rules, Signs & Road Positioning", [
                "**Road Signs & Signals:** Regulatory signs, warning signs, lane markings, and junction rules.",
                "**Lane Discipline:** Safe following distance, mirror-signal-manoeuvre routine, and checking blind spots.",
                "**Practical Goal:** Confident driving on calm city roads while obeying speed limits and signals."
            ]),
            ("Weeks 7–9: Defensive Driving & Complex Conditions", [
                "**Hazard Awareness:** Anticipating pedestrians, two-wheelers, sudden braking, and junctions.",
                "**Challenging Conditions:** Night driving, rain/wet roads, slopes/hill starts, and reversing/parallel parking.",
                "**Practical Goal:** Calm, predictable driving in moderate traffic and tight parking spaces."
            ]),
            ("Weeks 10–12: Road Test Readiness & Ongoing Safety", [
                "**Mock Driving Assessments:** Full routes covering lane changes, turns, parking, and emergency awareness.",
                "**Licensing & Compliance:** Completing official learner/driving test requirements and carrying valid documents.",
                "**Long-Term Habit:** Regular basic vehicle checks and zero-distraction driving."
            ]),
        ],
        "checklist": [
            "Knowing road signs, right-of-way rules, and safe following distances.",
            "Explaining blind-spot checks and defensive reactions to hazards.",
            "Demonstrating smooth control, parking, and reversing during a practical test.",
            "Basic pre-drive safety checks and breakdown/emergency steps."
        ]
    },
}


def find_matching_role(role_text: str) -> dict | None:
    clean = role_text.strip().lower()
    if not clean:
        return None
    for data in DETAILED_ROLES.values():
        for kw in data["keywords"]:
            if kw in clean:
                return data
    return None


def build_detailed_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full-Stack Developer"
    matched = find_matching_role(clean_role)

    if matched:
        level_plan = {
            "Beginner": f"Start from the basics for **{matched['title']}**. Follow the weekly order step by step, practice consistently, and complete every mini-project/goal.",
            "Intermediate": f"Use Weeks 1–3 as a quick revision for **{matched['title']}**, then spend most of your time on real-world scenarios, edge cases, and capstone execution.",
            "Advanced": f"Focus on mastery, edge cases, efficiency, and high-standard real-world execution in **{matched['title']}**.",
        }.get(exp_level, "")

        stack_md = "\n".join(f"- **{cat}:** `{tools}`" for cat, tools in matched["stack"].items())

        phases_md = ""
        for phase_title, bullets in matched["phases"]:
            bullet_lines = "\n".join(f"  - {b}" for b in bullets)
            phases_md += f"\n#### {phase_title}\n{bullet_lines}\n"

        checklist_md = "\n".join(f"- {q}" for q in matched["checklist"])

        return f"""
### Complete 12-Week Roadmap: {clean_role} ({exp_level})

**Overview:** {matched["overview"]}

> **Approach ({exp_level} Level):** {level_plan}

#### Core Skills, Tools & Subjects
{stack_md}
---
{phases_md}
---
#### Assessment & Readiness Checklist
{checklist_md}
"""

    # Domain-neutral structured roadmap for any specialized/unlisted course
    level_plan = {
        "Beginner": f"Start with core fundamentals and terminology for **{clean_role}**, practice regularly, and build small exercises before tackling bigger tasks.",
        "Intermediate": f"Quickly review fundamentals of **{clean_role}**, then focus on practical hands-on work, real scenarios, and fixing common mistakes.",
        "Advanced": f"Focus on mastery, edge cases, efficiency, and real-world execution standards in **{clean_role}**.",
    }.get(exp_level, "")

    return f"""
### Complete 12-Week Roadmap: {clean_role} ({exp_level})

> **Approach ({exp_level} Level):** {level_plan}

#### Core Areas to Focus On
- **Fundamentals:** Key concepts, rules, terminology, and basic principles of **{clean_role}**.
- **Practical Tools & Methods:** Essential tools, equipment, or standard methods used in **{clean_role}**.
- **Safety, Quality & Standards:** Rules, accuracy, error prevention, and best practices for **{clean_role}**.

---

#### Weeks 1–3: Basics & Fundamentals
  - **Core Concepts:** Learn the foundational rules, terms, and basic skills needed for **{clean_role}**.
  - **Setup & Practice:** Gather basic resources/tools and practice simple step-by-step exercises.
  - **Early Milestone:** Complete 2 basic practice tasks to build comfort and accuracy.

#### Weeks 4–6: Core Practical Skills
  - **Main Skills:** Practice the primary day-to-day techniques and workflows of **{clean_role}**.
  - **Guided Scenarios:** Work through common situations and learn how to correct mistakes early.
  - **Mid Milestone:** Complete a practical task showing steady control and consistency.

#### Weeks 7–9: Real-World Situations & Problem Solving
  - **Tricky Scenarios:** Practice handling harder situations, exceptions, and time/accuracy pressure in **{clean_role}**.
  - **Best Practices:** Follow safety, quality, and standard operating procedures consistently.
  - **Progress Milestone:** Handle full end-to-end tasks with minimal guidance.

#### Weeks 10–12: Mastery & Evaluation
  - **Full Practice Runs:** Do complete mock/real-world runs covering everything learned in **{clean_role}**.
  - **Review & Improvement:** Identify weak spots and polish speed, accuracy, and confidence.
  - **Readiness:** Prepare for practical tests, interviews, or real-world work in **{clean_role}**.

---

#### Readiness Checklist
- Can you explain and apply the core rules and basics of **{clean_role}** clearly?
- Can you handle common mistakes and unusual situations calmly?
- Have you completed practical exercises/assessments relevant to **{clean_role}**?
"""


def run_simulated_roadmap(target_role: str, exp_level: str) -> str:
    status = st.empty()
    progress = st.progress(0)

    steps = [
        (25, "Analyzing target role / course and experience level..."),
        (55, "Mapping core skills, tools, and weekly syllabus..."),
        (85, "Adding practical tasks and readiness checklist..."),
        (100, "Roadmap ready!"),
    ]
    for pct, msg in steps:
        status.info(msg)
        progress.progress(pct)
        time.sleep(0.35)

    status.empty()
    progress.empty()
    return build_detailed_roadmap(target_role, exp_level)


with tab1:
    st.subheader("Custom Career Roadmap Generator")
    st.write("Choose a popular track or type any role/course to get a detailed 12-week roadmap.")

    quick_pick = st.selectbox(
        "Quick Select Popular Course / Track (or choose 'Custom Input' below):",
        [
            "Custom Input",
            "Full-Stack Developer",
            "Frontend Developer",
            "Backend Developer",
            "Python Developer",
            "Java Backend Developer",
            "AI & Machine Learning Engineer",
            "Data Analyst / Data Scientist",
            "Cybersecurity Analyst",
            "Cloud & DevOps Engineer",
            "Mobile App Developer",
            "Embedded Systems & IoT Engineer",
            "VLSI & RTL Design Engineer",
            "UI/UX & Product Designer",
            "Digital Marketing Specialist",
            "Finance & Accounting Analyst",
            "Educator / Communication Specialist",
            "Driving & Road Safety",
        ],
    )

    default_text = "Full-Stack Developer" if quick_pick == "Custom Input" else quick_pick
    role = st.text_input(
        "Target Role / Course:",
        value=default_text,
    )
    level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        roadmap_text = run_simulated_roadmap(role, level)
        st.markdown(roadmap_text)


# -------------------- TAB 2: JOB SCAM DETECTOR --------------------
def analyze_job_simulated(job_text: str) -> tuple[str, int, list[str], list[str]]:
    status = st.empty()
    progress = st.progress(0)

    for pct, msg in [
        (30, "Scanning job description and recruiter details..."),
        (70, "Checking payment traps, contact channels, and urgency signals..."),
        (100, "Scam risk report ready!"),
    ]:
        status.info(msg)
        progress.progress(pct)
        time.sleep(0.3)

    status.empty()
    progress.empty()

    text = job_text.lower()
    score = 0
    red_flags = []
    safe_signals = []

    scam_patterns = [
        (r"\b(registration fee|security deposit|pay to apply|training fee|processing fee|refundable deposit|laptop fee)\b",
         "Requests upfront money, registration fee, or security deposit (major scam indicator).", 35),
        (r"\b(whatsapp|telegram)\b.*\b(contact|message|dm|number)\b|\b(contact|message|dm)\b.*\b(whatsapp|telegram)\b",
         "Pushes communication to WhatsApp/Telegram instead of an official company email or career portal.", 20),
        (r"\b(earn ₹|earn rs|daily payout|weekly payout|guaranteed income|no experience needed.*high salary|part[- ]time.*₹\s?\d{4,})\b",
         "Promises unrealistic daily/weekly earnings or high pay with zero experience.", 25),
        (r"\b(aadhaar|pan card|bank details|otp|cvv|passbook)\b",
         "Asks for sensitive identity or banking details before an official offer/verification.", 30),
        (r"\b(urgent hiring|limited slots|apply within 1 hour|immediate joining without interview|direct offer letter)\b",
         "Creates artificial urgency or skips proper technical/HR interviews.", 20),
        (r"@gmail\.com|@yahoo\.com|@outlook\.com",
         "Uses a free personal email domain instead of an official company domain.", 15),
    ]

    for pattern, reason, weight in scam_patterns:
        if re.search(pattern, text):
            score += weight
            red_flags.append(reason)

    if re.search(r"\b(technical round|interview process|github|portfolio|responsibilities|qualifications)\b", text):
        safe_signals.append("Mentions standard role qualifications or a structured interview process.")
    if re.search(r"https?://(www\.)?(linkedin\.com|careers\.|jobs\.)", text):
        safe_signals.append("Includes a career portal or LinkedIn reference (still verify the official domain).")

    score = min(score, 100)
    if score >= 50:
        verdict = "High Risk — Likely a Job Scam"
    elif score >= 20:
        verdict = "Medium Risk — Verify Carefully Before Applying"
    else:
        verdict = "Low Risk — Looks Safer (Still Verify Company)"

    return verdict, score, red_flags, safe_signals


with tab2:
    st.subheader("Job Scam Detector")
    st.write("Paste a job post, offer letter text, or recruiter message to get a detailed scam risk breakdown.")

    job_input = st.text_area(
        "Job Posting / Recruiter Message:",
        height=180,
        placeholder="Paste the job description, salary details, contact info, or recruiter message here...",
    )

    if st.button("Analyze Job Posting"):
        if not job_input.strip():
            st.warning("Please paste a job posting or message first.")
        else:
            verdict, risk_score, flags, positives = analyze_job_simulated(job_input)

            if risk_score >= 50:
                st.error(f"**{verdict}** (Risk Score: {risk_score}/100)")
            elif risk_score >= 20:
                st.warning(f"**{verdict}** (Risk Score: {risk_score}/100)")
            else:
                st.success(f"**{verdict}** (Risk Score: {risk_score}/100)")

            if flags:
                st.markdown("**Detected Red Flags:**")
                for flag in flags:
                    st.markdown(f"- {flag}")
            else:
                st.markdown("**Detected Red Flags:**\n- No obvious scam keywords or payment traps detected.")

            if positives:
                st.markdown("**Positive / Standard Signals:**")
                for pos in positives:
                    st.markdown(f"- {pos}")

            st.markdown("""
**Verification Checklist Before Applying:**
- Check the company's official website career page to confirm the job ID exists.
- Never pay fees for interviews, training, certificates, or offer letters.
- Verify the recruiter's profile and official company email domain.
""")
