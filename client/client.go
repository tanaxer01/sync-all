package client

import (
	"io"
	"log"
	"net/http"
)

var HeaderData = map[string]string{
	"X-Apple-ID-Account-Country": "account_country",
	"X-Apple-ID-Session-Id":      "session_id",
	"X-Apple-Session-Token":      "session_token",
	"X-Apple-TwoSV-Trust-Token":  "trust_token",
	"scnt":                       "scnt",
}

type ISession struct {
	Client *http.Client
	Data   map[string]string
}

func New() *ISession {
	s := &ISession{
		Client: &http.Client{},
		Data:   map[string]string{},
	}

	return s
}

func (s *ISession) IRequest(reqType string, url string) (string, error) {
	req, err := http.NewRequest(reqType, url, nil)
	if err != nil {
		return "", err
	}

	res, err := s.Client.Do(req)
	if err != nil {
		return "", err
	}
	defer res.Body.Close()

	for key, val := range HeaderData {
		if res.Header.Get(key) != "" {
			s.Data[val] = res.Header.Get(key)
		}
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return "", err
	}

	log.Printf("Body: %s\n", body)
	log.Printf("Response status: %s\n", res.Status)

	return "", nil
}
