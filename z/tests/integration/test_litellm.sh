#!/bin/bash

# LiteLLM Integration Tests
# Tests LiteLLM proxy functionality independently

set -e

# Configuration
LITELLM_BASE_URL="${LITELLM_BASE_URL:-http://localhost:4000}"
LITELLM_API_KEY="${LITELLM_MASTER_KEY:-sk-1234}"

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

# Test 1: Health Check
test_health() {
    print_test "Testing LiteLLM Health Endpoint"

    response=$(curl -s -w "\n%{http_code}" \
        -H "Authorization: Bearer ${LITELLM_API_KEY}" \
        "${LITELLM_BASE_URL}/health" 2>/dev/null)
    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        print_success "Health check passed: $status_code"
    else
        print_error "Health check failed: $status_code"
        print_info "Response: $body"
    fi
}

# Test 2: Liveliness Check
test_liveliness() {
    print_test "Testing LiteLLM Liveliness Endpoint"

    response=$(curl -s -w "\n%{http_code}" "${LITELLM_BASE_URL}/health/liveliness" 2>/dev/null)
    status_code=$(echo "$response" | tail -n1)

    if [ "$status_code" = "200" ]; then
        print_success "Liveliness check passed: $status_code"
    else
        print_error "Liveliness check failed: $status_code"
    fi
}

# Test 3: Readiness Check
test_readiness() {
    print_test "Testing LiteLLM Readiness Endpoint"

    response=$(curl -s -w "\n%{http_code}" "${LITELLM_BASE_URL}/health/readiness" 2>/dev/null)
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        print_success "Readiness check passed"
        db_status=$(echo "$body" | grep -o '"db":"[^"]*"' | cut -d'"' -f4)
        cache_status=$(echo "$body" | grep -o '"cache":"[^"]*"' | cut -d'"' -f4)
        print_info "Database: ${db_status:-unknown}"
        print_info "Cache: ${cache_status:-unknown}"
    else
        print_error "Readiness check failed: $status_code"
    fi
}

# Test 4: Models List
test_models_list() {
    print_test "Testing LiteLLM Models List"

    response=$(curl -s -w "\n%{http_code}" \
        -H "Authorization: Bearer ${LITELLM_API_KEY}" \
        -H "Content-Type: application/json" \
        "${LITELLM_BASE_URL}/v1/models" 2>/dev/null)

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        model_count=$(echo "$body" | grep -o '"id"' | wc -l | tr -d ' ')
        print_success "Models list retrieved: $model_count models"

        # Extract model names
        models=$(echo "$body" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
        while IFS= read -r model; do
            [ -n "$model" ] && print_info "  - $model"
        done <<< "$models"
    else
        print_error "Models list failed: $status_code"
        print_info "Response: $body"
    fi
}

# Test 5: Chat Completion
test_chat_completion() {
    print_test "Testing LiteLLM Chat Completion"

    payload='{
        "model": "gpt-4.1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Respond in one short sentence."},
            {"role": "user", "content": "Say LiteLLM test successful if you can read this."}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }'

    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -H "Authorization: Bearer ${LITELLM_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "${LITELLM_BASE_URL}/v1/chat/completions" 2>/dev/null)

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        print_success "Chat completion successful"
        content=$(echo "$body" | grep -o '"content":"[^"]*"' | head -1 | cut -d'"' -f4)
        model=$(echo "$body" | grep -o '"model":"[^"]*"' | head -1 | cut -d'"' -f4)
        print_info "Response: ${content:-<empty>}"
        print_info "Model: ${model:-unknown}"
    else
        print_error "Chat completion failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Test 6: Embeddings
test_embedding() {
    print_test "Testing LiteLLM Embeddings"

    payload='{
        "model": "text-embedding-3-small",
        "input": "Test embedding generation from LiteLLM"
    }'

    response=$(curl -s -w "\n%{http_code}" \
        -X POST \
        -H "Authorization: Bearer ${LITELLM_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        "${LITELLM_BASE_URL}/v1/embeddings" 2>/dev/null)

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$ d')

    if [ "$status_code" = "200" ]; then
        print_success "Embedding generation successful"
        model=$(echo "$body" | grep -o '"model":"[^"]*"' | head -1 | cut -d'"' -f4)
        print_info "Model: ${model:-unknown}"
    else
        print_error "Embedding generation failed: $status_code"
        print_info "Response: $(echo "$body" | head -c 200)"
    fi
}

# Main execution
main() {
    echo -e "\n${BOLD}============================================================${NC}"
    echo -e "${BOLD}LiteLLM Integration Tests${NC}"
    echo -e "${BOLD}============================================================${NC}"
    echo -e "Base URL: ${LITELLM_BASE_URL}"

    # Run all tests
    test_health
    test_liveliness
    test_readiness
    test_models_list
    test_chat_completion
    test_embedding

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
