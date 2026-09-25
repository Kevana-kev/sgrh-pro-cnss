Fingerprint Bridge

But: This is a minimal starter application that listens on http://localhost:5002 and exposes two endpoints:

- GET /status -> { status: 'ok' }
- POST /scan -> requires header `X-API-KEY: local-secret-key`, returns { template: '<base64>' }

Next steps:
- Integrate ZKTeco SDK inside `ScanFingerprintAsync` in `MainForm.cs`.
  - The project now attempts a reflection-based integration with `Interop.ZKFPEngXControl.dll` if present in the output directory.
  - For the most secure and reliable integration, use the SDK's .NET/ActiveX interop types directly. Replace the reflection code in `ScanFingerprintAsync()` with direct API calls.
- Replace the API key with a generated secret, and consider storing it securely.
- Ensure the app runs at startup if you want it always available.

Security & environment flags
----------------------------
- By default, mock templates and automatic approval/scans are disabled to avoid accidental enrollments.
- The following environment variables can be used for development only (set them explicitly when needed):
  - `FINGERPRINT_BRIDGE_AUTO=1` : enable auto-mode behaviors (pairing & scans without user dialogs)
  - `FINGERPRINT_BRIDGE_ALLOW_MOCK=1` : allow returning a mock template when in auto-mode
  - `FINGERPRINT_BRIDGE_ALLOW_AUTO_SCAN=1` : allow an initial automatic scan at startup when auto-mode is enabled
  - `FINGERPRINT_BRIDGE_ALLOW_AUTO_APPROVE=1` : allow pairing requests to be auto-approved in auto-mode

Configure-server changes
------------------------
- The `POST /configure-server` endpoint accepts optional `refreshToken` in addition to `accessToken` and `userId`.
- When saving a server URL, the bridge will reject non-HTTPS URLs in production (HTTPS is required for non-local addresses).

Token lifecycle
---------------
- The bridge now stores the refresh token (when provided) and will attempt to refresh the access token automatically when uploads receive a 401 response.

SDK binaries
------------
- The SDK installers/binaries should not be committed to the repository. Install the vendor SDK on the machine and copy the required interop assemblies into the application output folder as documented in the SDK.


How the webapp uses it (example):

fetch('http://localhost:5002/scan', { method: 'POST', headers: { 'X-API-KEY': 'local-secret-key' }}).then(r => r.json()).then(console.log);
