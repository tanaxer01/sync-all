package main

import (
	"net/http"

	"github.com/google/uuid"
)

var AUTH_ENDPOINT string = "https://idmsa.apple.com/appleauth/auth"

func AuthHeaders(override map[string]string) *http.Header {
	headers := &http.Header{
		"Accept":                           {"*/*"},
		"Content-Type":                     {"application/json"},
		"X-Apple-OAuth-Client-Id":          {"d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d"},
		"X-Apple-OAuth-Client-Type":        {"firstPartyAuth"},
		"X-Apple-OAuth-Redirect-URI":       {"https://www.icloud.com"},
		"X-Apple-OAuth-Require-Grant-Code": {"true"},
		"X-Apple-OAuth-Response-Mode":      {"web_message"},
		"X-Apple-OAuth-Response-Type":      {"code"},
		"X-Apple-Widget-Key":               {"d39ba9916b7251055b22c7f910e2ea796ee65e98b2ddecea8f5dde8d9d1a815d"},
		// "X-Apple-OAuth-State": client_id,
	}

	if override != nil {
		for key, val := range override {
			headers.Add(key, val)
		}
	}

	return headers
}
