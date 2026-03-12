---
name: ai-native-dev
description: Comprehensive AI-Native system development and deployment planning through interactive Q&A. Use when users want to design AI-powered applications with AI Agents, plan microservice architectures, define APIs, select technology stacks, design agent workflows, and plan Kubernetes deployments. Guides users through structured decision-making from system design to deployment documentation.
---

# AI-Native System Development & Deployment Skill

This skill provides a structured workflow for guiding users through the complete development lifecycle of AI-Native systems—from architecture design through Kubernetes deployment—via interactive Q&A. It ensures consistent decision-making at every stage.

## When to Trigger This Skill

**Trigger conditions:**
- User mentions AI-Native development: "build an AI app", "create AI-powered system", "develop with AI agents"
- User mentions agent design: "design AI agents", "plan agent architecture", "agent workflows"
- User mentions AI system architecture: "AI microservices", "LLM integration", "agentic system"
- User wants end-to-end planning: "plan my AI app from design to deployment"
- User asks about AI patterns: "how should I structure my AI app", "agent communication patterns"

## Design Principles (Apply Consistently)

| Principle | Decision | Rationale |
|-----------|----------|-----------|
| **Agent Autonomy** | Single-responsibility agents | Each agent has one clear purpose; easier to test and scale |
| **LLM Abstraction** | Provider-agnostic interface | Swap LLM providers without code changes |
| **Communication** | Async-first, sync when needed | AI operations are inherently slow; async prevents blocking |
| **State Management** | Stateless agents, external state | Agents don't hold state; enables horizontal scaling |
| **Error Handling** | Graceful degradation | AI failures shouldn't crash the system |
| **Observability** | Trace every LLM call | Debug AI behavior with full request/response logging |
| **Security** | Secrets in vault, never in code | API keys for LLMs are high-value targets |
| **K8s Services** | ClusterIP for internal traffic | No external exposure for service-to-service |
| **K8s RBAC** | Namespace-scoped, least privilege | Minimize blast-radius |

---

## Workflow Overview (8 Stages)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    AI-NATIVE SYSTEM DEVELOPMENT                         │
├─────────────────────────────────────────────────────────────────────────┤
│  PHASE 1: SYSTEM DESIGN                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │ Stage 1:     │  │ Stage 2:     │  │ Stage 3:     │                  │
│  │ System       │─►│ AI Agent     │─►│ API &        │                  │
│  │ Discovery    │  │ Design       │  │ Endpoints    │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
├─────────────────────────────────────────────────────────────────────────┤
│  PHASE 2: TECHNOLOGY & INTEGRATION                                      │
│  ┌──────────────┐  ┌──────────────┐                                    │
│  │ Stage 4:     │  │ Stage 5:     │                                    │
│  │ Tech Stack   │─►│ Integration  │                                    │
│  │ Selection    │  │ Patterns     │                                    │
│  └──────────────┘  └──────────────┘                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  PHASE 3: KUBERNETES DEPLOYMENT                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                  │
│  │ Stage 6:     │  │ Stage 7:     │  │ Stage 8:     │                  │
│  │ Manifest     │─►│ Config &     │─►│ Networking   │                  │
│  │ Planning     │  │ Secrets      │  │ & RBAC       │                  │
│  └──────────────┘  └──────────────┘  └──────────────┘                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# PHASE 1: SYSTEM DESIGN

## Stage 1: System Discovery

### Goal
Understand the overall system purpose, components, and user interactions.

### Questions to Ask

1. **System Purpose**
   - What problem does this AI-Native system solve?
   - Who are the primary users?

2. **Component Identification**
   - How many applications/services will the system have?
   - Which components are AI-powered vs traditional?

3. **User Interaction Model**
   - How do users interact with the system? (Web UI, API, Chat, CLI)
   - Is there real-time interaction (chat) or batch processing?

4. **External Dependencies**
   - Which external services are required? (LLM providers, databases, third-party APIs)
   - Are there existing systems to integrate with?

5. **Data Flow**
   - What data flows into the system?
   - What outputs does the system produce?

### Output Table: System Overview

```markdown
| Aspect | Description |
|--------|-------------|
| System Name | |
| Purpose | |
| Primary Users | |
| Interaction Model | |
| Component Count | |
| AI-Powered Components | |
| External Dependencies | |
```

### Output Table: Component Registry

```markdown
| Component | Type | AI-Powered | Description |
|-----------|------|------------|-------------|
| | Frontend / Backend / Agent / Service | Yes/No | |
```

---

## Stage 2: AI Agent Design

### Goal
Design AI agents with clear responsibilities, capabilities, and interaction patterns.

### Agent Classification Framework

| Agent Type | Characteristics | Use Case |
|------------|-----------------|----------|
| **Conversational Agent** | Handles natural language dialogue | Chat interfaces, Q&A systems |
| **Task Agent** | Executes specific tasks autonomously | Automation, workflow execution |
| **Orchestrator Agent** | Coordinates multiple agents | Complex multi-step processes |
| **Retrieval Agent** | Fetches and synthesizes information | RAG systems, knowledge bases |
| **Tool-Using Agent** | Calls external tools/APIs | Function calling, integrations |

### Questions to Ask

For each AI agent identified:

1. **Agent Identity**
   - What is the agent's name and primary responsibility?
   - What type of agent is it? (Conversational, Task, Orchestrator, Retrieval, Tool-Using)

2. **LLM Requirements**
   - Which LLM provider will it use? (OpenAI, Anthropic, Azure OpenAI, self-hosted)
   - What model capabilities are needed? (chat, function calling, vision, embeddings)
   - What are the latency requirements? (real-time < 2s, near-real-time < 10s, batch)

3. **Agent Capabilities**
   - What actions can this agent perform?
   - What tools/functions does it have access to?
   - What are its input/output formats?

4. **Agent Boundaries**
   - What should this agent NOT do?
   - What are its failure modes?
   - How should it handle uncertainty?

5. **Agent Communication**
   - Does it communicate with other agents?
   - Does it call backend services?
   - Does it interact directly with users?

### Output Table: Agent Registry

```markdown
| Agent Name | Type | LLM Provider | Model | Latency Req | Description |
|------------|------|--------------|-------|-------------|-------------|
```

### Output Table: Agent Capabilities

```markdown
| Agent Name | Capabilities (Actions) | Tools/Functions | Input Format | Output Format |
|------------|----------------------|-----------------|--------------|---------------|
```

### Output Table: Agent Communication Matrix

```markdown
| Agent | Communicates With | Communication Type | Purpose |
|-------|-------------------|-------------------|---------|
| | User / Agent / Service | Sync / Async / Stream | |
```

### Agent Design Principles (Apply Consistently)

| Principle | Implementation |
|-----------|----------------|
| Single Responsibility | Each agent has ONE primary purpose |
| Stateless Design | No in-memory state; use external storage |
| Graceful Degradation | Return meaningful errors, never crash |
| Timeout Handling | All LLM calls have timeouts (default: 30s) |
| Retry Logic | Exponential backoff for transient failures |
| Token Budgeting | Set max_tokens to control costs |
| Prompt Versioning | Version control all system prompts |

---

## Stage 3: API & Endpoint Design

### Goal
Define all APIs and endpoints for both traditional services and AI agents.

### API Design Framework

| Component Type | Endpoint Pattern | Example |
|----------------|------------------|---------|
| Frontend | Static + Proxy | `/`, `/assets/*`, `/api/*` (proxy) |
| Backend REST | Resource-based | `/api/v1/tasks`, `/api/v1/tasks/{id}` |
| AI Agent (Sync) | Action-based | `/agent/chat`, `/agent/analyze` |
| AI Agent (Stream) | SSE endpoint | `/agent/chat/stream` |
| Notifications | WebSocket/SSE | `/notifications/subscribe` |
| Health Checks | Standard paths | `/health`, `/ready`, `/live` |

### Questions to Ask

For each component:

1. **Endpoint Inventory**
   - What endpoints does this component expose?
   - What HTTP methods are used?
   - What is each endpoint's purpose?

2. **Request/Response**
   - What are the request payload structures?
   - What are the response formats?
   - Are there streaming responses?

3. **Authentication**
   - Which endpoints require authentication?
   - What auth mechanism? (JWT, API Key, OAuth)

4. **Rate Limiting**
   - Should any endpoints be rate-limited?
   - What are the limits? (requests/minute, tokens/day)

### Output Table: Endpoint Registry

```markdown
| Component | Endpoint | Method | Description | Auth Required |
|-----------|----------|--------|-------------|---------------|
```

### Output Table: AI Agent Endpoints (Detailed)

```markdown
| Agent | Endpoint | Method | Input | Output | Streaming | Timeout |
|-------|----------|--------|-------|--------|-----------|---------|
```

---

# PHASE 2: TECHNOLOGY & INTEGRATION

## Stage 4: Technology Stack Selection

### Goal
Select appropriate technologies with consistent decision-making rationale.

### Technology Decision Framework

| Layer | Options | Decision Factors |
|-------|---------|------------------|
| **Frontend** | React, Vue, Next.js, Static | Interactivity needs, SEO, team expertise |
| **Backend** | Node.js, Python, Go, Java | Performance, ecosystem, team expertise |
| **AI/Agent Framework** | LangChain, LlamaIndex, Custom, Semantic Kernel | Complexity, flexibility, vendor lock-in |
| **LLM Provider** | OpenAI, Anthropic, Azure OpenAI, Local | Cost, latency, compliance, capabilities |
| **Message Queue** | None, Redis, RabbitMQ, Kafka | Scale, ordering needs, persistence |
| **Database** | None, PostgreSQL, MongoDB, Redis | Data model, query patterns, scale |
| **Cache** | None, Redis, Memcached | Read patterns, invalidation needs |

### Questions to Ask

1. **Language & Runtime**
   - What programming language(s) for backend services?
   - What framework for AI agents?
   - Frontend technology?

2. **AI Infrastructure**
   - LLM provider selection?
   - Need for embeddings/vector database?
   - Agent orchestration framework?

3. **Data Layer**
   - Is a database needed? Which type?
   - Caching requirements?
   - Message queue for async processing?

4. **Constraints**
   - Team expertise?
   - Compliance requirements?
   - Budget constraints?

### Output Table: Technology Stack

```markdown
| Layer | Technology | Justification |
|-------|------------|---------------|
| Frontend | | |
| Backend Services | | |
| AI Agent Framework | | |
| LLM Provider | | |
| Database | | |
| Cache | | |
| Message Queue | | |
```

---

## Stage 5: Integration Patterns

### Goal
Define how components communicate and integrate.

### Communication Pattern Framework

| Pattern | When to Use | Implementation |
|---------|-------------|----------------|
| **Sync REST** | Simple request-response | HTTP client with timeout |
| **Async Queue** | Fire-and-forget, long processing | Message queue (Redis, RabbitMQ) |
| **Streaming (SSE)** | Real-time AI responses | Server-Sent Events |
| **WebSocket** | Bidirectional real-time | WS connection with heartbeat |
| **Event-Driven** | Loose coupling, multiple consumers | Pub/Sub pattern |

### AI-Specific Integration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **Request-Response** | Sync call to LLM, wait for response | Simple chat, single-turn |
| **Streaming Response** | Token-by-token streaming | Chat UX, long responses |
| **Tool Calling** | LLM calls functions, agent executes | Actions, integrations |
| **Agent Chaining** | Output of one agent feeds another | Complex workflows |
| **Human-in-the-Loop** | Agent requests human approval | High-stakes decisions |

### Questions to Ask

1. **Service Communication**
   - How do services communicate? (REST, gRPC, Queue)
   - Sync or async?
   - Error handling strategy?

2. **AI Integration**
   - How does UI communicate with AI agents? (REST, Stream, WebSocket)
   - How do agents communicate with backend?
   - How do agents call external tools?

3. **Event Handling**
   - Are there events that trigger actions?
   - How are notifications delivered?

### Output Table: Integration Matrix

```markdown
| From | To | Pattern | Protocol | Purpose |
|------|-----|---------|----------|---------|
```

### Output Table: Communication Flow

```markdown
| Flow Name | Steps | Pattern | Description |
|-----------|-------|---------|-------------|
| User Chat | UI → Agent → LLM → Agent → UI | Stream | User sends message, gets streamed response |
```

---

# PHASE 3: KUBERNETES DEPLOYMENT

## Stage 6: Manifest Planning

### Goal
Determine required Kubernetes resources based on system design.

### Manifest Selection Framework

| Component Characteristic | Manifest Type | Rationale |
|--------------------------|---------------|-----------|
| Stateless service | Deployment | Rolling updates, scaling |
| Stateful service (DB) | StatefulSet | Stable identity, ordered |
| Background processor | Deployment + HPA | Scale based on queue depth |
| Scheduled job | CronJob | Periodic execution |
| Per-node requirement | DaemonSet | Logging, monitoring agents |

### Questions to Ask

1. **Workload Types**
   - Confirm workload type for each component
   - Scaling requirements? (replicas, HPA)

2. **Namespace Strategy**
   - Single namespace or multiple?
   - Environment separation? (dev, staging, prod)

3. **Resource Requirements**
   - CPU/Memory requests and limits?
   - GPU requirements for local LLMs?

### Output Table: Manifest Inventory

```markdown
| Category | Manifest Type | Count | Names |
|----------|--------------|-------|-------|
| Workloads | Deployment | | |
| Networking | Service | | |
| Networking | Ingress | | |
| Networking | NetworkPolicy | | |
| Config | ConfigMap | | |
| Config | Secret | | |
| RBAC | ServiceAccount | | |
| RBAC | Role | | |
| RBAC | RoleBinding | | |
```

### Output Table: Deployment Details

```markdown
| Deployment Name | Replicas | Purpose |
|-----------------|----------|---------|
```

---

## Stage 7: Configuration & Secrets

### Goal
Design ConfigMaps and Secrets with security best practices.

### Configuration Classification

| Data Type | Resource | Security Level |
|-----------|----------|----------------|
| Service URLs | ConfigMap | Public |
| Feature flags | ConfigMap | Public |
| Log levels | ConfigMap | Public |
| LLM API keys | Secret | Critical |
| Database credentials | Secret | Critical |
| JWT signing keys | Secret | Critical |
| TLS certificates | Secret (TLS type) | High |

### AI-Native Specific Configuration

| Config Item | Resource | Description |
|-------------|----------|-------------|
| `LLM_API_KEY` | Secret | LLM provider API key |
| `LLM_ORG_ID` | Secret | LLM organization ID |
| `LLM_MODEL_NAME` | ConfigMap | Model identifier (not sensitive) |
| `LLM_TIMEOUT_MS` | ConfigMap | Request timeout |
| `LLM_MAX_TOKENS` | ConfigMap | Token limit per request |
| `LLM_TEMPERATURE` | ConfigMap | Model temperature setting |
| `AGENT_SYSTEM_PROMPT` | ConfigMap | Agent's system prompt (version controlled) |

### Questions to Ask

1. **Per-Component Config**
   - What non-sensitive config does each component need?
   - What environment variables?

2. **Secrets Inventory**
   - What secrets are required?
   - LLM API keys? Database credentials? JWT keys?

3. **Security Approach**
   - Encryption at rest for secrets?
   - External secret manager integration? (Vault, AWS Secrets Manager)

### Output Table: ConfigMaps

```markdown
| ConfigMap Name | Environment Variables | Justification |
|----------------|----------------------|---------------|
```

### Output Table: Secrets

```markdown
| Secret Name | Data Type | Keys | Security Approach | Justification |
|-------------|-----------|------|-------------------|---------------|
```

---

## Stage 8: Networking & RBAC

### Goal
Design secure networking and minimal-privilege access control.

### Service Type Decision (Consistency Rule)

| Scenario | Service Type | Rationale |
|----------|--------------|-----------|
| Internal communication | ClusterIP | Default; no external exposure |
| External access | ClusterIP + Ingress | Centralized TLS, routing |
| Development/testing | NodePort | Simple but not for production |

**Consistency Rule**: Default to ClusterIP for ALL services. Use single Ingress for external access.

### Network Policy Strategy

| Policy Type | Purpose |
|-------------|---------|
| Default Deny | Block all traffic by default |
| Allow Ingress | Whitelist specific ingress sources |
| Allow Egress | Whitelist specific egress destinations |
| LLM Egress | Allow agents to reach external LLM APIs |

### RBAC Blast-Radius Principle

| Scope | When to Use |
|-------|-------------|
| Namespace (Role) | Default; covers 99% of cases |
| Cluster (ClusterRole) | Only for cluster-wide resources |

### Questions to Ask

1. **Service Exposure**
   - Which components need external access?
   - TLS requirements?

2. **Network Policies**
   - Should traffic between services be restricted?
   - External egress requirements? (LLM APIs)

3. **RBAC Needs**
   - Do components need K8s API access?
   - ConfigMap/Secret read access?

### Output Table: Services

```markdown
| Service Name | Type | Justification |
|--------------|------|---------------|
```

### Output Table: Ingress Routes

```markdown
| Host | Path | Backend Service | Description |
|------|------|-----------------|-------------|
```

### Output Table: Network Policies

```markdown
| Policy Name | Pod Selector | Ingress From | Egress To | Justification |
|-------------|--------------|--------------|-----------|---------------|
```

### Output Table: RBAC Artifacts

```markdown
| Type | Name | Scope | Justification |
|------|------|-------|---------------|
```

---

## Final Output: Development Plan Document

After completing all 8 stages, generate a comprehensive document with:

### Document Structure

```markdown
# [System Name] - Development & Deployment Plan

## 1. Design Principles
[Consistency guidelines table]

## 2. System Architecture
### 2.1 System Overview
### 2.2 Component Registry

## 3. AI Agent Design
### 3.1 Agent Registry
### 3.2 Agent Capabilities
### 3.3 Agent Communication Matrix

## 4. API & Endpoints
### 4.1 Endpoint Registry
### 4.2 AI Agent Endpoints

## 5. Technology Stack
[Technology decisions with justifications]

## 6. Integration Patterns
### 6.1 Communication Matrix
### 6.2 Data Flow Diagrams

## 7. Kubernetes Deployment
### 7.1 Manifest Inventory
### 7.2 Deployments
### 7.3 ConfigMaps
### 7.4 Secrets
### 7.5 Services
### 7.6 Ingress
### 7.7 Network Policies
### 7.8 RBAC

## 8. Architecture Diagram
[ASCII/Text diagram]
```

---

## Consistency Checklist

Before finalizing, verify these consistency rules are applied:

| Category | Check |
|----------|-------|
| Agents | Each agent has single responsibility? |
| Agents | All agents are stateless? |
| Agents | LLM calls have timeouts? |
| APIs | Health endpoints on all components? |
| APIs | Consistent naming convention? |
| Services | All internal services use ClusterIP? |
| Services | Single Ingress for external access? |
| Secrets | No secrets in ConfigMaps? |
| Secrets | LLM API keys in Secrets? |
| RBAC | Namespace-scoped (not cluster)? |
| RBAC | Each component has own ServiceAccount? |
| Network | Default deny with explicit allows? |
| Network | LLM egress explicitly allowed for agents? |

---

## Example Interaction

**User**: I want to build an AI-powered task manager with a chat interface.

**Assistant**: I'll help you design and plan your AI-Native task manager. Let's go through the 8 stages systematically.

**Stage 1: System Discovery**

Let me understand your system:

1. What's the primary purpose? (e.g., personal productivity, team collaboration)
2. How will users interact? (Web app, mobile, CLI)
3. What AI capabilities do you need? (Natural language task creation, prioritization, summaries)
4. Any external integrations? (Calendar, email, Slack)

*[User responds, continue through all 8 stages...]*

---

## Related Skills

This skill extends and incorporates:
- `k8s-planning` - Kubernetes deployment planning (Stages 6-8)
