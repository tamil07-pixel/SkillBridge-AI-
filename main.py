import re
import time
import streamlit as st

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="centered")

st.title("SkillBridge AI")
st.caption("Personalized Career Roadmap Generator & AI-Driven Job Scam Detector")

tab1, tab2 = st.tabs(["🗺️ Career Roadmap Generator", "🛡️ Job Scam Detector"])


# -------------------- TAB 1: CAREER ROADMAP GENERATOR --------------------
DETAILED_ROLES = {
    "full stack": {
        "title": "Full-Stack Developer",
        "overview": "End-to-end web application development covering responsive UI, RESTful APIs, relational/NoSQL databases, authentication, and cloud deployment.",
        "stack": {
            "Frontend": "HTML5, CSS3 (Flexbox/Grid), JavaScript (ES6+), React, Tailwind CSS",
            "Backend": "Python (FastAPI) or Node.js (Express.js), REST APIs, JWT Auth",
            "Database & Tools": "PostgreSQL / MongoDB, Git, GitHub, Postman, Docker",
        },
        "phases": [
            ("Weeks 1–3: Web & JavaScript Foundations", [
                "**HTML5 & CSS3:** Semantic tags, forms, Flexbox, CSS Grid, and mobile-first responsive layouts.",
                "**Modern JavaScript:** `let/const`, arrow functions, destructuring, array methods (`map`, `filter`, `reduce`), Promises, `async/await`, and Fetch API.",
                "**Version Control:** Git init, branching, merging, pull requests, and writing clean GitHub READMEs.",
                "**Mini Project:** Build a responsive personal portfolio + a weather/movie search web app using a public REST API."
            ]),
            ("Weeks 4–6: Frontend Engineering with React", [
                "**React Core:** Functional components, JSX, props, state management (`useState`, `useEffect`), conditional rendering, and lists.",
                "**Routing & Forms:** React Router navigation, controlled forms, client-side validation, and loading/error states.",
                "**API Integration:** Connecting React frontend to backend APIs with Axios/Fetch and handling CORS cleanly.",
                "**Mini Project:** Build a multi-page Task & Expense Tracker dashboard with search, filters, and local/API persistence."
            ]),
            ("Weeks 7–9: Backend APIs & Database Design", [
                "**Backend Framework:** Build modular REST APIs in FastAPI (Python) or Express.js (Node) with proper HTTP status codes and validation.",
                "**Authentication & Security:** Password hashing (`bcrypt`), JWT login/signup flows, protected routes, and `.env` secret management.",
                "**Databases:** Schema design, CRUD operations, indexing, and relationships in PostgreSQL or MongoDB.",
                "**Mini Project:** Build a secure Notes/Job Application API with user login, role access, and Swagger/Postman docs."
            ]),
            ("Weeks 10–12: Full-Stack Capstones & Deployment", [
                "**Capstone 1:** Full-Stack Job Portal or AI Career Assistant with frontend, backend, database, and user authentication.",
                "**Capstone 2:** Real-time Analytics / E-commerce Dashboard with pagination, filters, and clean error handling.",
                "**Testing & Deployment:** Write basic API tests, configure production environment variables, and deploy live on Render/Vercel/Streamlit Cloud.",
                "**Portfolio Polish:** Add architecture diagrams, live demo links, and key metrics to every GitHub repo."
            ]),
        ],
        "interview": [
            "JavaScript event loop, closures, promises, and `==` vs `===`.",
            "React Virtual DOM, component lifecycle, hooks rules, and state lifting.",
            "REST API design principles, HTTP methods/status codes, and JWT vs session auth.",
            "SQL vs NoSQL trade-offs, indexing, and basic query optimization."
        ]
    },
    "python": {
        "title": "Python Developer",
        "overview": "Backend engineering, automation, API development, data handling, and scalable Python services.",
        "stack": {
            "Core Language": "Python 3.11+, OOP, Decorators, Generators, AsyncIO",
            "Frameworks & DB": "FastAPI / Django, SQLAlchemy, PostgreSQL, SQLite, Redis",
            "Testing & DevOps": "Pytest, Git, GitHub Actions, Docker, Linux CLI",
        },
        "phases": [
            ("Weeks 1–3: Core Python & Problem Solving", [
                "**Data Structures:** Lists, tuples, sets, dictionaries, comprehensions, and `collections` module.",
                "**OOP & Clean Code:** Classes, inheritance, dunder methods, type hints, exception handling, and virtual environments (`venv`).",
                "**DSA Practice:** Solve 45+ problems on strings, arrays, hash maps, stacks, and recursion.",
                "**Mini Project:** Build a CLI File Organizer & Automated Log Parser that generates CSV/JSON summary reports."
            ]),
            ("Weeks 4–6: Web APIs & Database Integration", [
                "**FastAPI / Django:** Routing, path/query parameters, Pydantic request/response schemas, and dependency injection.",
                "**Database & ORM:** Designing tables, migrations, relationships, and CRUD queries with SQLAlchemy + PostgreSQL.",
                "**Auth & Security:** OAuth2/JWT token authentication, rate limiting, and environment variable configs.",
                "**Mini Project:** Build a RESTful Inventory or Expense Management API with full Swagger documentation."
            ]),
            ("Weeks 7–9: Async Programming, Testing & Automation", [
                "**Async & Background Tasks:** `async/await` in Python, calling external third-party APIs with `httpx`, and background jobs.",
                "**Automated Testing:** Unit and integration tests with `pytest`, fixtures, and mocking external calls.",
                "**Data & File Processing:** Working with Pandas/CSV, PDF/Excel reports, and web scraping (`BeautifulSoup`).",
                "**Mini Project:** Build an automated Job Alert / Price Tracker service with scheduled checks and email/webhook alerts."
            ]),
            ("Weeks 10–12: Production Deployment & Capstones", [
                "**Docker & CI/CD:** Write a clean `Dockerfile`, run multi-container setups, and add GitHub Actions test checks.",
                "**Capstone Project:** Deploy a production-ready Python web app/API with logging, error monitoring, and live URL.",
                "**Documentation:** Document setup steps, API endpoints, and architecture in GitHub."
            ]),
        ],
        "interview": [
            "Mutable vs immutable types, memory management, garbage collection, and GIL.",
            "Decorators, generators (`yield`), context managers (`with`), and `*args/**kwargs`.",
            "FastAPI vs Django/Flask, sync vs async endpoints, and ORM N+1 query fixes.",
            "Writing clean unit tests and debugging production tracebacks."
        ]
    },
    "embedded": {
        "title": "Embedded Systems & IoT Engineer",
        "overview": "Firmware development in Embedded C/C++, microcontroller peripherals, communication protocols, RTOS, and cloud-connected IoT systems.",
        "stack": {
            "Languages & OS": "Embedded C, C++, Python (for gateways/dashboards), FreeRTOS, Embedded Linux",
            "Hardware & MCUs": "ESP32, STM32 (ARM Cortex-M), Arduino, Logic Analyzer, Multimeter",
            "Protocols & Cloud": "UART, I2C, SPI, CAN, MQTT, HTTP/REST, FastAPI",
        },
        "phases": [
            ("Weeks 1–3: Embedded C & Microcontroller Basics", [
                "**Embedded C Mastery:** Pointers, pointer arithmetic, bitwise manipulation, `volatile`, `const`, `static`, structs, and memory layout (stack/heap/flash/RAM).",
                "**Peripherals:** GPIO digital I/O, hardware timers, PWM generation, and ADC sensor reading on ESP32 or STM32.",
                "**Interrupts:** External interrupts (EXTI), timer ISRs, debouncing, and keeping ISRs short and deterministic.",
                "**Mini Project:** Build a PWM Motor Speed / LED Dimmer controller with rotary encoder and interrupt-driven buttons."
            ]),
            ("Weeks 4–6: Communication Protocols & Sensor Interfacing", [
                "**UART:** Serial framing, baud rate configuration, ring buffers, and PC/GPS/GSM module interfacing.",
                "**I2C & SPI:** Addressing, clock stretching, multi-slave buses, reading IMU/OLED/EEPROM chips, and debugging with a logic analyzer.",
                "**CAN Bus Basics:** Message frames, arbitration, and automotive/industrial telemetry concepts.",
                "**Mini Project:** Multi-sensor Environmental/Telemetry Node reading I2C + SPI sensors and logging calibrated packets over UART."
            ]),
            ("Weeks 7–9: RTOS & Edge Connectivity", [
                "**FreeRTOS:** Creating tasks, task priorities, scheduling, queues, binary/counting semaphores, and mutexes (avoiding priority inversion).",
                "**IoT Networking:** Wi-Fi/BLE provisioning on ESP32, MQTT publish/subscribe brokers, and JSON payload formatting.",
                "**Cloud Backend:** Build a lightweight Python FastAPI/Streamlit dashboard to visualize live device telemetry and alerts.",
                "**Mini Project:** Real-time Smart Health or Vehicle Telemetry Monitor streaming sensor packets via MQTT to a live web dashboard."
            ]),
            ("Weeks 10–12: System Integration, Debugging & Capstone", [
                "**Reliability & Power:** Watchdog timers (WDT), low-power sleep modes, brown-out detection, and OTA firmware updates.",
                "**Capstone Project:** Complete Hardware + Firmware + Cloud system (e.g., Smart Collision/Accident Alert or Industrial Predictive Monitor).",
                "**Documentation:** Publish schematics, pinout tables, firmware state machines, and demo videos on GitHub."
            ]),
        ],
        "interview": [
            "Why `volatile` is mandatory for hardware registers and ISR-shared variables.",
            "I2C vs SPI vs UART: speed, wiring, addressing, and full-duplex vs half-duplex.",
            "Stack overflow causes in microcontrollers, memory-mapped I/O, and linker script basics.",
            "FreeRTOS mutex vs binary semaphore and handling race conditions."
        ]
    },
    "data": {
        "title": "Data Analyst / Data Science",
        "overview": "Turning raw datasets into actionable business decisions using SQL, Python, statistical analysis, interactive BI dashboards, and predictive models.",
        "stack": {
            "Querying & Spreadsheets": "SQL (PostgreSQL/MySQL), Advanced Excel (Pivot Tables, XLOOKUP, Power Query)",
            "Programming & ML": "Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn",
            "BI & Storytelling": "Power BI / Tableau, KPI Design, A/B Testing",
        },
        "phases": [
            ("Weeks 1–3: SQL & Excel Foundations", [
                "**SQL Mastery:** `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `INNER/LEFT/RIGHT JOIN`, subqueries, CTEs (`WITH`), and Window Functions (`ROW_NUMBER`, `RANK`, `LAG/LEAD`).",
                "**Excel Analytics:** Pivot tables, dynamic formulas (`INDEX-MATCH`, `XLOOKUP`), conditional formatting, and data cleaning.",
                "**Statistics:** Mean/median/variance, distributions, correlation vs causation, and hypothesis testing.",
                "**Mini Project:** Analyze an E-commerce Sales SQL database to uncover top revenue segments, churn patterns, and seasonal trends."
            ]),
            ("Weeks 4–6: Python Data Analysis & Visualization", [
                "**Pandas & NumPy:** Handling missing values, duplicates, data types, merging datasets, `groupby` aggregations, and time-series resampling.",
                "**Exploratory Data Analysis (EDA):** Outlier detection, feature distributions, and visual storytelling with Matplotlib & Seaborn.",
                "**Mini Project:** Clean and analyze a real-world Telecom Churn or Healthcare dataset and publish an insight-driven Jupyter Notebook."
            ]),
            ("Weeks 7–9: BI Dashboards & Predictive Modeling", [
                "**Power BI / Tableau:** Data modeling, DAX/calculated fields, slicers, drill-downs, and executive KPI layouts.",
                "**Machine Learning Basics:** Linear/Logistic Regression, Decision Trees, Random Forest, train/test split, precision/recall/F1, and RMSE.",
                "**Mini Project:** Build an interactive Sales & Customer Retention Dashboard in Power BI/Tableau with churn risk scoring."
            ]),
            ("Weeks 10–12: End-to-End Case Studies & Portfolio", [
                "**Capstone 1:** Full business case study combining SQL extraction + Python cleaning + Power BI dashboard + executive summary.",
                "**Capstone 2:** Predictive analytics project with clear baseline vs improved metrics.",
                "**Portfolio:** Host notebooks, SQL scripts, and dashboard screenshots cleanly on GitHub."
            ]),
        ],
        "interview": [
            "Write SQL queries using Window Functions and CTEs on the spot.",
            "Explain handling missing/imbalanced data and choosing precision vs recall.",
            "Design KPIs for a product feature and explain A/B test significance.",
            "Walk through business impact from your portfolio projects."
        ]
    },
}


def build_detailed_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full-Stack Developer"
    role_lower = clean_role.lower()

    matched = next((v for k, v in DETAILED_ROLES.items() if k in role_lower), None)

    level_plan = {
        "Beginner": "Build strong fundamentals first. Follow the weekly order strictly, code daily for 1.5–2 hours, and complete every mini-project before moving to the next phase.",
        "Intermediate": "Move faster through Weeks 1–3 as revision, then spend 70% of your time on architecture, edge cases, testing, and deploying production-grade capstones.",
        "Advanced": "Focus on system scalability, performance optimization, security hardening, CI/CD automation, and deep architectural trade-offs for senior/specialist interviews.",
    }.get(exp_level, "")

    if matched:
        stack_md = "\n".join(f"- **{cat}:** `{tools}`" for cat, tools in matched["stack"].items())

        phases_md = ""
        for phase_title, bullets in matched["phases"]:
            bullet_lines = "\n".join(f"  - {b}" for b in bullets)
            phases_md += f"\n#### {phase_title}\n{bullet_lines}\n"

        interview_md = "\n".join(f"- {q}" for q in matched["interview"])

        return f"""
### Complete 12-Week Career Roadmap: {clean_role} ({exp_level})

**Role Overview:** {matched["overview"]}

> **How to Approach ({exp_level} Level):** {level_plan}

#### Core Tech Stack & Tools
{stack_md}
---
{phases_md}
---
#### Interview & Job Readiness Checklist
{interview_md}
- Keep **2–3 deployed projects** with live demo links, screenshots, and clear problem-solution READMEs on GitHub.
"""

    # Detailed structured roadmap for any custom role entered by the user
    return f"""
### Complete 12-Week Career Roadmap: {clean_role} ({exp_level})

> **How to Approach ({exp_level} Level):** {level_plan}

#### Core Skill Pillars to Master
- **Foundations & Theory:** Core principles, terminology, and standard workflows of **{clean_role}**.
- **Primary Tools & Platforms:** Top 3–4 industry tools/languages listed across current **{clean_role}** job descriptions.
- **Quality, Testing & Security:** Debugging, validation, documentation, and production best practices.

---

#### Weeks 1–3: Foundations & Tooling Setup
  - **Core Concepts:** Study the fundamental building blocks and problem-solving patterns required for **{clean_role}**.
  - **Environment & Git:** Set up your local/cloud workspace, learn Git & GitHub version control, and document daily progress.
  - **Mini Project:** Build 2 small foundational exercises/scripts that demonstrate core concepts cleanly.

#### Weeks 4–6: Core Practical Skills & Workflows
  - **Primary Stack:** Learn the main framework, software suite, or engineering workflow used day-to-day in **{clean_role}** roles.
  - **Data & Integrations:** Practice connecting components, handling real-world inputs/APIs, and fixing common errors.
  - **Mini Project:** Build a working mid-sized module solving a practical problem in **{clean_role}**.

#### Weeks 7–9: Advanced Topics, Testing & Optimization
  - **Reliability & Standards:** Implement testing, error handling, performance tuning, and industry safety/security guidelines.
  - **Real-World Case Studies:** Analyze existing open-source projects or architecture breakdowns for **{clean_role}**.
  - **Mini Project:** Upgrade your earlier project with proper validation, logging, and clean modular structure.

#### Weeks 10–12: Capstone Projects & Interview Preparation
  - **Capstone 1:** Build an end-to-end portfolio project tailored specifically to **{clean_role}** job requirements.
  - **Capstone 2:** Build a second project highlighting a specialized skill or integration within **{clean_role}**.
  - **GitHub & Resume:** Publish live demos, architecture diagrams, and measurable outcomes for each project.

---

#### Interview & Job Readiness Checklist
- Master the top 20 technical concepts and scenario-based questions for **{clean_role}**.
- Be ready to explain trade-offs, debugging steps, and architecture decisions from your projects.
- Tailor your resume keywords to match the exact tools and deliverables of **{clean_role}**.
"""


def run_simulated_roadmap(target_role: str, exp_level: str) -> str:
    status = st.empty()
    progress = st.progress(0)

    steps = [
        (25, "Analyzing target role and experience level..."),
        (55, "Mapping core tech stack and weekly syllabus..."),
        (85, "Adding hands-on projects and interview checklist..."),
        (100, "Detailed roadmap ready!"),
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
    st.write("Enter your target role to get a detailed 12-week syllabus, tech stack, projects, and interview checklist.")

    role = st.text_input(
        "Target Role (e.g., Full-Stack Developer, Python Developer, Embedded Systems Engineer, Data Analyst):",
        value="Full-Stack Developer",
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
