# Contributing to VP Cloud SDK

Thank you for your interest in contributing to the VP Cloud SDK! This document provides important information about how the SDK is structured and how to report issues.

## Generated Source / API Models

There are several components of the SDK that we cannot accept direct changes to:

### Generated Source Files

All source files in the SDK are code-generated from the OpenAPI specification. You can tell when a file is code-generated because it will contain a header comment at the top indicating as such. Any manual edits to these files will be overwritten the next time the source is regenerated. As such, we cannot accept pull requests directly on generated source files.

**If you identify an issue within code-generated source, please:**
1. Create a GitHub issue describing the problem
2. Contact Voltage Park support at support@voltagepark.com

### OpenAPI Specification

The OpenAPI specification files (e.g., `openapi/v1/openapi.json`) are sourced from the official Voltage Park Cloud API and are automatically updated as part of SDK releases. As such, we cannot accept pull requests that modify these files directly.

**If you discover an issue with the API models or specification, please:**
1. Create a GitHub issue describing the problem
2. Contact Voltage Park support at support@voltagepark.com

## Reporting Issues

If you encounter any issues with the SDK, including:
- Bugs or errors in generated code
- Missing or incorrect API models
- Documentation issues
- Feature requests

Please create a GitHub issue with:
- A clear description of the problem
- Steps to reproduce (if applicable)
- Expected vs. actual behavior
- SDK version and Python version
- Any relevant error messages or logs

For urgent issues or questions, you can also contact Voltage Park support directly at support@voltagepark.com.

## Support

For API support, questions, or urgent issues, please contact:
- **Email**: support@voltagepark.com

Thank you for helping improve the VP Cloud SDK!

