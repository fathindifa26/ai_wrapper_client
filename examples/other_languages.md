# AI Wrapper API - Usage Examples (Multiple Languages)

Examples untuk akses AI Wrapper API dari berbagai bahasa pemrograman.

## Setup
Ganti `http://your-vm:8000` dengan URL VM Anda.

---

## cURL (Command Line)

### Basic Request
```bash
curl -X POST http://your-vm:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is artificial intelligence?"
  }'
```

### With Project URL
```bash
curl -X POST http://your-vm:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is AI?",
    "project_url": "https://imagine.wpp.ai/chat/PROJECT_ID/foundational"
  }'
```

### Check Status
```bash
curl http://your-vm:8000/status
```

### List Projects
```bash
curl http://your-vm:8000/projects
```

---

## JavaScript / Node.js

### Using fetch (Node.js 18+)
```javascript
// basic_client.js
const API_URL = 'http://your-vm:8000';

async function chat(prompt, projectUrl = null) {
  const payload = { prompt };
  if (projectUrl) {
    payload.project_url = projectUrl;
  }

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (data.status === 'success') {
      console.log(`[${data.project_id}] ${data.response}`);
      return data.response;
    } else {
      console.error(`Error: ${data.error}`);
      return null;
    }
  } catch (error) {
    console.error(`Request failed: ${error.message}`);
    return null;
  }
}

// Usage
chat('What is Python?').then(response => {
  if (response) {
    console.log('Success!');
  }
});
```

### Using axios
```javascript
// with_axios.js
const axios = require('axios');

const API_URL = 'http://your-vm:8000';

async function chat(prompt, projectUrl = null) {
  try {
    const response = await axios.post(`${API_URL}/chat`, {
      prompt: prompt,
      project_url: projectUrl
    }, {
      timeout: 180000  // 3 minutes
    });

    if (response.data.status === 'success') {
      return response.data.response;
    } else {
      throw new Error(response.data.error);
    }
  } catch (error) {
    console.error(`Chat failed: ${error.message}`);
    throw error;
  }
}

// Usage
async function main() {
  const answer = await chat('Explain machine learning briefly');
  console.log(answer);
}

main();
```

---

## Python (without client library)

### Using requests
```python
import requests

API_URL = "http://your-vm:8000"

def chat(prompt, project_url=None):
    """Send chat request."""
    payload = {"prompt": prompt}
    if project_url:
        payload["project_url"] = project_url

    try:
        response = requests.post(
            f"{API_URL}/chat",
            json=payload,
            timeout=180
        )
        response.raise_for_status()
        data = response.json()

        if data["status"] == "success":
            return data["response"]
        else:
            raise Exception(data.get("error", "Unknown error"))

    except requests.exceptions.Timeout:
        raise Exception("Request timeout")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")


# Usage
if __name__ == "__main__":
    answer = chat("What is artificial intelligence?")
    print(answer)
```

---

## Java

### Using HttpClient (Java 11+)
```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class AIWrapperClient {
    private static final String API_URL = "http://your-vm:8000";
    private static final HttpClient client = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(180))
            .build();

    public static String chat(String prompt, String projectUrl) throws Exception {
        JsonObject payload = new JsonObject();
        payload.addProperty("prompt", prompt);
        if (projectUrl != null) {
            payload.addProperty("project_url", projectUrl);
        }

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL + "/chat"))
                .header("Content-Type", "application/json")
                .timeout(Duration.ofSeconds(180))
                .POST(HttpRequest.BodyPublishers.ofString(payload.toString()))
                .build();

        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());

        JsonObject data = JsonParser.parseString(response.body()).getAsJsonObject();

        if (data.get("status").getAsString().equals("success")) {
            return data.get("response").getAsString();
        } else {
            throw new Exception(data.get("error").getAsString());
        }
    }

    public static void main(String[] args) {
        try {
            String answer = chat("What is AI?", null);
            System.out.println("Response: " + answer);
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

---

## PHP

### Using cURL
```php
<?php
// ai_client.php

define('API_URL', 'http://your-vm:8000');

function chat($prompt, $projectUrl = null) {
    $payload = ['prompt' => $prompt];
    if ($projectUrl !== null) {
        $payload['project_url'] = $projectUrl;
    }

    $ch = curl_init(API_URL . '/chat');
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 180);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json'
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if (curl_errno($ch)) {
        throw new Exception('Request failed: ' . curl_error($ch));
    }

    curl_close($ch);

    $data = json_decode($response, true);

    if ($httpCode === 200 && $data['status'] === 'success') {
        return $data['response'];
    } else {
        throw new Exception($data['error'] ?? 'Unknown error');
    }
}

// Usage
try {
    $answer = chat('What is artificial intelligence?');
    echo "Response: " . $answer . "\n";
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>
```

---

## Go

### Using net/http
```go
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

const APIURL = "http://your-vm:8000"

type ChatRequest struct {
	Prompt     string  `json:"prompt"`
	ProjectURL *string `json:"project_url,omitempty"`
}

type ChatResponse struct {
	Status    string  `json:"status"`
	ProjectID *string `json:"project_id,omitempty"`
	Response  *string `json:"response,omitempty"`
	Error     *string `json:"error,omitempty"`
}

func chat(prompt string, projectURL *string) (string, error) {
	client := &http.Client{
		Timeout: 180 * time.Second,
	}

	reqBody := ChatRequest{
		Prompt:     prompt,
		ProjectURL: projectURL,
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return "", err
	}

	resp, err := client.Post(
		APIURL+"/chat",
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	var chatResp ChatResponse
	if err := json.Unmarshal(body, &chatResp); err != nil {
		return "", err
	}

	if chatResp.Status == "success" && chatResp.Response != nil {
		return *chatResp.Response, nil
	} else if chatResp.Error != nil {
		return "", fmt.Errorf(*chatResp.Error)
	}

	return "", fmt.Errorf("unknown error")
}

func main() {
	answer, err := chat("What is AI?", nil)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Printf("Response: %s\n", answer)
}
```

---

## Best Practices

### 1. Error Handling
```python
try:
    response = client.chat(prompt)
    if response.success:
        process(response.response)
    else:
        log_error(response.error)
        fallback()
except Timeout:
    retry_or_fallback()
```

### 2. Timeout Configuration
- Default: 180s (3 minutes)
- Adjust based on prompt complexity
- Always handle timeout gracefully

### 3. Connection Pooling
```python
# Reuse client instance
client = AIClient(API_URL)  # Initialize once

# Use multiple times
for prompt in prompts:
    response = client.chat(prompt)
```

### 4. Monitoring
```python
# Periodic health check
status = client.get_status()
if status['api_status'] != 'running':
    alert_admin()
```

---

## Next Steps

1. **Python**: Use `client_library.py` (recommended)
2. **Other Languages**: Copy & adapt examples above
3. **Production**: Add retry logic, rate limiting, monitoring
4. **Security**: Use HTTPS, API keys if needed
