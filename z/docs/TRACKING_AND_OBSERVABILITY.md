# Tracking & Observability Documentation

Comprehensive guide to ID tracking, LLM integration, and observability in Zuna.

## Table of Contents

- [Overview](#overview)
- [ID Structure & Tracking](#id-structure--tracking)
- [LiteLLM Integration](#litellm-integration)
- [Langfuse Observability](#langfuse-observability)
- [Memory System (Mem0)](#memory-system-mem0)
- [Request Flow](#request-flow)
- [Monitoring & Debugging](#monitoring--debugging)
- [Best Practices](#best-practices)

---

## Overview

The application implements comprehensive tracking and observability across four layers:

1. **ID Tracking**: Unique identifiers with aliases for correlation across systems
2. **LLM Integration**: LiteLLM proxy for unified LLM API access (GPT-4.1)
3. **Observability**: Langfuse v3 for LLM tracing, monitoring, and analytics
4. **Memory System**: Mem0 for conversation memory (planned, configuration ready)

### Key Features

- ✅ Automatic UUID generation for all requests
- ✅ Multiple ID aliases for cross-system compatibility
- ✅ LLM-powered responses via LiteLLM proxy OR direct Azure OpenAI
- ✅ Configurable LiteLLM enable/disable with automatic fallback
- ✅ Full Langfuse tracing with comprehensive metadata
- ✅ Token usage and cost tracking
- ✅ End-to-end request correlation
- ✅ SSL disabled for local development (httpx verify=False)
- ⏳ Conversation memory system (Mem0 integration pending)

---

## ID Structure & Tracking

### Primary IDs

Every chat request generates four primary identifiers:

| ID | Purpose | Generated | Example |
|----|---------|-----------|---------|
| `user_id` | User identifier | Backend (once per user) | `d99edc13-c1e0-4bf8-be1d-72c728802afd` |
| `chat_id` | Individual message/request | Backend (per message) | `a7882acf-b4cd-4400-9196-6cfae48feee3` |
| `conversation_id` | Conversation/session | Frontend/Backend | `12135790-1fb1-461e-babb-f1512743a1bc` |
| `usecase_id` | Use case/application | Backend/Frontend | `c2155e18-757e-4849-86df-5e43d440f078` |

### ID Aliases

Each primary ID has multiple aliases for compatibility with different observability systems:

#### chat_id Aliases
- `request_id` - Request identifier
- `run_id` - Run identifier
- `correlation_id` - Correlation identifier
- `observation_id` - Observation identifier

**Purpose:** Different systems use different terminology for request tracking. All aliases point to the same `chat_id`.

#### conversation_id Aliases
- `session_id` - Session identifier
- `thread_id` - Thread identifier

**Purpose:** Session/conversation tracking across different platforms.

#### usecase_id Aliases
- `app_id` - Application identifier
- `agent_id` - Agent identifier

**Purpose:** Application/use case categorization.

#### user_id Alias
- `user_email` - User email (currently same as user_id)

**Purpose:** User identification with email-like format.

### TrackingMetadata Model

All tracking information is encapsulated in the `TrackingMetadata` Pydantic model:

```python
class TrackingMetadata(BaseModel):
    # Primary IDs
    user_id: str
    chat_id: str
    conversation_id: str
    usecase_id: str

    # chat_id aliases
    request_id: str
    run_id: str
    correlation_id: str
    observation_id: str

    # conversation_id aliases
    session_id: str
    thread_id: str

    # usecase_id aliases
    app_id: str
    agent_id: str

    # user_id alias
    user_email: str
```

### Automatic Generation

The `TrackingMetadata.create()` method generates all IDs and aliases automatically:

```python
tracking = TrackingMetadata.create(
    user_id="optional-user-id",           # Auto-generated if None
    conversation_id="existing-conv-id",   # Use existing conversation
    usecase_id=None,                      # Auto-generated
    chat_id=None,                         # Always auto-generated per message
)
```

**Location:**
- Backend: `backend/app/models/chat.py`
- Engine: `engine/app/models/process.py` (identical copy)

---

## LiteLLM Integration

### Overview

LiteLLM is a unified LLM gateway that provides an OpenAI-compatible API for multiple LLM providers.

**Architecture:**
```
Engine → LiteLLM Proxy (port 4000) → Azure OpenAI (GPT-4.1)
```

**Features:**
- ✅ OpenAI-compatible API
- ✅ Azure OpenAI integration
- ✅ Request/response caching
- ✅ SSL verification disabled for local development
- ✅ Automatic token counting
- ✅ Rate limiting and load balancing

### Configuration

**LiteLLM Service:** Configured in `docker-compose.yml`

**Models Available:**
- `gpt-4.1` - GPT-4 Turbo (primary)
- `text-embedding-3-small` - Text embeddings
- `cohere-rerank-v3.5` - Reranking

**Configuration File:** `configs/litellm/config.yaml`

### Enable/Disable LiteLLM

LiteLLM proxy can be enabled or disabled via the `LITELLM_ENABLED` environment variable. When disabled, the system automatically falls back to direct Azure OpenAI API calls.

**Configuration Location:** `.env` file (project root)

#### Mode 1: LiteLLM Proxy Enabled (Default)

```bash
LITELLM_ENABLED=true

# LiteLLM configuration
LITELLM_MASTER_KEY=sk-1234567890abcdef
LITELLM_CHAT_MODEL=gpt-4.1
LITELLM_EMBEDDING_MODEL=text-embedding-3-small
LITELLM_RERANK_MODEL=cohere-rerank-v3.5
```

**Architecture:**
```
Engine → LiteLLM Proxy → Azure OpenAI / Other Providers
```

**Engine logs on startup:**
```
INFO | LiteLLM client initialized | Base URL: http://litellm:4000
INFO | MessageProcessor initialized | Client: LiteLLM Proxy | Model: gpt-4.1 | Langfuse enabled: True
```

**Behavior:**
- ✅ All LLM calls routed through LiteLLM proxy
- ✅ Support for multiple providers (Azure OpenAI, OpenAI, Anthropic, etc.)
- ✅ Built-in caching, rate limiting, and load balancing
- ✅ Unified API for all providers
- ✅ Proxy-level monitoring and logging

**Processing logs:**
```
INFO | Calling LiteLLM Proxy | Model: gpt-4.1 | Chat ID: xxx
INFO | LiteLLM chat completion success | Model: gpt-4.1 | Tokens: 360
INFO | LLM processing complete | Time: 3.97s | Tokens: 360
```

#### Mode 2: Direct Azure OpenAI (LiteLLM Disabled)

```bash
LITELLM_ENABLED=false

# Azure OpenAI configuration (fallback)
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
```

**Architecture:**
```
Engine → Azure OpenAI REST API (Direct)
```

**Engine logs on startup:**
```
INFO | Azure OpenAI direct client initialized | Endpoint: https://your-instance.openai.azure.com/ | Chat deployment: gpt-4
INFO | MessageProcessor initialized | Client: Azure OpenAI Direct | Model: gpt-4 | Langfuse enabled: True
```

**Behavior:**
- ✅ Direct REST API calls to Azure OpenAI
- ✅ No proxy overhead
- ✅ SSL verification disabled for local development (httpx verify=False)
- ✅ Automatic fallback when LiteLLM unavailable
- ✅ Uses Azure deployment names instead of model IDs

**Processing logs:**
```
INFO | Calling Azure OpenAI Direct | Model: gpt-4 | Chat ID: xxx
INFO | Azure OpenAI chat completion success | Deployment: gpt-4 | Tokens: 615
INFO | LLM processing complete | Time: 5.29s | Tokens: 615
```

#### Comparison

| Feature | LiteLLM Proxy | Azure OpenAI Direct |
|---------|---------------|---------------------|
| **Providers** | Multiple (Azure, OpenAI, Anthropic, etc.) | Azure OpenAI only |
| **Caching** | Built-in proxy cache | No caching |
| **Load Balancing** | Proxy handles it | Manual implementation |
| **Rate Limiting** | Proxy handles it | Manual implementation |
| **SSL** | Disabled for local dev | Disabled for local dev |
| **Overhead** | Proxy hop (~100-200ms) | Direct API call |
| **Monitoring** | Proxy-level + Langfuse | Langfuse only |
| **Model Names** | Model IDs (gpt-4.1) | Deployment names (gpt-4) |
| **Fallback** | N/A (primary) | Automatic fallback |

#### When to Use Each Mode

**Use LiteLLM Proxy (LITELLM_ENABLED=true):**
- Production environments with multiple LLM providers
- Need unified API across providers
- Want built-in caching and rate limiting
- Require load balancing across multiple backends
- Need proxy-level monitoring and logging

**Use Azure OpenAI Direct (LITELLM_ENABLED=false):**
- Development/testing without LiteLLM dependency
- Single Azure OpenAI backend only
- Minimize latency (no proxy hop)
- LiteLLM service unavailable
- Simplified architecture for specific use cases

#### Configuration Flow

```
.env file (LITELLM_ENABLED=true/false)
  ↓
configs/settings.py (LiteLLMSettings.litellm_enabled)
  ↓
configs/settings.py (LiteLLMSettings.is_enabled property)
  ↓
engine/app/config.py (settings.litellm.is_enabled)
  ↓
engine/app/services/processor.py (chooses client)
  ↓
IF enabled → engine/app/services/litellm_client.py (LiteLLMClient)
IF disabled → engine/app/services/azure_openai_client.py (AzureOpenAIClient)
```

#### Switching Between Modes

```bash
# 1. Update .env
LITELLM_ENABLED=true   # or false

# 2. Restart engine to reload configuration
docker-compose stop engine && docker-compose up -d engine

# 3. Verify logs show correct client
docker logs chat-engine --tail 20 | grep "MessageProcessor initialized"
```

**Important:**
1. Both clients use httpx with SSL disabled (verify=False) for local development
2. Both clients are OpenAI-compatible (same response format)
3. Langfuse tracing works identically in both modes
4. No code changes needed - purely configuration-driven
5. Azure OpenAI requires deployment names, not model IDs

### LiteLLM Client

**Location:** `engine/app/services/litellm_client.py`

**Key Features:**
```python
class LiteLLMClient:
    def __init__(self):
        # SSL disabled for local development
        self.client = httpx.AsyncClient(
            base_url="http://litellm:4000",
            verify=False,  # Disable SSL
            headers={"Authorization": f"Bearer {MASTER_KEY}"},
        )

    async def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        # Call LiteLLM proxy
        response = await self.client.post("/v1/chat/completions", json={...})
        return response.json()
```

### Usage in Engine

**Location:** `engine/app/services/processor.py`

```python
class MessageProcessor:
    def __init__(self):
        self.litellm_client = get_litellm_client()
        self.model = "gpt-4.1"
        self.temperature = 0.7

    async def process(self, message: str, tracking: TrackingMetadata):
        # Prepare messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]

        # Call LiteLLM
        llm_response = await self.litellm_client.chat_completion(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        # Extract response and token usage
        response_text = llm_response["choices"][0]["message"]["content"]
        usage = llm_response.get("usage", {})

        return response_text, usage
```

### Authentication

LiteLLM requires Bearer token authentication:

**Environment Variable:** `LITELLM_MASTER_KEY`

**Header Format:**
```bash
Authorization: Bearer sk-1234567890abcdef
```

**Endpoints:**
- `/v1/chat/completions` - Chat completions (requires auth)
- `/v1/embeddings` - Text embeddings (requires auth)
- `/health/liveliness` - Health check (no auth required)

---

## Langfuse Observability

### Overview

Langfuse v3 is an LLM observability platform that tracks:
- LLM requests and responses
- Token usage and costs
- Processing times
- User sessions and conversations
- Comprehensive metadata

**Architecture:**
```
Engine → Langfuse SDK → Langfuse Server (port 3000)
         ↓
      Traces, Generations, Spans stored in PostgreSQL
```

### Enable/Disable Langfuse

Langfuse tracing can be controlled via the `LANGFUSE_ENABLED` environment variable.

**Configuration Location:** `.env` file (project root)

#### To Enable Langfuse (Default)

```bash
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=lf_pk_a7b3c9d2e8f4a1b6c5d9e2f7a3b8c4d1
LANGFUSE_SECRET_KEY=lf_sk_f2a8b7c3d9e1f6a4b2c7d8e3f9a1b5c6d2e8f4a9b3c1d7e2f8a4b6c9d1e5f3a7
```

**Engine logs on startup:**
```
INFO | Langfuse client initialized | Host: http://langfuse-web:3000
INFO | MessageProcessor initialized | Model: gpt-4.1 | Langfuse enabled: True
```

**Behavior:**
- ✅ All LLM calls are logged to Langfuse
- ✅ Full metadata tracking (all 13 IDs)
- ✅ Token usage and cost tracking
- ✅ Traces visible in Langfuse UI

#### To Disable Langfuse

```bash
LANGFUSE_ENABLED=false
```

**Engine logs on startup:**
```
WARNING | Langfuse is not enabled | Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY
INFO | MessageProcessor initialized | Model: gpt-4.1 | Langfuse enabled: False
```

**Behavior:**
- ✅ No Langfuse tracing occurs
- ✅ LLM calls still work normally via LiteLLM
- ✅ No performance overhead from tracing
- ✅ No data sent to Langfuse

**When to Disable:**
- Local development without observability needs
- Reducing external dependencies
- Performance testing without tracing overhead
- Privacy-sensitive environments

**Important:**
1. Langfuse is enabled ONLY if:
   - `LANGFUSE_ENABLED=true` AND
   - Both `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` are set
2. Changes to `.env` require container restart:
   ```bash
   docker-compose stop engine && docker-compose up -d engine
   ```

**Configuration Flow:**
```
.env file
  ↓
configs/settings.py (LangfuseSettings)
  ↓
engine/app/config.py (settings.langfuse)
  ↓
engine/app/services/langfuse_tracer.py (checks settings.langfuse.is_enabled)
  ↓
engine/app/services/processor.py (skips logging if disabled)
```

### Langfuse Tracer

**Location:** `engine/app/services/langfuse_tracer.py`

**Simplified API:**
```python
class LangfuseTracer:
    def log_llm_call(
        self,
        tracking: TrackingMetadata,
        model: str,
        input_messages: List[Dict[str, str]],
        output_message: str,
        usage: Optional[Dict[str, int]] = None,
        temperature: float = 0.7,
        processing_time: float = 0.0,
    ) -> bool:
        # Log complete LLM call with all metadata
        generation = self.client.start_generation(
            name="llm_generation",
            model=model,
            model_parameters={"temperature": temperature},
            input=input_messages,
            output=output_message,
            metadata={
                # All tracking IDs and aliases
                "user_id": tracking.user_id,
                "chat_id": tracking.chat_id,
                "conversation_id": tracking.conversation_id,
                "usecase_id": tracking.usecase_id,
                "request_id": tracking.request_id,
                "run_id": tracking.run_id,
                "correlation_id": tracking.correlation_id,
                "observation_id": tracking.observation_id,
                "session_id": tracking.session_id,
                "thread_id": tracking.thread_id,
                "app_id": tracking.app_id,
                "agent_id": tracking.agent_id,
                "user_email": tracking.user_email,
                # Additional metadata
                "model": model,
                "temperature": temperature,
                "processing_time_seconds": processing_time,
            },
            usage_details={
                "input": usage["prompt_tokens"],
                "output": usage["completion_tokens"],
                "total": usage["total_tokens"],
            },
        )
        generation.end()
```

### Metadata in Langfuse

Every LLM call logged to Langfuse includes:

**Trace Information:**
- Trace ID: `chat_id`
- User ID: `user_id`
- Session ID: `conversation_id`

**Generation Metadata:**
- All 13 tracking IDs (primary + aliases)
- Model: `gpt-4.1`
- Temperature: `0.7`
- Processing time: Seconds
- Timestamp: ISO 8601 format

**Usage Data:**
- Input tokens (prompt)
- Output tokens (completion)
- Total tokens
- Cost (calculated by Langfuse)

**Input/Output:**
- Input: Full message list (system + user)
- Output: Generated response text

### Accessing Langfuse UI

**URL:** http://localhost:3000

**Default Credentials:**
- Email: `admin@example.com`
- Password: (see `.env`)

**Change immediately in production!**

### Langfuse Features

1. **Traces View**: See all LLM calls with full details
2. **Sessions View**: Group traces by `conversation_id`
3. **Users View**: Track activity by `user_id`
4. **Analytics**: Token usage, costs, latencies
5. **Debugging**: Full request/response inspection
6. **Search**: Filter by any metadata field

---

## Memory System (Mem0)

### Overview

The memory system provides conversation memory and context retention capabilities using Mem0. This feature is currently **disabled by default** and will be integrated in a future release.

**Planned Features:**
- Persistent conversation memory across sessions
- User-specific context and preferences
- Automatic extraction of key information
- Context-aware responses based on conversation history
- Memory search and retrieval

**Status:** Configuration ready, integration pending

### Enable/Disable Memory

Memory system can be controlled via the `MEMORY_ENABLED` environment variable.

**Configuration Location:** `.env` file (project root)

#### Current Status (Disabled)

```bash
MEMORY_ENABLED=false  # Default
```

**Engine logs on startup:**
```
INFO | Memory system (Mem0): Disabled | Will be integrated in future
```

**Behavior:**
- ✅ No memory operations occur
- ✅ Standard LLM processing without memory context
- ✅ No external dependencies on Mem0

#### Future Status (When Enabled)

```bash
MEMORY_ENABLED=true
# Additional Mem0 configuration will be added:
# MEM0_API_KEY=your_api_key
# MEM0_HOST=http://mem0-server:8080
```

**Expected logs on startup (future):**
```
INFO | Memory system (Mem0): Enabled | Host: http://mem0-server:8080
```

**Expected behavior (future):**
- ✅ Conversation memory stored and retrieved
- ✅ Context from previous messages used in responses
- ✅ User preferences remembered across sessions
- ✅ Key information automatically extracted

**Configuration Flow:**
```
.env file (MEMORY_ENABLED=true/false)
  ↓
configs/settings.py (MemorySettings)
  ↓
engine/app/config.py (settings.memory)
  ↓
[Future] engine/app/services/memory_manager.py
  ↓
[Future] engine/app/services/processor.py (uses memory context)
```

### When Memory Will Be Integrated

Memory system (Mem0) integration is planned for future development. This will include:

1. **Mem0 Service**: Docker container for Mem0 server
2. **Memory Manager**: Service to interact with Mem0 API
3. **Context Injection**: Automatic memory context in LLM prompts
4. **Memory Storage**: Persistent storage of conversation context
5. **Memory Search**: Query historical context by user/conversation
6. **Memory UI**: Dashboard for viewing and managing memories

**Current Implementation:**
- ✅ Environment configuration ready
- ✅ Settings class created
- ✅ Logging in place
- ⏳ Service integration pending
- ⏳ API client pending
- ⏳ Context management pending

**To Enable Later:**
1. Update `MEMORY_ENABLED=true` in `.env`
2. Add Mem0 service to `docker-compose.yml`
3. Implement memory manager service
4. Integrate with message processor
5. Restart services

---

## Request Flow

### Complete Flow with Tracking

```
1. Frontend → POST /api/chat
   {
     "message": "Hello!",
     "conversation_id": "optional"
   }

2. Backend (main.py:chat)
   - Generate/reuse conversation_id
   - Create TrackingMetadata with UUIDs
   - Log: "Tracking metadata generated | User: xxx | Chat: xxx"

3. Backend → Engine POST /process
   {
     "message": "Hello!",
     "context": {},
     "tracking": {
       "user_id": "uuid",
       "chat_id": "uuid",
       "conversation_id": "uuid",
       "usecase_id": "uuid",
       "request_id": "uuid",  # Same as chat_id
       ...all aliases...
     }
   }

4. Engine (main.py:process)
   - Receive request with tracking
   - Log: "Processing message with tracking | User: xxx | Chat: xxx"

5. Engine (processor.py:process)
   - Start timing
   - Prepare messages for LLM
   - Log: "Calling LiteLLM | Model: gpt-4.1 | Chat ID: xxx"

6. Engine → LiteLLM POST /v1/chat/completions
   {
     "model": "gpt-4.1",
     "messages": [
       {"role": "system", "content": "..."},
       {"role": "user", "content": "Hello!"}
     ],
     "temperature": 0.7
   }

7. LiteLLM → Azure OpenAI
   - Forward request to Azure
   - Return response with token usage

8. Engine → Langfuse (langfuse_tracer.py)
   - Create generation with start_generation()
   - Include all tracking metadata
   - Include token usage
   - End generation
   - Log: "Langfuse LLM call logged | Trace ID: xxx"

9. Engine (processor.py)
   - Calculate processing time
   - Build metadata response
   - Log: "LLM processing complete | Chat ID: xxx | Time: 2.05s | Tokens: 60"

10. Engine → Backend
    {
      "response": "Hello! How can I help?",
      "metadata": {
        "processing_type": "llm",
        "model": "gpt-4.1",
        "tokens": {...},
        "tracking": {...}
      }
    }

11. Backend → Frontend
    {
      "response": "Hello! How can I help?",
      "conversation_id": "uuid",
      "timestamp": "2025-12-31T10:00:00Z"
    }
```

### Timing Breakdown

Typical request timing:
- **Frontend → Backend**: < 10ms
- **Backend processing**: < 50ms
- **Backend → Engine**: < 10ms
- **Engine → LiteLLM → Azure**: 1-3 seconds
- **Langfuse logging**: < 50ms (async)
- **Total**: ~2-3 seconds

---

## Monitoring & Debugging

### Log Messages

#### Backend Logs

```bash
# Tracking generation
2026-01-01 01:50:51.441 | INFO | Tracking metadata generated | User: xxx | Chat: xxx | Conv: xxx | Usecase: xxx

# Engine response received
2026-01-01 01:50:53.535 | INFO | Engine response received | Conv: xxx | Chat: xxx
```

#### Engine Logs

```bash
# Service initialization
2026-01-01 01:50:09.401 | INFO | LiteLLM client initialized | Base URL: http://litellm:4000
2026-01-01 01:50:09.410 | INFO | Langfuse client initialized | Host: http://langfuse-web:3000
2026-01-01 01:50:09.410 | INFO | MessageProcessor initialized | Model: gpt-4.1 | Langfuse enabled: True

# Processing
2026-01-01 01:50:51.463 | INFO | Processing message with tracking | User: xxx | Chat: xxx | Conv: xxx | Usecase: xxx
2026-01-01 01:50:51.463 | INFO | Calling LiteLLM | Model: gpt-4.1 | Chat ID: xxx
2026-01-01 01:50:53.534 | INFO | LLM processing complete | Chat ID: xxx | Time: 2.07s | Tokens: 53
```

### Viewing Logs

```bash
# Backend logs
docker logs chat-backend --tail=50 --follow

# Engine logs
docker logs chat-engine --tail=50 --follow

# Filter by tracking ID
docker logs chat-engine 2>&1 | grep "Chat ID: a7882acf"

# Filter by errors
docker logs chat-engine 2>&1 | grep ERROR
```

### Checking Services

```bash
# Backend health
curl http://localhost:8000/health

# Engine health
docker exec chat-backend curl http://engine:8001/health

# LiteLLM health
curl http://localhost:4000/health/liveliness

# Langfuse health
curl http://localhost:3000/api/public/health
```

### Debugging Tracking

**Find all logs for a specific chat_id:**
```bash
CHAT_ID="a7882acf-b4cd-4400-9196-6cfae48feee3"

# Backend
docker logs chat-backend 2>&1 | grep "$CHAT_ID"

# Engine
docker logs chat-engine 2>&1 | grep "$CHAT_ID"
```

**Find all messages in a conversation:**
```bash
CONV_ID="12135790-1fb1-461e-babb-f1512743a1bc"

docker logs chat-backend 2>&1 | grep "$CONV_ID"
docker logs chat-engine 2>&1 | grep "$CONV_ID"
```

### Langfuse Debugging

**Access Langfuse UI:**
1. Open http://localhost:3000
2. Login: `admin@example.com` / (see `.env`)
3. View **Traces** tab
4. Search by metadata:
   - `chat_id:a7882acf`
   - `conversation_id:12135790`
   - `user_id:d99edc13`
5. Click trace to see full details

**Common Issues:**

**Traces not appearing:**
- Check Langfuse logs: `docker logs chat-langfuse-web --tail=50`
- Verify credentials in `.env`
- Ensure engine can reach Langfuse: `docker exec chat-engine curl http://langfuse-web:3000/api/public/health`

**Missing metadata:**
- Check engine logs for "Langfuse LLM call logged" message
- Verify TrackingMetadata is passed from backend to engine
- Check for errors in langfuse_tracer.py

---

## Best Practices

### ID Generation

**DO:**
- ✅ Let backend auto-generate `chat_id` for each message
- ✅ Reuse `conversation_id` for continuation
- ✅ Generate `user_id` once per user and reuse
- ✅ Use descriptive `usecase_id` per application feature

**DON'T:**
- ❌ Manually create UUIDs in frontend
- ❌ Reuse `chat_id` across multiple messages
- ❌ Change `conversation_id` mid-conversation
- ❌ Use sensitive data in IDs

### Tracking Metadata

**DO:**
- ✅ Always send tracking metadata from backend to engine
- ✅ Include all IDs and aliases
- ✅ Log important tracking points (generation, processing, completion)
- ✅ Use structured logging with consistent field names

**DON'T:**
- ❌ Skip tracking for "test" requests
- ❌ Remove or modify tracking IDs in flight
- ❌ Log personally identifiable information (PII) in metadata

### LiteLLM Integration

**DO:**
- ✅ Use SSL-disabled httpx client for local development
- ✅ Handle timeouts gracefully (default: 60s)
- ✅ Log token usage for cost tracking
- ✅ Implement fallback for LiteLLM failures

**DON'T:**
- ❌ Disable SSL in production
- ❌ Hardcode API keys in code
- ❌ Ignore token limits
- ❌ Skip error handling

### Langfuse Observability

**DO:**
- ✅ Log every LLM call
- ✅ Include comprehensive metadata
- ✅ Flush events on shutdown: `tracer.flush()`
- ✅ Use descriptive generation names
- ✅ Track processing time

**DON'T:**
- ❌ Log PII in input/output
- ❌ Skip token usage tracking
- ❌ Ignore Langfuse errors (log and continue)
- ❌ Leave default admin password in production

### Production Checklist

Before deploying to production:

- [ ] Change Langfuse admin password
- [ ] Enable SSL for LiteLLM client
- [ ] Set up proper `user_id` (real users, not UUIDs)
- [ ] Configure `user_email` with actual emails
- [ ] Set meaningful `usecase_id` per feature
- [ ] Review metadata for sensitive data
- [ ] Set up Langfuse cost tracking
- [ ] Configure rate limiting
- [ ] Set up monitoring alerts
- [ ] Document tracking ID conventions for your team

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                          │
│                                                                   │
│  POST /api/chat                                                   │
│  { message, conversation_id? }                                    │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                       Backend (FastAPI)                          │
│                                                                   │
│  1. Generate TrackingMetadata                                    │
│     - user_id, chat_id, conversation_id, usecase_id              │
│     - All 13 aliases                                             │
│                                                                   │
│  2. POST /process → Engine                                       │
│     { message, context, tracking: {...} }                        │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ↓
┌─────────────────────────────────────────────────────────────────┐
│                        Engine (FastAPI)                          │
│                                                                   │
│  MessageProcessor:                                               │
│    1. Receive tracking metadata                                  │
│    2. Call LiteLLM proxy                                         │
│    3. Log to Langfuse with metadata                              │
│    4. Return response + metadata                                 │
└───────────┬─────────────────────────┬───────────────────────────┘
            │                         │
            ↓                         ↓
┌───────────────────────┐  ┌───────────────────────────────────┐
│   LiteLLM Proxy       │  │   Langfuse v3 Platform            │
│   (Port 4000)         │  │   (Port 3000)                     │
│                       │  │                                    │
│ - Azure OpenAI GPT-4  │  │ - Traces with all metadata        │
│ - Token counting      │  │ - Token usage tracking            │
│ - Caching             │  │ - Session grouping                │
│ - Rate limiting       │  │ - Analytics & debugging           │
└───────────────────────┘  └────────────────────────────────────┘
```

---

## Example Tracking Session

**Scenario:** User has a 3-message conversation

### Message 1: "Hello!"

**Generated IDs:**
```
user_id: 550e8400-e29b-41d4-a716-446655440000
chat_id: 7c9e6679-7425-40de-944b-e07fc1f90ae7
conversation_id: 92b39e8d-0e0e-4a4f-8f4d-4f3e3e3e3e3e
usecase_id: a1b2c3d4-e5f6-7890-1234-567890abcdef
```

**Langfuse Trace:**
- Trace ID: `7c9e6679-7425-40de-944b-e07fc1f90ae7`
- User ID: `550e8400-e29b-41d4-a716-446655440000`
- Session ID: `92b39e8d-0e0e-4a4f-8f4d-4f3e3e3e3e3e`
- Metadata: All 13 IDs
- Tokens: 45

### Message 2: "Tell me a joke"

**Generated IDs:**
```
user_id: 550e8400-e29b-41d4-a716-446655440000 (REUSED)
chat_id: 3fa85f64-5717-4562-b3fc-2c963f66afa6 (NEW)
conversation_id: 92b39e8d-0e0e-4a4f-8f4d-4f3e3e3e3e3e (REUSED)
usecase_id: a1b2c3d4-e5f6-7890-1234-567890abcdef (REUSED)
```

**Langfuse Trace:**
- Trace ID: `3fa85f64-5717-4562-b3fc-2c963f66afa6`
- User ID: `550e8400-e29b-41d4-a716-446655440000`
- Session ID: `92b39e8d-0e0e-4a4f-8f4d-4f3e3e3e3e3e` (SAME!)
- Tokens: 68

### Message 3: "Thanks!"

**Generated IDs:**
```
user_id: 550e8400-e29b-41d4-a716-446655440000 (REUSED)
chat_id: 9c3f4a5b-6c7d-8e9f-0a1b-2c3d4e5f6a7b (NEW)
conversation_id: 92b39e8d-0e0e-4a4f-8f4d-4f3e3e3e3e3e (REUSED)
usecase_id: a1b2c3d4-e5f6-7890-1234-567890abcdef (REUSED)
```

**Langfuse Trace:**
- Trace ID: `9c3f4a5b-6c7d-8e9f-0a1b-2c3d4e5f6a7b`
- User ID: `550e8400-e29b-41d4-a716-446655440000`
- Session ID: `92b39e8d-0e0e-4a4f-8f4d-4f3e3e3e3e3e` (SAME!)
- Tokens: 35

**In Langfuse UI:**
- **Traces view**: 3 separate traces
- **Sessions view**: 1 session with 3 traces grouped together
- **Users view**: 1 user with 3 traces and 148 total tokens

---

## API Reference

### TrackingMetadata.create()

```python
@classmethod
def create(
    cls,
    user_id: Optional[str] = None,
    chat_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    usecase_id: Optional[str] = None,
) -> TrackingMetadata
```

**Parameters:**
- `user_id`: User identifier (generates UUID if None)
- `chat_id`: Chat identifier (generates UUID if None)
- `conversation_id`: Conversation identifier (generates UUID if None)
- `usecase_id`: Use case identifier (generates UUID if None)

**Returns:** `TrackingMetadata` instance with all IDs and aliases

### LiteLLMClient.chat_completion()

```python
async def chat_completion(
    self,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs: Any,
) -> Dict[str, Any]
```

**Parameters:**
- `model`: Model name (e.g., "gpt-4.1")
- `messages`: List of message dicts with 'role' and 'content'
- `temperature`: Sampling temperature (0.0 to 2.0)
- `max_tokens`: Maximum tokens to generate
- `**kwargs`: Additional LiteLLM parameters

**Returns:** LiteLLM response dictionary with choices, usage, etc.

### LangfuseTracer.log_llm_call()

```python
def log_llm_call(
    self,
    tracking: TrackingMetadata,
    model: str,
    input_messages: List[Dict[str, str]],
    output_message: str,
    usage: Optional[Dict[str, int]] = None,
    temperature: float = 0.7,
    processing_time: float = 0.0,
) -> bool
```

**Parameters:**
- `tracking`: TrackingMetadata with all IDs
- `model`: Model name
- `input_messages`: Input messages list
- `output_message`: Generated output
- `usage`: Token usage dict (prompt_tokens, completion_tokens, total_tokens)
- `temperature`: Model temperature
- `processing_time`: Processing time in seconds

**Returns:** `True` if successful, `False` otherwise

---

**Last Updated:** 2026-01-01
**Version:** 1.0.0
