# doc-summarizer

## Version: 0.1.0

### Paths

#### /api/v1/chat/{session_id}

**POST**

**Summary:** Chat

**Operation ID:** chat_api_v1_chat__session_id__post

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | path | True | `type: N/A`<br>`title: Session Id` | N/A | N/A |
**Request Body:**
- **Required:** True
- **Content:**
  - **application/json:**
    - **Schema:** [ChatRequestBody](#chatrequestbody)

**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [ChatResponse](#chatresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/chat/sse/{session_id}

**POST**

**Summary:** Chat Stream

**Operation ID:** chat_stream_api_v1_chat_sse__session_id__post

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | path | True | `type: N/A`<br>`title: Session Id` | N/A | N/A |
**Request Body:**
- **Required:** True
- **Content:**
  - **application/json:**
    - **Schema:** [ChatRequestBody](#chatrequestbody)

**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [A](#a)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/chat/history/{session_id}

**GET**

**Summary:** Chat History

**Operation ID:** chat_history_api_v1_chat_history__session_id__get

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | path | True | `type: N/A`<br>`title: Session Id` | N/A | N/A |
**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [ChatHistoryResponse](#chathistoryresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/file/upload

**POST**

**Summary:** File Upload

**Operation ID:** file_upload_api_v1_file_upload_post

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | query | False | `type: N/A`<br>`title: Session Id` | N/A | N/A |
**Request Body:**
- **Required:** True
- **Content:**
  - **multipart/form-data:**
    - **Schema:** [Body_file_upload_api_v1_file_upload_post](#body_file_upload_api_v1_file_upload_post)

**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [FileUploadResponse](#fileuploadresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/file/list

**GET**

**Summary:** List Files

**Operation ID:** list_files_api_v1_file_list_get

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | query | True | `type: N/A`<br>`title: Session Id` | N/A | N/A |
**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [GetFilesResponse](#getfilesresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/file/{file_id}

**DELETE**

**Summary:** Delete File

**Operation ID:** delete_file_api_v1_file__file_id__delete

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| file_id | path | True | `type: string`<br>`title: File Id` | N/A | N/A |
**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [DeleteByIDResponse](#deletebyidresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/session/create

**POST**

**Summary:** Create Session

**Operation ID:** create_session_api_v1_session_create_post

**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [CreateSessionResponse](#createsessionresponse)` |
#### /api/v1/session/list

**GET**

**Summary:** List Sessions

**Operation ID:** list_sessions_api_v1_session_list_get

**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [GetSessionsResponse](#getsessionsresponse)` |
#### /api/v1/session/{session_id}

**GET**

**Summary:** Get Session By Id

**Operation ID:** get_session_by_id_api_v1_session__session_id__get

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | path | True | `type: string`<br>`title: Session Id` | N/A | N/A |
**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [GetSessionByIDResponse](#getsessionbyidresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
#### /api/v1/session/{session_id}

**DELETE**

**Summary:** Delete Session

**Operation ID:** delete_session_api_v1_session__session_id__delete

**Parameters:**

| Name | In | Required | Schema | Description | Example |
|------|----|----------|--------|-------------|---------|
| session_id | path | True | `type: N/A`<br>`title: Session Id` | N/A | N/A |
**Responses:**

| Status Code | Description | Content |
|-------------|-------------|---------|
| 200 | Successful Response | application/json: `schema: [DeleteByIDResponse](#deletebyidresponse)` |
| 422 | Validation Error | application/json: `schema: [HTTPValidationError](#httpvalidationerror)` |
### Components
#### Schemas
##### Body_file_upload_api_v1_file_upload_post
- **Type:** object
- **Required:** files
- **Title:** Body_file_upload_api_v1_file_upload_post
- **Properties:**
  - **files:**
    - **Type:** array
    - **Title:** Files
    - **Description:** N/A
##### ChatFileReference
- **Type:** object
- **Required:** id, file_name
- **Title:** ChatFileReference
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **file_name:**
    - **Type:** string
    - **Title:** File Name
    - **Description:** N/A
##### ChatHistoryItem
- **Type:** object
- **Required:** id, created, session_id, role, message, references
- **Title:** ChatHistoryItem
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **created:**
    - **Type:** string
    - **Title:** Created
    - **Description:** N/A
  - **session_id:**
    - **Type:** string
    - **Title:** Session Id
    - **Description:** N/A
  - **role:**
    - **Type:** string
    - **Title:** Role
    - **Description:** N/A
  - **message:**
    - **Type:** string
    - **Title:** Message
    - **Description:** N/A
  - **references:**
    - **Type:** N/A
    - **Title:** References
    - **Description:** N/A
##### ChatHistoryResponse
- **Type:** object
- **Required:** data
- **Title:** ChatHistoryResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** array
    - **Title:** Data
    - **Description:** N/A
##### ChatRequestBody
- **Type:** object
- **Required:** query
- **Title:** ChatRequestBody
- **Properties:**
  - **query:**
    - **Type:** string
    - **Title:** Query
    - **Description:** N/A
##### ChatResponse
- **Type:** object
- **Required:** data
- **Title:** ChatResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
##### CompletionResponseWithReferences
- **Type:** object
- **Required:** content
- **Title:** CompletionResponseWithReferences
- **Properties:**
  - **content:**
    - **Type:** string
    - **Title:** Content
    - **Description:** N/A
  - **usage_metadata:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
  - **references:**
    - **Type:** N/A
    - **Title:** References
    - **Description:** N/A
##### CreateSessionResponse
- **Type:** object
- **Required:** data
- **Title:** CreateSessionResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
##### DeleteByID
- **Type:** object
- **Required:** id, message
- **Title:** DeleteByID
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **message:**
    - **Type:** string
    - **Title:** Message
    - **Description:** N/A
##### DeleteByIDResponse
- **Type:** object
- **Required:** data
- **Title:** DeleteByIDResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
##### ExtractedFile
- **Type:** object
- **Required:** id, file_name, file_type
- **Title:** ExtractedFile
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **file_name:**
    - **Type:** string
    - **Title:** File Name
    - **Description:** N/A
  - **file_type:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
  - **file_size:**
    - **Type:** N/A
    - **Title:** File Size
    - **Description:** N/A
##### ExtractedFileResponse
- **Type:** object
- **Required:** id, file_name, file_type, created
- **Title:** ExtractedFileResponse
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **file_name:**
    - **Type:** string
    - **Title:** File Name
    - **Description:** N/A
  - **file_type:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
  - **file_size:**
    - **Type:** N/A
    - **Title:** File Size
    - **Description:** N/A
  - **created:**
    - **Type:** string
    - **Title:** Created
    - **Description:** N/A
##### FileExtractionResponse
- **Type:** object
- **Required:** session_id, files
- **Title:** FileExtractionResponse
- **Properties:**
  - **session_id:**
    - **Type:** string
    - **Title:** Session Id
    - **Description:** N/A
  - **files:**
    - **Type:** array
    - **Title:** Files
    - **Description:** N/A
##### FileType
- **Type:** string
- **Title:** FileType
- **Properties:**
##### FileUploadResponse
- **Type:** object
- **Required:** data
- **Title:** FileUploadResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
##### GetFileResponse
- **Type:** object
- **Required:** id, file_name, file_type, created, session_id
- **Title:** GetFileResponse
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **file_name:**
    - **Type:** string
    - **Title:** File Name
    - **Description:** N/A
  - **file_type:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
  - **file_size:**
    - **Type:** N/A
    - **Title:** File Size
    - **Description:** N/A
  - **created:**
    - **Type:** string
    - **Title:** Created
    - **Description:** N/A
  - **session_id:**
    - **Type:** string
    - **Title:** Session Id
    - **Description:** N/A
##### GetFilesResponse
- **Type:** object
- **Required:** data
- **Title:** GetFilesResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** array
    - **Title:** Data
    - **Description:** N/A
##### GetSessionByID
- **Type:** object
- **Required:** id, session_name, created, files
- **Title:** GetSessionByID
- **Properties:**
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
  - **session_name:**
    - **Type:** string
    - **Title:** Session Name
    - **Description:** N/A
  - **created:**
    - **Type:** string
    - **Title:** Created
    - **Description:** N/A
  - **files:**
    - **Type:** array
    - **Title:** Files
    - **Description:** N/A
##### GetSessionByIDResponse
- **Type:** object
- **Required:** data
- **Title:** GetSessionByIDResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** N/A
    - **Title:** N/A
    - **Description:** N/A
##### GetSessionsResponse
- **Type:** object
- **Required:** data
- **Title:** GetSessionsResponse
- **Properties:**
  - **success:**
    - **Type:** boolean
    - **Title:** Success
    - **Description:** N/A
  - **data:**
    - **Type:** array
    - **Title:** Data
    - **Description:** N/A
##### HTTPValidationError
- **Type:** object
- **Title:** HTTPValidationError
- **Properties:**
  - **detail:**
    - **Type:** array
    - **Title:** Detail
    - **Description:** N/A
##### Reference
- **Type:** object
- **Required:** file_name, file_id
- **Title:** Reference
- **Properties:**
  - **file_name:**
    - **Type:** string
    - **Title:** File Name
    - **Description:** N/A
  - **file_id:**
    - **Type:** string
    - **Title:** File Id
    - **Description:** N/A
##### Session
- **Type:** object
- **Title:** Session
- **Properties:**
  - **created:**
    - **Type:** string
    - **Format:** date-time
    - **Title:** Created
    - **Description:** N/A
  - **session_name:**
    - **Type:** string
    - **Title:** Session Name
    - **Description:** N/A
  - **files:**
    - **Type:** array
    - **Title:** Files
    - **Description:** N/A
  - **id:**
    - **Type:** string
    - **Title:** Id
    - **Description:** N/A
##### UsageMetadata
- **Type:** object
- **Required:** input_tokens, output_tokens, total_tokens
- **Title:** UsageMetadata
- **Properties:**
  - **input_tokens:**
    - **Type:** integer
    - **Title:** Input Tokens
    - **Description:** N/A
  - **output_tokens:**
    - **Type:** integer
    - **Title:** Output Tokens
    - **Description:** N/A
  - **total_tokens:**
    - **Type:** integer
    - **Title:** Total Tokens
    - **Description:** N/A
##### ValidationError
- **Type:** object
- **Required:** loc, msg, type
- **Title:** ValidationError
- **Properties:**
  - **loc:**
    - **Type:** array
    - **Title:** Location
    - **Description:** N/A
  - **msg:**
    - **Type:** string
    - **Title:** Message
    - **Description:** N/A
  - **type:**
    - **Type:** string
    - **Title:** Error Type
    - **Description:** N/A