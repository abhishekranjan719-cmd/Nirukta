#!/bin/bash

# Langfuse Integration Tests
# Tests Langfuse observability platform functionality independently

set -e

# Configuration
LANGFUSE_BASE_URL="${LANGFUSE_HOST:-http://localhost:3000}"
LANGFUSE_PUBLIC_KEY="${LANGFUSE_PUBLIC_KEY:-lf_pk_a7b3c9d2e8f4a1b6c5d9e2f7a3b8c4d1}"
LANGFUSE_SECRET_KEY="${LANGFUSE_SECRET_KEY:-lf_sk_f2a8b7c3d9e1f6a4b2c7d8e3f9a1b5c6d2e8f4a9b3c1d7e2f8a4b6c9d1e5f3a7}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Counters
PASSED=0
FAILED=0

print_test() {
    echo -e "\n${BLUE}${BOLD}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Test 1: Public Health Check
test_health() {
    print_test "Testing Langfuse Public Health Endpoint"

    response=$(curl -s -w "\n%{http_code}" "${LANGFUSE_BASE_URL}/api/public/health" 2>/dev/null)
    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        status=$(echo "$body" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        version=$(echo "$body" | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        print_success "Health check passed"
        print_info "Status: ${status:-unknown}"
        print_info "Version: ${version:-unknown}"
    else
        print_error "Health check failed: $status_code"
    fi
}

# Test 2: Web UI Accessibility
test_web_ui() {
    print_test "Testing Langfuse Web UI"

    response=$(curl -s -w "\n%{http_code}" -L "${LANGFUSE_BASE_URL}" 2>/dev/null)
    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ] && echo "$body" | grep -qi "langfuse"; then
        print_success "Web UI accessible"
    else
        print_error "Web UI check failed: $status_code"
    fi
}

# Test 3: Projects API
test_projects_api() {
    print_test "Testing Langfuse Projects API"

    response=$(curl -s -w "\n%{http_code}" \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        "${LANGFUSE_BASE_URL}/api/public/v2/projects" 2>/dev/null)

    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        print_success "Projects API accessible"
        project_count=$(echo "$body" | grep -o '"id"' | wc -l | tr -d ' ')
        print_info "Found $project_count project(s)"
    else
        print_error "Projects API failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Test 4: Trace Ingestion
test_trace_ingestion() {
    print_test "Testing Langfuse Trace Ingestion"

    trace_id="test-trace-$(date +%s)"
    payload="{
        \"id\": \"${trace_id}\",
        \"name\": \"test-trace\",
        \"userId\": \"test-user\",
        \"metadata\": {
            \"test\": true,
            \"source\": \"integration-test\"
        },
        \"tags\": [\"test\", \"integration\"]
    }"

    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "${LANGFUSE_BASE_URL}/api/public/traces" 2>/dev/null)

    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ] || [ "$status_code" = "201" ]; then
        print_success "Trace ingestion successful"
        print_info "Trace ID: $trace_id"
    else
        print_error "Trace ingestion failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Test 5: Span Ingestion
test_span_ingestion() {
    print_test "Testing Langfuse Span Ingestion"

    trace_id="test-trace-$(date +%s)"
    span_id="test-span-$(date +%s)"

    # First create the trace
    trace_payload="{\"id\": \"${trace_id}\", \"name\": \"test-trace-with-span\"}"
    curl -s -X POST \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        -H "Content-Type: application/json" \
        -d "$trace_payload" \
        "${LANGFUSE_BASE_URL}/api/public/traces" 2>/dev/null >/dev/null

    # Then create a span
    span_payload="{
        \"id\": \"${span_id}\",
        \"traceId\": \"${trace_id}\",
        \"name\": \"test-span\",
        \"startTime\": \"$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")\",
        \"endTime\": \"$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")\",
        \"metadata\": {\"test\": true}
    }"

    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        -H "Content-Type: application/json" \
        -d "$span_payload" \
        "${LANGFUSE_BASE_URL}/api/public/spans" 2>/dev/null)

    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ] || [ "$status_code" = "201" ]; then
        print_success "Span ingestion successful"
        print_info "Span ID: $span_id"
    else
        print_error "Span ingestion failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Test 6: Generation Ingestion
test_generation_ingestion() {
    print_test "Testing Langfuse Generation Ingestion"

    trace_id="test-trace-$(date +%s)"
    gen_id="test-gen-$(date +%s)"

    # First create the trace
    trace_payload="{\"id\": \"${trace_id}\", \"name\": \"test-trace-with-generation\"}"
    curl -s -X POST \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        -H "Content-Type: application/json" \
        -d "$trace_payload" \
        "${LANGFUSE_BASE_URL}/api/public/traces" 2>/dev/null >/dev/null

    # Create generation
    gen_payload="{
        \"id\": \"${gen_id}\",
        \"traceId\": \"${trace_id}\",
        \"name\": \"test-generation\",
        \"startTime\": \"$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")\",
        \"endTime\": \"$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")\",
        \"model\": \"gpt-4.1\",
        \"modelParameters\": {\"temperature\": 0.7, \"max_tokens\": 100},
        \"input\": [{\"role\": \"user\", \"content\": \"Test message\"}],
        \"output\": {\"role\": \"assistant\", \"content\": \"Test response\"},
        \"usage\": {\"promptTokens\": 10, \"completionTokens\": 5, \"totalTokens\": 15},
        \"metadata\": {\"test\": true}
    }"

    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        -H "Content-Type: application/json" \
        -d "$gen_payload" \
        "${LANGFUSE_BASE_URL}/api/public/generations" 2>/dev/null)

    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ] || [ "$status_code" = "201" ]; then
        print_success "Generation ingestion successful"
        print_info "Generation ID: $gen_id"
    else
        print_error "Generation ingestion failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Test 7: Trace Retrieval
test_trace_retrieval() {
    print_test "Testing Langfuse Trace Retrieval"

    response=$(curl -s -w "\n%{http_code}" \
        -u "${LANGFUSE_PUBLIC_KEY}:${LANGFUSE_SECRET_KEY}" \
        "${LANGFUSE_BASE_URL}/api/public/traces?page=1&limit=10" 2>/dev/null)

    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        trace_count=$(echo "$body" | grep -o '"id"' | wc -l | tr -d ' ')
        print_success "Trace retrieval successful"
        print_info "Retrieved $trace_count trace(s)"
    else
        print_error "Trace retrieval failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Main execution
main() {
    echo -e "\n${BOLD}============================================================${NC}"
    echo -e "${BOLD}Langfuse Integration Tests${NC}"
    echo -e "${BOLD}============================================================${NC}"
    echo -e "Base URL: ${LANGFUSE_BASE_URL}"
    echo -e "Public Key: ${LANGFUSE_PUBLIC_KEY:0:20}..."

    # Run all tests
    test_health
    test_web_ui
    test_projects_api
    test_trace_ingestion
    test_span_ingestion
    test_generation_ingestion
    test_trace_retrieval

    # Print summary
    echo -e "\n${BOLD}============================================================${NC}"
    echo -e "${BOLD}Test Summary${NC}"
    echo -e "${BOLD}============================================================${NC}"

    TOTAL=$((PASSED + FAILED))

    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}${BOLD}✓ All tests passed! ($PASSED/$TOTAL)${NC}\n"
        exit 0
    else
        echo -e "${RED}${BOLD}✗ Some tests failed ($PASSED/$TOTAL passed, $FAILED failed)${NC}\n"
        exit 1
    fi
}

main
