package client

import "testing"

func TestSimpleGet(t *testing.T) {
	c := New()

	c.IRequest("GET", "https://httpbin.org/get")
}
