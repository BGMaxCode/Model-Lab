# Software Engineering Architectures & DFD-to-Architecture Conversion

---

## Table of Contents

1. [What is Software Architecture?](#1-what-is-software-architecture)
2. [Types of Software Engineering Architectures](#2-types-of-software-engineering-architectures)
   - 2.1 Layered (N-Tier) Architecture
   - 2.2 Client-Server Architecture
   - 2.3 Microservices Architecture
   - 2.4 Event-Driven Architecture
   - 2.5 Monolithic Architecture
   - 2.6 Service-Oriented Architecture (SOA)
   - 2.7 Serverless Architecture
   - 2.8 Pipe and Filter Architecture
   - 2.9 Repository / Blackboard Architecture
   - 2.10 Broker Architecture
   - 2.11 Model-View-Controller (MVC) Architecture
   - 2.12 Model-View-ViewModel (MVVM) Architecture
   - 2.13 Hexagonal (Ports & Adapters) Architecture
   - 2.14 CQRS Architecture
   - 2.15 Space-Based Architecture
3. [Data Flow Diagrams (DFD) — Overview](#3-data-flow-diagrams-dfd--overview)
4. [Converting DFD to Software Architecture](#4-converting-dfd-to-software-architecture)
   - 4.1 General Conversion Steps
   - 4.2 DFD → Layered Architecture
   - 4.3 DFD → Client-Server Architecture
   - 4.4 DFD → Microservices Architecture
   - 4.5 DFD → Pipe and Filter Architecture
   - 4.6 DFD → Event-Driven Architecture
   - 4.7 DFD → MVC Architecture
5. [Comparison Table](#5-comparison-table)
6. [Choosing the Right Architecture](#6-choosing-the-right-architecture)

---

## 1. What is Software Architecture?

Software architecture is the high-level structure of a software system — the collection of software elements, the relations among them, and the properties of both. It defines how components interact, how data flows, how concerns are separated, and how the system will evolve over time.

A good architecture:
- Separates concerns cleanly
- Enables scalability, maintainability, and testability
- Communicates design intent clearly to stakeholders
- Guides technology choices and team organization

---

## 2. Types of Software Engineering Architectures

---

### 2.1 Layered (N-Tier) Architecture

**Definition:** Organizes the system into horizontal layers, each with a specific role. Each layer only communicates with the layer directly above or below it.

**Typical Layers:**
- **Presentation Layer** — UI, user interaction
- **Business Logic Layer** — Application rules, workflows
- **Data Access Layer** — Database queries, ORM
- **Database Layer** — Persistent storage

**When to Use:**
- Enterprise applications (ERP, CRM)
- Applications with clear separation of concerns
- Teams with functional specialization (frontend, backend, DBA)

**Pros:** Simple to understand, easy to test layers in isolation, supports parallel development.

**Cons:** Can lead to unnecessary coupling between layers; tight layering can slow down data-heavy operations.

**Example:** Traditional web apps built with MVC frameworks (Spring MVC, Django, Rails).

---

### 2.2 Client-Server Architecture

**Definition:** Divides the system into two roles — **clients** that request services and **servers** that provide them. Communication typically happens over a network.

**Variants:**
- 2-Tier: Client talks directly to the database
- 3-Tier: Client → Application Server → Database
- N-Tier: Multiple intermediate layers

**When to Use:**
- Web applications, mobile backends, REST APIs
- Centralized data management
- Multiple clients sharing a common backend

**Pros:** Centralized control, easy updates on server side, good for multi-client scenarios.

**Cons:** Server becomes a single point of failure; network latency affects performance.

---

### 2.3 Microservices Architecture

**Definition:** Structures an application as a collection of small, independently deployable services, each responsible for a specific business capability and communicating via APIs.

**Key Characteristics:**
- Each service has its own database
- Services communicate via REST, gRPC, or message queues
- Independent deployment and scaling of each service
- Organized around business domains (DDD)

**When to Use:**
- Large-scale applications needing independent scaling
- Teams that want independent release cycles
- Systems that evolve rapidly (e-commerce, SaaS platforms)

**Pros:** Independent scaling, technology diversity, fault isolation, faster deployments.

**Cons:** Complex distributed systems, data consistency challenges, operational overhead (service discovery, monitoring).

**Example:** Netflix, Amazon, Uber.

---

### 2.4 Event-Driven Architecture (EDA)

**Definition:** Components communicate by producing and consuming **events** (messages about things that have happened). No direct coupling between producers and consumers.

**Core Components:**
- **Event Producers** — Emit events when something happens
- **Event Brokers/Bus** — Route events (Kafka, RabbitMQ, AWS SNS/SQS)
- **Event Consumers** — React to events asynchronously

**Patterns:**
- **Pub/Sub** — One event, multiple consumers
- **Event Sourcing** — State derived from a log of events
- **CQRS + EDA** — Combined for read/write separation

**When to Use:**
- Real-time data streaming, IoT
- Loosely coupled systems
- Workflows with asynchronous processing (order fulfillment, notifications)

**Pros:** High decoupling, scalable, supports async processing.

**Cons:** Harder to debug, eventual consistency challenges, complex error handling.

---

### 2.5 Monolithic Architecture

**Definition:** The entire application is built, deployed, and run as a single unit. All functionality — UI, business logic, and data access — exists in one codebase and process.

**When to Use:**
- Small teams, early-stage startups
- Simple applications with limited scope
- When simplicity is preferred over scalability

**Pros:** Simple to develop and deploy, easy to test end-to-end, low operational overhead.

**Cons:** Hard to scale individual components, tight coupling, long build times as system grows.

---

### 2.6 Service-Oriented Architecture (SOA)

**Definition:** Structures software as a set of interoperable services that communicate through a shared middleware layer, typically an **Enterprise Service Bus (ESB)**.

**Difference from Microservices:**
- SOA services are coarser-grained (larger, may share databases)
- Uses centralized ESB vs. decentralized communication in microservices
- Targets enterprise integration across heterogeneous systems

**When to Use:**
- Large enterprise environments with legacy systems
- Cross-department system integration
- B2B integration via standard protocols (SOAP, WSDL)

**Pros:** Reusability of services, interoperability, enterprise-wide integration.

**Cons:** ESB can become a bottleneck, heavy XML/SOAP overhead, complex governance.

---

### 2.7 Serverless Architecture

**Definition:** Application logic is deployed as individual functions (Function-as-a-Service) that are triggered by events and executed on cloud-managed infrastructure. No server management by the developer.

**Key Providers:** AWS Lambda, Azure Functions, Google Cloud Functions

**When to Use:**
- Applications with sporadic or variable workloads
- Rapid prototyping and MVPs
- Event-triggered tasks (file uploads, API requests, scheduled jobs)

**Pros:** No server management, pay-per-use, automatic scaling.

**Cons:** Cold start latency, vendor lock-in, difficulty with long-running tasks, limited local testing.

---

### 2.8 Pipe and Filter Architecture

**Definition:** Data flows through a sequence of processing steps (**filters**) connected by channels (**pipes**). Each filter transforms the data and passes it to the next.

**Key Components:**
- **Pipes** — Data channels (often buffered queues)
- **Filters** — Independently operating transformations
- **Data Sources / Sinks** — Start and end of the pipeline

**When to Use:**
- ETL (Extract, Transform, Load) pipelines
- Compilers and interpreters
- Signal/image processing
- Data streaming systems

**Pros:** Easy to add/reorder processing steps, filters are reusable and testable in isolation.

**Cons:** Not suitable for interactive systems, overhead from data marshaling between filters.

---

### 2.9 Repository / Blackboard Architecture

**Definition:** A central data store (**repository** or **blackboard**) is shared by multiple independent components that read from and write to it.

**Variants:**
- **Repository** — Components are triggered by client requests
- **Blackboard** — Components are triggered by changes in the data store (opportunistic problem-solving)

**When to Use:**
- AI/knowledge-based systems
- Compilers (symbol tables)
- Complex search and optimization problems (scheduling, robotics)

**Pros:** Decoupled components, shared data access, supports collaborative problem solving.

**Cons:** Central store is a bottleneck and single point of failure; concurrency management is complex.

---

### 2.10 Broker Architecture

**Definition:** A **broker** component is responsible for coordinating communication between clients and servers. Clients don't know where services are located.

**When to Use:**
- Distributed systems where location transparency is needed
- Middleware platforms (CORBA, Java RMI, message brokers)
- Systems requiring dynamic service discovery

**Pros:** Decouples clients from server implementations, supports load balancing and failover.

**Cons:** Broker is a single point of failure; adds latency.

---

### 2.11 Model-View-Controller (MVC) Architecture

**Definition:** Separates application into three interconnected components:
- **Model** — Data and business logic
- **View** — User interface rendering
- **Controller** — Handles user input, updates Model and View

**When to Use:**
- Web applications (Django, Rails, Spring MVC, ASP.NET MVC)
- Desktop GUI applications

**Pros:** Clear separation of concerns, supports parallel UI and backend development, testable.

**Cons:** Can become complex with large controllers; View and Controller often tightly coupled in practice.

---

### 2.12 Model-View-ViewModel (MVVM) Architecture

**Definition:** Evolution of MVC for data-binding-heavy UIs:
- **Model** — Data and business rules
- **View** — UI elements (declarative)
- **ViewModel** — Exposes data streams and commands; two-way data binding

**When to Use:**
- Modern frontend frameworks (Angular, Vue.js, React with state management, WPF, Xamarin)

**Pros:** Clean separation, testable ViewModels, efficient data binding.

**Cons:** Overhead for simple UIs; data binding can be hard to debug.

---

### 2.13 Hexagonal (Ports & Adapters) Architecture

**Definition:** Places the business logic at the center, surrounded by **ports** (interfaces) and **adapters** (implementations). External concerns (UI, database, messaging) interact with the core only through defined ports.

**When to Use:**
- Domain-driven applications requiring high testability
- Applications that need to swap out infrastructure (e.g., change DB from MySQL to MongoDB)
- Microservices with clean domain boundaries

**Pros:** Highly testable core, infrastructure-agnostic, clear boundaries.

**Cons:** More upfront design effort; more abstractions to manage.

---

### 2.14 CQRS (Command Query Responsibility Segregation)

**Definition:** Separates the **read model** (queries) from the **write model** (commands). Each can have its own database, optimized independently.

**When to Use:**
- Systems with very different read and write workloads
- Combined with Event Sourcing for audit trails
- High-performance reporting alongside transactional systems

**Pros:** Independent optimization of reads and writes, scalable, supports complex domain logic.

**Cons:** Eventual consistency between read/write sides; increased complexity.

---

### 2.15 Space-Based Architecture

**Definition:** Eliminates the database as the central bottleneck by distributing both processing and storage across a **tuple space** (in-memory data grid). Multiple processing units share data via a distributed memory grid.

**When to Use:**
- High-throughput, high-scalability applications (auction sites, stock tickers, online gaming)
- Applications where database becomes a bottleneck under peak load

**Pros:** Near-linear scalability, eliminates database bottleneck.

**Cons:** Complex to implement, eventual consistency, data loss risk without persistence strategy.

---

## 3. Data Flow Diagrams (DFD) — Overview

A **Data Flow Diagram (DFD)** is a graphical representation of how data moves through a system. It shows:

| Symbol | Meaning |
|--------|---------|
| Rectangle / Square | **External Entity** — Data source or sink (user, external system) |
| Rounded Rectangle / Circle | **Process** — Transforms input data into output |
| Open-ended Rectangle | **Data Store** — Where data is stored (database, file) |
| Arrow | **Data Flow** — Direction and name of data movement |

**DFD Levels:**
- **Context Diagram (Level 0)** — Entire system as a single process, showing external entities
- **Level 1 DFD** — Major sub-processes and data stores
- **Level 2 DFD** — Further decomposition of each Level 1 process

---

## 4. Converting DFD to Software Architecture

Converting a DFD into a software architecture is a systematic process of mapping DFD elements to architectural components.

---

### 4.1 General Conversion Steps

#### Step 1: Analyze the DFD

- Identify all **external entities** (users, external systems)
- Identify all **processes** and group related ones
- Identify all **data stores**
- Trace all **data flows** and identify direction, volume, and frequency

#### Step 2: Identify Architectural Drivers

Ask:
- Is the system data-intensive or process-intensive?
- Are processes tightly or loosely coupled?
- Are there clear input→transform→output pipelines?
- Do external entities initiate actions (request-driven) or does data drive behavior?
- Are there time-critical or asynchronous flows?

#### Step 3: Map DFD Elements to Architecture Components

| DFD Element | Architectural Counterpart |
|-------------|--------------------------|
| External Entity | Client, External API, UI Layer, Third-party service |
| Process | Module, Service, Microservice, Controller, Function |
| Data Store | Database, Cache, File System, Message Queue |
| Data Flow | API call, Message, Event, Method call, Data stream |

#### Step 4: Group Processes into Architectural Units

- Cluster tightly related processes into **layers**, **services**, or **modules**
- Processes sharing the same data store often belong in the same service or layer
- Processes that are sequential with linear data flow suggest a **pipe and filter** design
- Processes triggered by events suggest **event-driven** design

#### Step 5: Identify Interfaces

- Data flows crossing group boundaries become **APIs**, **events**, or **message contracts**
- Define the interface type: synchronous (REST, gRPC) or asynchronous (queue, event bus)

#### Step 6: Map Data Stores to Storage Solutions

| Data Store Characteristic | Recommended Storage |
|--------------------------|---------------------|
| Structured, relational | Relational DB (PostgreSQL, MySQL) |
| Flexible schema | NoSQL (MongoDB, DynamoDB) |
| High-speed reads | Cache (Redis, Memcached) |
| Ordered event log | Message Queue (Kafka, RabbitMQ) |
| Files/blobs | Object Storage (S3, Azure Blob) |

#### Step 7: Define Non-Functional Architecture Concerns

Based on DFD data volume and flow frequency, address: scalability, fault tolerance, security boundaries, and deployment units.

---

### 4.2 DFD → Layered Architecture

**When DFD Suggests Layered:**
- External entities are **users or UI clients**
- Processes clearly separate into user-facing, logic-processing, and data-access categories
- Data flows top-down (entity → process → store)

**Conversion Mapping:**

```
External Entity (User)  →  Presentation Layer
Process (Validate, Compute, Route)  →  Business Logic Layer
Process (Query, Update)  →  Data Access Layer
Data Store  →  Database Layer
```

**Steps:**
1. Place all user-facing processes in the **Presentation Layer**
2. Group domain logic processes into the **Business/Service Layer**
3. Move all data store interaction processes into the **Repository/DAO Layer**
4. Data flows between DFD processes become **method calls** between layers
5. Apply the **dependency rule**: upper layers depend on lower, never the reverse

**Example:**

```
DFD:  User → [Login Process] → [Validate Credentials] → User Store

Layered:
  Presentation:  LoginController (handles HTTP request)
  Business:      AuthService (validates credentials, generates token)
  Data Access:   UserRepository (queries User Store)
  Database:      users table
```

---

### 4.3 DFD → Client-Server Architecture

**When DFD Suggests Client-Server:**
- Multiple external entities send requests to centralized processes
- Data stores are centralized and shared
- Data flows are request-response in nature

**Conversion Mapping:**

```
External Entity  →  Client Application
Centralized Processes  →  Server / API Layer
Data Stores  →  Server-side Databases
Data Flows  →  HTTP / TCP / WebSocket requests
```

**Steps:**
1. Group all external entities into **client types** (web browser, mobile app, desktop app)
2. Move all processes to the **server side**
3. Define **API endpoints** for each data flow from client to server
4. Data stores remain on the **server side**
5. Apply authentication/authorization at the server boundary

---

### 4.4 DFD → Microservices Architecture

**When DFD Suggests Microservices:**
- Processes fall into distinct **business domain clusters**
- Different processes access different data stores (no shared DB)
- Some processes need independent scalability
- Loose coupling between process clusters

**Conversion Mapping:**

```
Process Cluster (same domain)  →  Microservice
Data Store per Cluster  →  Service-owned Database
Data Flow between Clusters  →  REST API or Message Queue
External Entity  →  API Gateway / Client
```

**Steps:**
1. Use **Domain-Driven Design** to identify bounded contexts in the DFD
2. Assign each bounded context (cluster of related processes) to a **separate microservice**
3. Each microservice owns its data store — no sharing
4. Cross-service data flows become **synchronous API calls** (REST/gRPC) or **asynchronous messages** (Kafka/RabbitMQ)
5. External entities interact via an **API Gateway** that routes to services
6. Introduce **service discovery**, **circuit breakers**, and **distributed tracing** for operational readiness

**Example:**

```
DFD Clusters:
  [Register User, Login, Reset Password] → User Store
  [Place Order, Cancel Order] → Order Store
  [Process Payment, Refund] → Payment Store

Microservices:
  user-service     ← manages user-service DB
  order-service    ← manages order-service DB
  payment-service  ← manages payment-service DB
  API Gateway      ← routes external entity requests
```

---

### 4.5 DFD → Pipe and Filter Architecture

**When DFD Suggests Pipe and Filter:**
- Data flows in a **linear, sequential** path through multiple processes
- Each process takes input data, transforms it, and passes it on
- Processes are largely independent (no shared state)
- No user interaction mid-pipeline

**Conversion Mapping:**

```
Sequential Process Chain  →  Filter Sequence
Data Flow between Processes  →  Pipe (buffer/queue/stream)
Initial External Entity  →  Data Source
Final Data Store  →  Data Sink
```

**Steps:**
1. Identify the **start source** (data input point) and **end sink** (output or storage)
2. Map each process in the chain to a **filter** with defined input/output schema
3. Connect filters with **pipes** — can be in-memory channels, file streams, or message queues
4. Ensure each filter has a **single responsibility** and is independently replaceable
5. Introduce **parallel pipes** if the DFD shows branching paths

**Example:**

```
DFD: Raw Log File → [Parse] → [Filter Errors] → [Enrich] → [Store] → Analytics DB

Pipeline:
  Source: Raw Log Stream
  Filter 1: LogParser
  Filter 2: ErrorFilter
  Filter 3: MetadataEnricher
  Sink: AnalyticsDatabase
```

---

### 4.6 DFD → Event-Driven Architecture

**When DFD Suggests Event-Driven:**
- Data flows are **asynchronous** or **triggered by state changes**
- Multiple processes react to the same data change
- Processes are loosely coupled with no direct call dependency
- DFD shows a **fan-out** pattern (one process triggers many)

**Conversion Mapping:**

```
State-Changing Process  →  Event Producer
Data Flow (fan-out)  →  Event (message on broker)
Reacting Processes  →  Event Consumers / Subscribers
Data Store  →  Consumer-owned Store or Event Log
```

**Steps:**
1. Identify processes that represent **domain events** (OrderPlaced, PaymentReceived, UserSignedUp)
2. Map those processes to **event producers**
3. Identify downstream processes that react and map them to **consumers**
4. Introduce an **event broker** (Kafka, RabbitMQ) as the intermediary
5. Each consumer maintains its own state in its own data store
6. Apply the **at-least-once / exactly-once delivery** strategy based on criticality

---

### 4.7 DFD → MVC Architecture

**When DFD Suggests MVC:**
- External entity is a **user interacting with a UI**
- Processes handle **user input**, **business operations**, and **data retrieval**
- Data stores back the UI with structured data

**Conversion Mapping:**

```
External Entity (User Input)  →  View (UI)
Input-Handling Process  →  Controller
Business Logic Process  →  Model (or Service)
Data Store  →  Model / Repository
```

**Steps:**
1. Map every user-facing data flow to a **View** component
2. Map every input-processing step to a **Controller** action
3. Map domain logic processes and data stores to the **Model** layer
4. Establish the MVC cycle: View sends input → Controller processes → Model updates → View re-renders

**Example:**

```
DFD: User → [Submit Form] → [Validate & Save] → Product Store

MVC:
  View:        ProductForm.html (renders form, displays errors)
  Controller:  ProductController.submitForm() (receives POST, calls service)
  Model:       Product, ProductRepository (business rules + DB access)
```

---

## 5. Comparison Table

| Architecture | Coupling | Scalability | Complexity | Best For |
|---|---|---|---|---|
| Layered | Medium | Vertical | Low | Enterprise apps, CRUD systems |
| Client-Server | Medium | Moderate | Low | Web/mobile backends |
| Microservices | Low | High | High | Large-scale distributed systems |
| Event-Driven | Very Low | Very High | High | Real-time, async systems |
| Monolithic | High | Low | Very Low | Small apps, MVPs |
| SOA | Medium | Moderate | High | Enterprise integration |
| Serverless | Very Low | Auto | Medium | Event-triggered functions |
| Pipe & Filter | Low | Moderate | Low | Data pipelines, ETL |
| Repository | Medium | Low | Medium | AI/knowledge systems |
| Broker | Low | High | Medium | Distributed middleware |
| MVC | Medium | Moderate | Low | Web/GUI applications |
| MVVM | Low | Moderate | Medium | Modern frontend (SPA, mobile) |
| Hexagonal | Very Low | Moderate | High | DDD, highly testable systems |
| CQRS | Low | High | High | Read/write asymmetric systems |
| Space-Based | Very Low | Very High | Very High | Ultra-high throughput systems |

---

## 6. Choosing the Right Architecture

Use this decision guide based on your DFD analysis:

```
Is the system simple with a small team?
  → Monolithic Architecture

Is data flowing linearly through transformations?
  → Pipe and Filter Architecture

Are there multiple users interacting with a UI?
  → MVC / MVVM / Layered Architecture

Are there many clients calling shared services?
  → Client-Server Architecture

Are processes grouped into distinct business domains?
  → Microservices Architecture

Do processes react to state changes asynchronously?
  → Event-Driven Architecture

Do you need to integrate legacy enterprise systems?
  → SOA / Broker Architecture

Is the workload sporadic and event-triggered?
  → Serverless Architecture

Is the domain complex with strict testability needs?
  → Hexagonal Architecture

Are read and write volumes very different?
  → CQRS Architecture

Does the system need extreme throughput and scalability?
  → Space-Based Architecture
```

---

*This document covers the principal software engineering architecture styles and provides a systematic methodology for deriving architecture from Data Flow Diagrams (DFDs). Architecture selection should always account for team size, operational capability, business domain complexity, and long-term maintenance considerations.*
