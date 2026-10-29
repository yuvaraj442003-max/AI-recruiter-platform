"""
curriculum_software_testing.py - Complete 8 Chapters Comprehensive Curriculum for Software Testing & QA.
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & Architecture
3. Step-by-Step Solved Examples with working code and breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

SOFTWARE_TESTING_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "Software Testing Life Cycle (STLC), QA Fundamentals & Defect Management",
        "key_takeaways": "Master SDLC vs STLC phases, defect lifecycle, severity vs priority, and test documentation (Test Plan, Test Strategy, Test Case design).",
        "topics": [
            "Quality Assurance (QA) vs Quality Control (QC) vs Software Testing",
            "Software Testing Life Cycle (STLC): Requirements Analysis, Test Planning, Test Case Development, Environment Setup, Execution & Closure",
            "Defect Life Cycle: States (New, Assigned, Open, Fixed, Retest, Verified, Closed, Reopened, Deferred)",
            "Defect Severity (Impact on system) vs Defect Priority (Urgency of business fix) classification matrix",
            "Traceability Matrix (RTM): Forward vs Backward requirements traceability"
        ],
        "sections": {
            "concept": "Software Quality Assurance guarantees that applications meet business, functional, and performance requirements without critical regressions. The Software Testing Life Cycle (STLC) runs concurrently with the development lifecycle. A defect or bug progresses through a formalized state machine. Two independent metrics govern triage: Severity reflects the technical impact on application operation (Critical, Major, Moderate, Minor); Priority reflects business urgency (High, Medium, Low). A cosmetic spelling error on an enterprise homepage has Low Severity but High Priority; a memory leak in a rare background report has High Severity but Low Priority. The Requirements Traceability Matrix (RTM) guarantees 100% test coverage.",
            "formulas": "1. Defect Density = Total_Defects / Size_of_Release (e.g. Defects per 1,000 Lines of Code KLOC)\n2. Test Case Execution Rate % = (Executed_Test_Cases / Total_Test_Cases) * 100\n3. Defect Removal Efficiency (DRE) % = (Defects_Found_Internally / (Internal_Defects + Production_Defects)) * 100",
            "solved_examples": [
                {
                    "title": "Classifying Defect Severity vs Priority Matrix for E-Commerce Platform",
                    "difficulty": "Easy | Infosys, TCS, Cognizant, Wipro",
                    "problem": "Classify Severity and Priority for four real-world production defects.",
                    "step_by_step": [
                        "Defect 1: The 'Pay Now' button triggers a crash for 100% of users -> Critical Severity, High Priority (Blocks revenue).",
                        "Defect 2: The company CEO's name is misspelled on the public homepage -> Minor Severity, High Priority (Brand reputation).",
                        "Defect 3: Database deadlock occurs only if 10,000 users export CSV simultaneously at midnight -> Critical Severity, Low Priority (Can be deferred to next sprint).",
                        "Defect 4: Inactive footer copyright link points to 2024 instead of 2026 -> Minor Severity, Low Priority."
                    ],
                    "code_or_math": "# Defect Matrix Mapping\ndefects = [\n    ('Checkout Crash', 'Critical', 'High'),\n    ('Logo Misspelling', 'Minor', 'High'),\n    ('Rare DB Deadlock', 'Critical', 'Low'),\n    ('Footer Year', 'Minor', 'Low')\n]\nfor name, sev, prio in defects:\n    print(f'{name:20} -> Severity: {sev:10} | Priority: {prio}')"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary purpose of a Requirements Traceability Matrix (RTM) in software quality engineering?",
                    "options": [
                        "To calculate developer hourly billing rates",
                        "To map user requirements bidirectionally to corresponding test cases, ensuring zero untested requirements",
                        "To track keyboard typing speed of QA analysts",
                        "To automatically generate HTML user interfaces"
                    ],
                    "answer": "To map user requirements bidirectionally to corresponding test cases, ensuring zero untested requirements",
                    "explanation": "A Requirements Traceability Matrix (RTM) connects every business requirement to its corresponding test cases and defects, providing proof of complete test coverage and ensuring that no functional requirements are missed."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Cognizant",
                    "question": "Can a defect have High Priority but Low Severity? Give a real-world software example.",
                    "model_answer": "Yes. A defect has High Priority when it demands immediate business resolution, but Low Severity when it does not break software functionality. A classic example is the company name or logo being misspelled on the main login page or public marketing header. Technologically, the application functions with 100% uptime (Low Severity), but from a brand reputation and executive standpoint, it must be fixed immediately within hours (High Priority).",
                    "interviewer_tip": "Clearly separate functional technical impact from business commercial urgency."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Black-Box vs White-Box Testing Techniques & Test Design Strategies",
        "key_takeaways": "Master Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Decision Table testing, Cyclomatic Complexity, and Statement/Branch Coverage.",
        "topics": [
            "Black-Box (Specification-Based) vs White-Box (Structure-Based) vs Experience-Based Testing",
            "Equivalence Class Partitioning (EP): Valid vs Invalid input partitions",
            "Boundary Value Analysis (BVA): 2-value (min, max) and 3-value boundary test design",
            "Decision Table Testing & State Transition Testing for complex business rule logic",
            "White-Box Metrics: Statement Coverage, Branch/Decision Coverage, Path Coverage & McCabe's Cyclomatic Complexity"
        ],
        "sections": {
            "concept": "Test design techniques maximize defect detection while minimizing redundant test cases. Black-Box testing evaluates functionality without internal code knowledge. Equivalence Partitioning (EP) divides the input domain into classes where all values are expected to behave identically, testing one representative value from each class. Boundary Value Analysis (BVA) focuses on the boundaries between partitions (min, min-1, min+1, max, max-1, max+1) where developer off-by-one errors (> vs >=) disproportionately occur. White-Box testing examines internal control flow graphs: McCabe's Cyclomatic Complexity determines the exact number of linearly independent paths required for 100% path coverage.",
            "formulas": "1. McCabe's Cyclomatic Complexity: V(G) = E - N + 2P where E=edges, N=nodes, P=connected components (or V(G) = Decision_Points + 1)\n2. Branch Coverage % = (Executed_Branches / Total_Decision_Branches) * 100\n3. BVA Test Set for range [A, B]: {A-1, A, A+1, B-1, B, B+1}",
            "solved_examples": [
                {
                    "title": "Designing BVA and EP Test Cases for an Age Input Field (Range 18 to 60)",
                    "difficulty": "Easy | TCS, Infosys, Capgemini",
                    "problem": "Design valid and invalid Equivalence Partitions and Boundary Value test inputs for an input field accepting ages 18 to 60.",
                    "step_by_step": [
                        "Step 1: Equivalence Partitioning: Class 1 (Invalid): age < 18 (e.g. 10). Class 2 (Valid): 18 <= age <= 60 (e.g. 35). Class 3 (Invalid): age > 60 (e.g. 75).",
                        "Step 2: Boundary Value Analysis on Lower Bound (18): 17 (Invalid), 18 (Valid Boundary), 19 (Valid).",
                        "Step 3: Boundary Value Analysis on Upper Bound (60): 59 (Valid), 60 (Valid Boundary), 61 (Invalid).",
                        "Step 4: Edge Cases: 0, negative numbers (-5), non-numeric characters ('abc'), null/empty.",
                        "Step 5: Total comprehensive test suite: {10, 17, 18, 19, 35, 59, 60, 61, 75, -1, 'text'}."
                    ],
                    "code_or_math": "def validate_age(age):\n    return isinstance(age, int) and 18 <= age <= 60\n\ntest_cases = [17, 18, 19, 35, 59, 60, 61]\nfor val in test_cases:\n    print(f'Age: {val:2} -> Expected: {val in range(18, 61)} | Actual: {validate_age(val)}')"
                }
            ],
            "practice_questions": [
                {
                    "question": "If a software program's control flow graph contains 14 edges and 10 nodes with 1 connected component, what is its McCabe's Cyclomatic Complexity?",
                    "options": [
                        "4",
                        "6",
                        "10",
                        "24"
                    ],
                    "answer": "6",
                    "explanation": "Using McCabe's formula V(G) = E - N + 2P: V(G) = 14 - 10 + 2(1) = 4 + 2 = 6. Exactly 6 independent test paths are required for full branch coverage."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft & Amazon",
                    "question": "Why is 100% Statement Coverage NOT sufficient to guarantee that software is free of bugs?",
                    "model_answer": "Statement coverage only ensures that every line of code was executed at least once, but it completely ignores decision logic branches. For example, consider an `if (x > 0)` block without an `else` branch. A single test where x=5 executes 100% of statements. However, if the code crashes when x <= 0 (e.g. unhandled null pointer or division by zero), statement coverage passes 100% while branch coverage remains at 50% and critical production bugs remain undetected.",
                    "interviewer_tip": "Provide the missing `else` branch counter-example to demonstrate true white-box testing mastery."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "UI Test Automation with Selenium WebDriver & Page Object Model (POM)",
        "key_takeaways": "Master WebDriver architecture, robust locator strategies (XPath, CSS), dynamic explicit waits, and Page Object Model design pattern.",
        "topics": [
            "Selenium WebDriver Architecture: W3C WebDriver standard, JSON Wire Protocol deprecation & Browser Drivers",
            "Locator Strategies: ID, Name, CSS Selectors, Relative XPath vs Absolute XPath best practices",
            "Synchronization & Dynamic Waits: Implicit Wait vs Explicit Wait (WebDriverWait + ExpectedConditions) vs FluentWait",
            "Handling Complex UI Elements: Dropdowns (Select), Alerts, iFrames, Multiple Windows & Action Chains",
            "Page Object Model (POM): Separation of page locators, actions, and test assertions"
        ],
        "sections": {
            "concept": "Selenium WebDriver is the industry-standard framework for cross-browser web UI automation. Under the W3C WebDriver standard, language client bindings (Java, Python, C#) communicate directly with browser drivers via HTTP REST APIs. Flaky tests are the #1 issue in automated UI testing, caused by race conditions. Best practice mandates avoiding hardcoded Thread.sleep() and implicit waits in favor of dynamic Explicit Waits (WebDriverWait with ExpectedConditions: elementToBeClickable, visibilityOfElementLocated). The Page Object Model (POM) abstracts web page elements and interactions into dedicated classes, isolating UI changes to single files and keeping test scripts maintainable.",
            "formulas": "1. Flaky Test Mitigation: Robustness = Explicit_Waits + Dynamic_Polling + StaleElement_Retries\n2. CSS Selector Speed: CSS Selectors evaluate 2x to 5x faster than complex text-based XPaths in modern browsers\n3. POM Architecture: Test Script -> Calls Page Object Method -> Interacts with WebDriver -> Asserts Result",
            "solved_examples": [
                {
                    "title": "Writing a Clean Page Object Model (POM) Automation Test in Python / Selenium",
                    "difficulty": "Medium | Cognizant, Infosys, ThoughtWorks",
                    "problem": "Create a reusable LoginPage class using Page Object Model and write an automated test verifying successful login.",
                    "step_by_step": [
                        "Step 1: Define `LoginPage` class holding locators (By.ID, By.CSS_SELECTOR).",
                        "Step 2: Add methods: `enter_username()`, `enter_password()`, `click_login()`.",
                        "Step 3: Wrap element interactions in `WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator))`.",
                        "Step 4: In test file, instantiate `LoginPage`, execute steps, and assert URL redirects to dashboard.",
                        "Step 5: Zero locators or explicit driver calls exist in the test assertion script."
                    ],
                    "code_or_math": "# Page Object Model Pattern\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\n\nclass LoginPage:\n    def __init__(self, driver):\n        self.driver = driver\n        self.user_field = (By.ID, 'username')\n        self.pass_field = (By.ID, 'password')\n        self.submit_btn = (By.CSS_SELECTOR, 'button[type=\"submit\"]')\n        \n    def login(self, username, password):\n        wait = WebDriverWait(self.driver, 10)\n        wait.until(EC.visibility_of_element_located(self.user_field)).send_keys(username)\n        wait.until(EC.visibility_of_element_located(self.pass_field)).send_keys(password)\n        wait.until(EC.element_to_be_clickable(self.submit_btn)).click()"
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens when an automated test script attempts to click an element while another animation or AJAX spinner overlay is still loading in the DOM?",
                    "options": [
                        "Selenium automatically closes the browser window",
                        "WebDriver throws an ElementClickInterceptedException or StaleElementReferenceException",
                        "The operating system formats the hard drive",
                        "The test passes automatically"
                    ],
                    "answer": "WebDriver throws an ElementClickInterceptedException or StaleElementReferenceException",
                    "explanation": "If a floating modal, loading spinner, or overlay intercepts the click coordinate, WebDriver raises `ElementClickInterceptedException`. If the DOM re-renders during the call, it raises `StaleElementReferenceException`. Both are resolved using Explicit Waits for element invisibility of the spinner."
                }
            ],
            "interview_questions": [
                {
                    "company": "ThoughtWorks & Amazon",
                    "question": "Why should you never mix Implicit Waits and Explicit Waits in the same Selenium automation framework?",
                    "model_answer": "Mixing implicit and explicit waits produces unpredictable wait times and erratic test timeouts according to official Selenium documentation. An implicit wait instructs the driver to poll the DOM for N seconds for any missing element, while an explicit wait polls for a specific condition. When combined, the browser driver can compound the timeouts (e.g. waiting 10s + 10s = 20s) or prematurely evaluate conditions against unhydrated DOM nodes, causing intermittent flaky test failures that are nearly impossible to debug.",
                    "interviewer_tip": "Cite official Selenium guidelines: Set implicit wait to 0 and use explicit waits everywhere."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "API Testing with REST Assured & Postman: HTTP, JSON Assertions & Mocking",
        "key_takeaways": "Master REST architecture, HTTP status code validation, JSON schema validation, Postman environment variables, and REST Assured BDD syntax.",
        "topics": [
            "RESTful API Principles: Statelessness, Resource URIs, HTTP Verbs (GET, POST, PUT, PATCH, DELETE)",
            "HTTP Response Codes: 2xx (Success), 3xx (Redirection), 4xx (Client Error), 5xx (Server Error)",
            "REST Assured Framework: Given-When-Then BDD syntax, RequestSpecification & ResponseSpecification",
            "JSON Parsing & Assertions: JsonPath queries, Hamcrest matchers & JSON Schema Validation",
            "API Mocking & Virtualization with WireMock and Postman Mock Servers"
        ],
        "sections": {
            "concept": "API testing validates the business logic, security, data integrity, and performance of applications at the integration layer without UI rendering overhead. Automated API tests execute up to 100x faster than UI Selenium tests and are far less flaky. In REST Assured, tests are written using Behavior-Driven Development (BDD) syntax: `given()` sets up headers, authentication tokens, query parameters, and JSON payloads; `when()` triggers the HTTP method; `then()` asserts HTTP status codes, headers, response body fields (using JsonPath), and schema compliance. Contract testing and API virtualization (WireMock) isolate service testing from unstable downstream microservices.",
            "formulas": "1. Test Pyramid Rule: 70% Unit Tests, 20% Integration/API Tests, 10% End-to-End UI Tests\n2. API Execution Speed Ratio: 1 Selenium UI Test ~ 50 to 100 REST API Tests\n3. JSON Schema Validation: Validates data types, required fields, and regex formats in O(1) assert",
            "solved_examples": [
                {
                    "title": "Writing an Automated REST API Test in Python / Requests with JSON Assertions",
                    "difficulty": "Easy | PayTM, Amazon, Cisco",
                    "problem": "Write an automated test validating a user creation endpoint returns HTTP 201 Created and matching JSON data.",
                    "step_by_step": [
                        "Step 1: Construct JSON payload dictionary with name and email.",
                        "Step 2: Send HTTP POST request with `headers={'Content-Type': 'application/json'}`.",
                        "Step 3: Assert `response.status_code == 201`.",
                        "Step 4: Parse response JSON and assert returned `id` is a non-empty UUID string.",
                        "Step 5: Assert returned `email` matches the submitted payload."
                    ],
                    "code_or_math": "import requests\n\ndef test_create_user_api():\n    url = 'https://reqres.in/api/users'\n    payload = {'name': 'Candidate', 'job': 'SDET'}\n    res = requests.post(url, json=payload)\n    assert res.status_code == 201, f'Expected 201 but got {res.status_code}'\n    data = res.json()\n    assert data['name'] == 'Candidate'\n    assert 'id' in data\n    print('Test Passed: User created successfully with ID:', data['id'])"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary difference between the HTTP PUT and HTTP PATCH methods in RESTful API design?",
                    "options": [
                        "PUT is for reading data; PATCH is for deleting data",
                        "PUT replaces the entire resource representation; PATCH applies partial modifications to specific fields",
                        "PATCH can only be sent over HTTP without encryption",
                        "PUT only works with XML payloads"
                    ],
                    "answer": "PUT replaces the entire resource representation; PATCH applies partial modifications to specific fields",
                    "explanation": "According to RFC 7231, PUT replaces the complete target resource with the uploaded payload (missing fields are set to null). PATCH applies partial modifications, updating only the specific fields specified in the request body."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Cisco",
                    "question": "What is the Martin Fowler 'Test Automation Pyramid', and why should API tests outnumber UI tests?",
                    "model_answer": "The Test Automation Pyramid dictates having a broad base of fast, cheap Unit Tests (70%), a strong middle layer of Integration and API Tests (20%), and a lean top layer of End-to-End UI Tests (10%). API tests outnumber UI tests because: 1) Speed: API tests execute in milliseconds compared to seconds/minutes for browser automation; 2) Reliability: API tests bypass browser rendering, CSS animation delays, and network timeouts, making them virtually non-flaky; 3) Root Cause Isolation: When an API test fails, the exact endpoint, request payload, and status code pinpoint the exact bug immediately.",
                    "interviewer_tip": "Cite the inverted 'Ice Cream Cone' anti-pattern as a warning against UI-heavy testing."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Test Automation Framework Architecture: PyTest, TestNG & Data-Driven Testing",
        "key_takeaways": "Master framework design, annotations/fixtures, parallel test execution, data-driven parameterization, and Allure rich reporting.",
        "topics": [
            "Test Framework Architecture: Test Runner, Page Objects, Utilities, Config Manager, Reporting",
            "PyTest Deep Dive: Fixtures (scope: function, class, module, session), autouse, yield cleanup",
            "TestNG Framework (Java): Annotations (@Test, @BeforeMethod, @DataProvider), testng.xml suites",
            "Data-Driven Testing (DDT): Parameterization via CSV, Excel (Apache POI), JSON & Database queries",
            "Test Reporting & CI Integration: Allure Reports, ExtentReports, JUnit XML & Slack notification webhooks"
        ],
        "sections": {
            "concept": "A professional Test Automation Framework is an organized set of guidelines, concepts, and modular components designed to support automated testing. Core components include: Config Manager (reading environment properties and base URLs), WebDriver Manager (handling browser binaries), Utilities (database connections, screenshot capture on failure), and Report Engine. In PyTest, `fixtures` manage setup and teardown cleanly using `yield`. Data-Driven Testing (DDT) executes the same test logic against dozens of external test data rows (CSV/Excel), separating test code from business data inputs.",
            "formulas": "1. Parallel Test Execution Speedup: Speedup = T_sequential / (T_sequential / Num_Threads) * Thread_Efficiency\n2. Fixture Lifecycle: Code before `yield` = Setup; Code after `yield` = Teardown\n3. Data Provider Combinations: Total_Tests = Rows_in_Dataset * Scenarios",
            "solved_examples": [
                {
                    "title": "Writing a Parameterized Data-Driven Test in PyTest with Setup/Teardown Fixture",
                    "difficulty": "Medium | ThoughtWorks, EPAM, Infosys",
                    "problem": "Write a PyTest script that tests discount calculation across 4 different customer tiers using `@pytest.mark.parametrize`.",
                    "step_by_step": [
                        "Step 1: Define a session or function fixture that initializes the discount engine.",
                        "Step 2: Apply `@pytest.mark.parametrize` with argument names and tuples of inputs and expected outputs.",
                        "Step 3: PyTest executes the test 4 distinct times with clear individual reporting.",
                        "Step 4: All tests pass cleanly in parallel."
                    ],
                    "code_or_math": "import pytest\n\ndef calculate_discount(tier, amount):\n    rates = {'Bronze': 0.05, 'Silver': 0.10, 'Gold': 0.20, 'Platinum': 0.30}\n    return amount * rates.get(tier, 0.0)\n\n@pytest.mark.parametrize('tier, amount, expected', [\n    ('Bronze', 1000, 50.0),\n    ('Silver', 1000, 100.0),\n    ('Gold', 1000, 200.0),\n    ('Platinum', 1000, 300.0)\n])\ndef test_discounts(tier, amount, expected):\n    assert calculate_discount(tier, amount) == expected"
                }
            ],
            "practice_questions": [
                {
                    "question": "In the PyTest testing framework, what is the default scope of a fixture if the `scope` parameter is not explicitly defined?",
                    "options": [
                        "session",
                        "module",
                        "function",
                        "package"
                    ],
                    "answer": "function",
                    "explanation": "The default scope of a PyTest fixture is `function`. The fixture runs setup before each test function starts and executes teardown after the test function finishes."
                }
            ],
            "interview_questions": [
                {
                    "company": "EPAM & ThoughtWorks",
                    "question": "How do you capture screenshots automatically only when a Selenium automated test fails, without cluttering passing test logs?",
                    "model_answer": "In PyTest, implement a custom hook in `conftest.py` using `pytest_runtest_makereport(item, call)`. When a test finishes execution, the hook inspects `call.excinfo`. If an exception is detected and `report.failed` is true, the hook retrieves the WebDriver instance from the test item, calls `driver.save_screenshot('failures/' + item.name + '.png')`, and attaches the image directly to the Allure HTML report. In Java TestNG, implement the `ITestListener` interface and override the `onTestFailure(ITestResult result)` method.",
                    "interviewer_tip": "Cite `pytest_runtest_makereport` hook to show deep framework internals knowledge."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Performance, Load & Stress Testing with Apache JMeter & Locust",
        "key_takeaways": "Master Performance metrics (Throughput, Response Time, Concurrency), JMeter Thread Groups, Locust Python load tests, and bottleneck identification.",
        "topics": [
            "Performance Testing Paradigms: Load Testing vs Stress Testing vs Soak/Endurance vs Spike Testing",
            "Key Performance Metrics: Throughput (TPS / RPS), Latency, Response Time, Error Rate & Percentiles",
            "Apache JMeter: Thread Groups, HTTP Request Samplers, Timers (Pacing), Assertions & Listeners",
            "Locust Framework: Code-based Python load testing, HttpUser, `@task` weights & distributed workers",
            "System Bottleneck Analysis: CPU saturation, Memory leaks, Database connection pool exhaustion & slow queries"
        ],
        "sections": {
            "concept": "Performance testing evaluates how systems behave under normal and peak transaction loads. Load Testing verifies application performance under anticipated normal user volumes. Stress Testing pushes systems beyond operational limits until breaking point to verify graceful degradation and recovery. Spike Testing simulates sudden surges (e.g. Black Friday ticket drops). Apache JMeter uses multi-threaded virtual users simulating HTTP requests. Locust allows writing performance tests purely in Python using lightweight gevent coroutines, enabling a single test generator machine to simulate tens of thousands of concurrent users.",
            "formulas": "1. Throughput (TPS) = Completed_Transactions / Total_Test_Duration_Seconds\n2. Little's Law in Performance Engineering: N = X * R (Concurrent_Users = Throughput * Response_Time)\n3. Degradation Knee: The point where throughput plateaus and response time increases exponentially",
            "solved_examples": [
                {
                    "title": "Writing a Scalable Code-Based Load Test Script in Python with Locust",
                    "difficulty": "Medium | Amazon, Hotstar, Swiggy",
                    "problem": "Create a Locust load test script simulating 10,000 users browsing products (weight 4) and checking out (weight 1) with 1-3 second pacing.",
                    "step_by_step": [
                        "Step 1: Define class inheriting from `HttpUser`.",
                        "Step 2: Configure pacing delay using `between(1, 3)` seconds.",
                        "Step 3: Define `@task(4)` for browsing products (`GET /api/v1/products`).",
                        "Step 4: Define `@task(1)` for checkout order creation (`POST /api/v1/orders`).",
                        "Step 5: Run with `locust -f locustfile.py --users 1000 --spawn-rate 50 --headless -t 5m`."
                    ],
                    "code_or_math": "from locust import HttpUser, task, between\n\nclass StoreUser(HttpUser):\n    wait_time = between(1, 3)\n    \n    @task(4)\n    def browse_products(self):\n        self.client.get('/api/v1/products')\n        \n    @task(1)\n    def checkout(self):\n        self.client.post('/api/v1/orders', json={'item_id': 101, 'qty': 1})"
                }
            ],
            "practice_questions": [
                {
                    "question": "According to Little's Law (N = X * R), if a web application handles an average response time of 0.5 seconds and an arrival throughput of 400 requests per second, how many concurrent active users are on the system?",
                    "options": [
                        "100 users",
                        "200 users",
                        "800 users",
                        "4,000 users"
                    ],
                    "answer": "200 users",
                    "explanation": "Little's Law states N = X * R, where N is concurrent requests, X is throughput (400 req/sec), and R is average response time (0.5 sec). N = 400 * 0.5 = 200 concurrent active requests."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Swiggy",
                    "question": "What is the difference between an Endurance (Soak) Test and a Spike Test?",
                    "model_answer": "An Endurance (Soak) test runs a system under a sustained moderate load over a long period (e.g. 24 to 72 hours) specifically to discover slow memory leaks, database connection pool exhaustion, file descriptor leaks, and buffer bloat that only manifest over time. A Spike test suddenly subjects the system to an abrupt, dramatic surge in traffic (e.g. jumping from 500 users to 50,000 users in 30 seconds) to test auto-scaling responsiveness, circuit breakers, and queue buffering.",
                    "interviewer_tip": "Cite memory leaks for Soak tests and auto-scaling response for Spike tests."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Modern Web Automation with Playwright & Cypress: Fast, Parallel & Resilient Testing",
        "key_takeaways": "Master modern headless browser automation with Playwright (Chrome, WebKit, Firefox), auto-waiting, network mocking, and Cypress architecture.",
        "topics": [
            "Limitations of legacy Selenium: Flakiness, external driver management & slow HTTP polling",
            "Microsoft Playwright Architecture: DevTools Protocol (CDP), web sockets & multi-browser engine (Chromium, Firefox, WebKit)",
            "Playwright Auto-Waiting: Automatic element actionability checks (visible, stable, enabled, editable)",
            "Network Interception & API Mocking: `page.route()`, modifying responses & simulating offline states",
            "Cypress Architecture: Running inside the browser run-loop, automatic time-travel & DOM snapshots"
        ],
        "sections": {
            "concept": "Modern web development (React, Angular, Vue single-page apps) exposed the limitations of legacy Selenium, such as explicit wait boilerplate and flaky HTTP polling. Microsoft Playwright and Cypress represent next-generation test automation tools. Playwright communicates directly with browser engines via bidirectional WebSockets over the Chrome DevTools Protocol (CDP). Playwright features built-in Auto-Waiting: before clicking an element, it automatically checks that the element is attached to DOM, visible, stable (no CSS transitions in progress), enabled, and not obscured by overlays, completely eliminating flakiness. Playwright supports fast network mocking and isolated BrowserContexts for parallel multi-tab and multi-user testing.",
            "formulas": "1. Playwright Actionability Check: Clickable = Attached & Visible & Stable & Enabled & Not_Obscured\n2. BrowserContext Overhead: Creates isolated incognito session in < 5ms without launching new browser process\n3. Parallel Execution Multiplier: Playwright executes 3x to 5x faster than legacy Selenium WebDriver",
            "solved_examples": [
                {
                    "title": "Writing a Resilient Async Automated Test in Python with Playwright",
                    "difficulty": "Medium | Microsoft, Netflix, Meta",
                    "problem": "Write an automated Playwright script that intercepts a payment API call to return a mocked mock response and asserts button state.",
                    "step_by_step": [
                        "Step 1: Launch chromium browser and create isolated browser context.",
                        "Step 2: Intercept `/api/v1/payment` using `page.route()` to return custom mock JSON (`{'status': 'SUCCESS'}`).",
                        "Step 3: Navigate to checkout page.",
                        "Step 4: Click `#checkout-btn` (Playwright auto-waits for clickability).",
                        "Step 5: Assert success banner appears using `expect(page.locator('.success')).to_be_visible()`."
                    ],
                    "code_or_math": "import asyncio\nfrom playwright.async_api import async_playwright, expect\n\nasync def test_mocked_payment():\n    async with async_playwright() as p:\n        browser = await p.chromium.launch(headless=True)\n        page = await browser.new_page()\n        # Network Mocking\n        await page.route('**/api/v1/payment', lambda route: route.fulfill(\n            status=200, content_type='application/json', body='{\"status\": \"PAID\"}'\n        ))\n        await page.goto('https://example.com/checkout')\n        await page.click('#pay-btn') # Auto-waits\n        await browser.close()"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the primary benefit of Playwright's 'Auto-Waiting' feature over Selenium's default behavior?",
                    "options": [
                        "It automatically solves CAPTCHA puzzles",
                        "It automatically checks that an element is attached, visible, stable, enabled, and ready for action before executing clicks or typing, eliminating Thread.sleep and flaky explicit waits",
                        "It converts tests into PDF documents",
                        "It shuts down the computer if a test fails"
                    ],
                    "answer": "It automatically checks that an element is attached, visible, stable, enabled, and ready for action before executing clicks or typing, eliminating Thread.sleep and flaky explicit waits",
                    "explanation": "Playwright performs thorough actionability checks before any user interaction (ensuring the element is visible, stable, enabled, and not covered by animations), rendering tests resilient against race conditions without manual wait statements."
                }
            ],
            "interview_questions": [
                {
                    "company": "Microsoft & Netflix",
                    "question": "What is a 'BrowserContext' in Playwright, and how does it enable ultra-fast parallel testing?",
                    "model_answer": "In traditional Selenium, running tests in parallel requires launching multiple heavy browser processes, consuming gigabytes of RAM. In Playwright, a single browser instance is launched once. Each test runs inside an isolated `BrowserContext`, which behaves like an entirely fresh incognito session with its own independent cookies, cache, local storage, and session tokens. Creating a BrowserContext takes less than 5 milliseconds and minimal memory, allowing dozens of isolated tests to execute in parallel on a single machine.",
                    "interviewer_tip": "Highlight that BrowserContexts avoid the overhead of relaunching browser processes."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Solved SDET Automation Engineering Challenges & Placement Technical Drills",
        "key_takeaways": "Master top SDET placement coding challenges: building custom test runners, visual regression testing, cross-browser Docker grids, and CI/CD quality gates.",
        "topics": [
            "SDET Coding Challenge 1: Implementing a robust dynamic table parser with sorting & pagination validation",
            "SDET Coding Challenge 2: Designing a distributed Dockerized Selenium Grid / Selenoid execution cluster",
            "Visual Regression Testing: Pixel-by-pixel image comparison with Percy / Applitools Eyes",
            "Quality Gates in CI/CD: Blocking deployments on SonarQube quality gate rules & test coverage failures",
            "FAANG SDET placement technical interview questions, scenario drills & architecture defense matrices"
        ],
        "sections": {
            "concept": "Software Development Engineer in Test (SDET) placement interviews test both advanced programming skills (data structures, algorithms) and deep automated testing architecture. Candidates must write clean, maintainable automation code, handle dynamic web tables with pagination, and implement visual regression testing (pixel-by-pixel image diffing). Quality gates in CI/CD pipelines automate deployment criteria: code must pass 100% of unit and API tests, maintain >80% code coverage, pass SonarQube static security analysis with zero Critical/Blocker bugs, and complete performance benchmarks before merging to production.",
            "formulas": "1. Visual Difference Percentage = (Changed_Pixels / Total_Image_Pixels) * 100 (Threshold typically < 0.1%)\n2. Flaky Test Score = (Flaky_Runs / Total_Executions) * 100 (Flaky tests auto-quarantined if > 2%)\n3. Quality Gate Rule: Status = Pass if (Coverage >= 80% & Blockers == 0 & Security_Rating == 'A') else Fail",
            "solved_examples": [
                {
                    "title": "Solving the Dynamic HTML Table Pagination SDET Coding Challenge",
                    "difficulty": "Hard | Amazon, Google, Microsoft",
                    "problem": "Write an automation algorithm that traverses all pages of a dynamic paginated web table to locate a row matching a customer ID and extract their transaction status.",
                    "step_by_step": [
                        "Step 1: Enter loop while Next Page button is enabled.",
                        "Step 2: Scrape all rows on current table page into list of text values.",
                        "Step 3: Search for target Customer ID in first column.",
                        "Step 4: If found, extract and return transaction status from column 4.",
                        "Step 5: If not found, click Next Page button, wait for table refresh, and repeat. Return None if last page reached."
                    ],
                    "code_or_math": "def find_customer_status(driver, target_id):\n    while True:\n        rows = driver.find_elements('css selector', 'table#orders tbody tr')\n        for row in rows:\n            cols = row.find_elements('tag name', 'td')\n            if cols and cols[0].text.strip() == target_id:\n                return cols[3].text.strip() # Found status\n        next_btn = driver.find_elements('css selector', 'button.next-page:not([disabled])')\n        if not next_btn:\n            break # Reached last page\n        next_btn[0].click()\n        # wait for table update\n    return None"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is a 'Test Quarantine' policy in enterprise automated CI/CD pipelines?",
                    "options": [
                        "Isolating infected computers with computer viruses",
                        "Automatically detecting intermittently failing (flaky) tests, removing them from the blocking build pipeline, and placing them in an isolated monitoring suite until fixed",
                        "Shutting down the testing team for two weeks",
                        "Encrypting all test scripts with passwords"
                    ],
                    "answer": "Automatically detecting intermittently failing (flaky) tests, removing them from the blocking build pipeline, and placing them in an isolated monitoring suite until fixed",
                    "explanation": "A single flaky test can block continuous deployment pipelines and destroy developer trust in automation. A quarantine policy moves intermittently failing tests out of the critical deployment path to a separate non-blocking suite until the root cause is resolved."
                }
            ],
            "interview_questions": [
                {
                    "company": "Amazon & Google",
                    "question": "What makes an engineer an SDET (Software Development Engineer in Test) rather than a traditional QA tester?",
                    "model_answer": "An SDET is a software developer whose primary product is test automation software, framework architecture, and developer productivity tooling. While traditional manual QA focuses on black-box test execution and bug reporting, an SDET writes production-grade code, designs distributed test frameworks, builds CI/CD quality gates, profiles performance bottlenecks, analyzes database deadlock queries, and collaborates closely with backend developers to build testability directly into software architectures.",
                    "interviewer_tip": "Emphasize writing software that tests software and building developer productivity tools."
                }
            ]
        }
    }
]
