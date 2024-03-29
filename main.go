package main

import "log"

func main() {
	headers := AuthHeaders(map[string]string{"test": "test"})

	for k, v := range *headers {
		log.Printf("%s -> %s", k, v)
	}
}
