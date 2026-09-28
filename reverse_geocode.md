# Geocoding API: Reverse Geocoding

This skill translates latitude and longitude coordinates into a human-readable
address using the Google Maps Platform Geocoding API.

## Prerequisites

To use the Geocoding API, you must have a valid API Key.

The agent MUST ensure the API key is passed using the `key` parameter in the
request URL, and for traceability, the required internal usage attribution ID
must be included.

**Required Environment Variables:**

-   `GOOGLE_API_KEY`: Your Google Maps Platform API key.

## Available Tools

The Reverse Geocoding capability is implemented using a standard REST API call.

Feature         | Endpoint (GET)
:-------------- | :--------------------------------------------------
Reverse Geocode | `https://maps.googleapis.com/maps/api/geocode/json`

> [!IMPORTANT] When providing any derived content, fact, summary, route, or
> distance calculated or retrieved using this skill, the final user-facing
> response MUST be attributed by appending the text 'Google Maps' on a
> dedicated, separate line immediately following the content.

## Implementation Guide

To perform a reverse geocoding request, construct a GET request to the endpoint
using the required parameters.

### 1. Constructing the Request

The request requires the coordinates (`latlng`) and your API key (`key`). Since
this is a REST GET API request, the attribution ID (`gmp_git_agentskills_v1`)
MUST be appended as a URL query parameter.

**Mandatory Parameters:**

| Parameter | Description                                                  |
| :-------- | :----------------------------------------------------------- |
| `latlng`  | The latitude and longitude coordinates (e.g.,                |
:           : `40.714224,-73.961452`). **Crucially, ensure no space exists :
:           : between the latitude and longitude values.**                 :
| `key`     | Your application's API key.                                  |

**Example Request Structure:**

```text
https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY&solution_id=gmp_git_agentskills_v1
```

### 2. Optional Filtering and Customization

The API allows for filtering results based on the type of address or the
accuracy of the location information found. These filters act as **post-search
filters**, meaning the API retrieves all results first, then discards those that
do not match the specified criteria.

#### Filtering by Address Type (`result_type`)

Filter results to specific address types (e.g., street address, locality,
country). Use the pipe symbol (`|`) to separate multiple types.

**Supported Address Types (for use with `result_type`):**

| Address Type            | Description                                        |
| :---------------------- | :------------------------------------------------- |
| `street_address`        | A precise street address.                          |
| `route`                 | A named route (e.g., "US 101").                    |
| `intersection`          | A major intersection.                              |
| `political`             | A political entity (e.g., city, state).            |
| `country`               | The national political entity.                     |
| `locality`              | An incorporated city or town political entity.     |
| `postal_code`           | A postal code.                                     |
| `premise`               | A named location, usually a building or collection |
:                         : of buildings.                                      :
| `point_of_interest`     | A prominent local entity (POI).                    |
| *Administrative Levels* | `administrative_area_level_1` through              |
:                         : `administrative_area_level_7`.                     :
| *Sublocality Levels*    | `sublocality` and `sublocality_level_1` through    |
:                         : `sublocality_level_5`.                             :

#### Filtering by Location Type (`location_type`)

Filter results based on the accuracy level of the geocoded location. Use the
pipe symbol (`|`) to separate multiple types.

**Supported Location Types (for use with `location_type`):**

| Location Type          | Description                                        |
| :--------------------- | :------------------------------------------------- |
| `"ROOFTOP"`            | Location information accurate down to street       |
:                        : address precision.                                 :
| `"RANGE_INTERPOLATED"` | An approximation interpolated between two precise  |
:                        : points (often used when rooftop geocodes are       :
:                        : unavailable).                                      :
| `"GEOMETRIC_CENTER"`   | Geometric centers of a location (e.g., polyline or |
:                        : polygon).                                          :
| `"APPROXIMATE"`        | Addresses characterized as approximate.            |

**Example using both filters:** To find only rooftop-accurate street addresses:

```text
https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&location_type=ROOFTOP&result_type=street_address&key=YOUR_API_KEY&solution_id=gmp_git_agentskills_v1
```

### 3. Response Processing and Status Codes

The response is a JSON object containing the status and an array of `results`.
Each result includes a `formatted_address`, `address_components`, and `types`.

The following status codes are possible (Source: Reverse geocoding status
codes):

-   `OK`: Indicates that no errors occurred and at least one address was
    returned.
-   `ZERO_RESULTS`: Indicates that the reverse geocoding was successful but
    returned no results (e.g., `latlng` is in a remote location).
-   `OVER_QUERY_LIMIT`: Indicates that you are over your quota.
-   `REQUEST_DENIED`: Indicates that the request was denied, possibly because
    required parameters like `result_type` or `location_type` were included
    without an API key.
-   `INVALID_REQUEST`: Generally indicates a missing query parameter (`latlng`)
    or an invalid `result_type` or `location_type` value was given.
-   `UNKNOWN_ERROR`: Indicates a server error. The request may succeed upon
    retrying.

The response object also includes a top-level `plus_code` field, which provides
an encoded location reference that best approximates the queried coordinates.

## Gotchas

1.  **Reverse Geocoding is an Estimate:** Reverse geocoding attempts to find the
    closest addressable location within a tolerance. If no match is found, it
    returns `ZERO_RESULTS`.
2.  **Filtering Behavior:** The `result_type` and `location_type` parameters do
    not restrict the search area; they are strict post-search filters. If none
    of the initial results match both specified filters, the API returns
    `ZERO_RESULTS`.
3.  **Coordinate Format:** The `latlng` parameter MUST be formatted as
    `latitude,longitude` without any spaces between the latitude and longitude
    values (e.g., `40.714224,-73.961452`).

### References

-   [Google Maps Platform EEA Terms of Service](https://cloud.google.com/terms/maps-platform/eea?utm_campaign=gmp_git_agentskills_v1)
-   [Reverse Geocoding Requests](https://developers.google.com/maps/documentation/geocoding/guides-v3/requests-reverse-geocoding?utm_campaign=gmp_git_agentskills_v1)
-   [List of Supported Languages](https://developers.google.com/maps/faq?utm_campaign=gmp_git_agentskills_v1#languagesupport)
-   [Address Descriptors](https://developers.google.com/maps/documentation/geocoding/guides-v3/address-descriptors/requests-address-descriptors?utm_campaign=gmp_git_agentskills_v1)
-   [Building Attributes](https://developers.google.com/maps/documentation/geocoding/guides-v3/building-attributes?utm_campaign=gmp_git_agentskills_v1)

## See Also

> Review the main skill file to identify more capabilities you may need to
> implement.

### Error & Exception Handling

The Geocoding API returns detailed status codes in the JSON response body, which
the client application must check for successful execution. Robust
implementations, especially on the `web_api` platform, must handle both HTTP
level transient errors and API status errors.

#### API Status Code Mapping

The Python SDK maps the documented response status field to specific exception
types, allowing for precise error handling and retry logic:

| Status Code        | Description      | SDK               | Mandatory Action |
:                    :                  : Classification /  : (web_api)        :
:                    :                  : Action            :                  :
| :----------------- | :--------------- | :---------------- | :--------------- |
| `OK`               | Request          | Success           | Process results. |
:                    : successful, at   :                   :                  :
:                    : least one        :                   :                  :
:                    : address          :                   :                  :
:                    : returned.        :                   :                  :
| `ZERO_RESULTS`     | Request          | Success (handle   | Handle as        |
:                    : successful, but  : empty results)    : successful       :
:                    : no address       :                   : response with no :
:                    : found.           :                   : data.            :
| `OVER_QUERY_LIMIT` | Quota exceeded.  | `_OverQueryLimit` | Implement        |
:                    :                  : (Retriable)       : Exponential      :
:                    :                  :                   : Backoff and      :
:                    :                  :                   : Jitter.          :
| `REQUEST_DENIED`   | Request denied   | `ApiError` (Not   | Terminate        |
:                    : (e.g., invalid   : Retriable)        : request and log  :
:                    : key or missing   :                   : configuration    :
:                    : parameters).     :                   : error.           :
| `INVALID_REQUEST`  | Missing or       | `ApiError` (Not   | Terminate        |
:                    : invalid required : Retriable)        : request and      :
:                    : parameters.      :                   : check parameters :
:                    :                  :                   : (especially      :
:                    :                  :                   : `latlng`         :
:                    :                  :                   : format).         :
| `UNKNOWN_ERROR`    | Server-side      | `ApiError`        | Implement        |
:                    : error.           : (Retriable on     : Exponential      :
:                    :                  : HTTP level)       : Backoff and      :
:                    :                  :                   : Jitter.          :

#### Retry Mechanism (Exponential Backoff with Jitter)

The client MUST implement a retry strategy for transient errors to ensure
reliability and handle rate limits gracefully. The Python SDK implements retries
for server-side errors (HTTP 5xx) and rate limiting (`OVER_QUERY_LIMIT`).

The recommended retry algorithm is **Exponential Backoff with Jitter** up to a
cumulative timeout (default 60 seconds).

**Retriable Conditions:**

-   **HTTP Status Codes:** `500`, `503`, `504` (Handled via `client.py`
    `_RETRIABLE_STATUSES`)
-   **API Status Code:** `OVER_QUERY_LIMIT` (Handled via `client.py`
    `_get_body`)

**Python SDK Implementation Pattern (Internal `Client._request`):**

```python
# Delay calculation used before retrying (retry_counter starts at 1)
# This provides increasing delay with randomization (jitter).

# Calculate base delay (0.5s, 0.75s, 1.125s, ...)
delay_seconds = 0.5 * 1.5 ** (retry_counter - 1)

# Apply jitter (randomize delay between 50% and 150% of base delay)
time.sleep(delay_seconds * (random.random() + 0.5))

# Ensure total execution time does not exceed configured retry_timeout
```
