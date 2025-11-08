/**
 * Ethereum Keccak-256 Implementation in C
 * High-performance cryptographic primitives for blockchain
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <openssl/evp.h>
#include <curl/curl.h>
#include <json-c/json.h>

#define RPC_URL "https://eth.llamarpc.com"

typedef struct {
    char *data;
    size_t size;
} Response;

// Callback for CURL
static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    Response *mem = (Response *)userp;

    char *ptr = realloc(mem->data, mem->size + realsize + 1);
    if (ptr == NULL) {
        printf("Not enough memory\n");
        return 0;
    }

    mem->data = ptr;
    memcpy(&(mem->data[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->data[mem->size] = 0;

    return realsize;
}

// Make RPC call
int rpc_call(const char *method, json_object **result) {
    CURL *curl;
    CURLcode res;
    Response response = {0};

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    if (!curl) {
        return -1;
    }

    json_object *payload = json_object_new_object();
    json_object_object_add(payload, "jsonrpc", json_object_new_string("2.0"));
    json_object_object_add(payload, "method", json_object_new_string(method));
    json_object_object_add(payload, "params", json_object_new_array());
    json_object_object_add(payload, "id", json_object_new_int(1));

    const char *json_string = json_object_to_json_string(payload);

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_URL, RPC_URL);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_string);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&response);

    res = curl_easy_perform(curl);

    if (res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_getstr(res));
        curl_easy_cleanup(curl);
        return -1;
    }

    json_object *parsed = json_tokener_parse(response.data);
    json_object_object_get_ex(parsed, "result", result);

    curl_easy_cleanup(curl);
    curl_slist_free_all(headers);
    json_object_put(payload);
    free(response.data);

    return 0;
}

// Keccak-256 hash
void keccak256(const uint8_t *input, size_t len, uint8_t output[32]) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();
    const EVP_MD *md = EVP_sha3_256(); // Keccak-256 is SHA3-256

    EVP_DigestInit_ex(ctx, md, NULL);
    EVP_DigestUpdate(ctx, input, len);
    EVP_DigestFinal_ex(ctx, output, NULL);
    EVP_MD_CTX_free(ctx);
}

// Get block number
uint64_t get_block_number() {
    json_object *result;
    if (rpc_call("eth_blockNumber", &result) == 0) {
        const char *hex = json_object_get_string(result);
        return strtoull(hex, NULL, 16);
    }
    return 0;
}

int main() {
    printf("🔨 C Ethereum Crypto Library\n");
    printf("========================================\n");

    // Test Keccak-256
    const char *message = "Hello, Ethereum!";
    uint8_t hash[32];
    keccak256((const uint8_t *)message, strlen(message), hash);

    printf("📝 Input: %s\n", message);
    printf("🔐 Keccak-256: 0x");
    for (int i = 0; i < 32; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n\n");

    // Get block number
    uint64_t block = get_block_number();
    if (block > 0) {
        printf("📦 Block Number: %lu\n", block);
    }

    return 0;
}
