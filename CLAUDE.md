# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Activate virtual environment (required before running anything)
source venv/bin/activate

# Install dependencies
pip install -r requirements-app.txt

# Run all tests
pytest

# Run a single test file
pytest tests/modules/create_booking/app/test_create_booking_usecase.py

# Run a single test by name
pytest tests/modules/create_booking/app/test_create_booking_usecase.py::TestCreateBookingUsecase::test_create_booking_valid

# Run tests with coverage
pytest --cov=src
```

Set `STAGE=TEST` in your `.env` file (or environment) for local development — this switches to mock repositories and local DynamoDB config automatically.

## Architecture

This is a **Clean Architecture** Python microservice deployed as AWS Lambda functions behind API Gateway, with DynamoDB as the database. Each Lambda function is a module under `src/modules/`.

### Layer flow (outer → inner)

```
Lambda event → Presenter → Controller → Usecase → Repository Interface
                                                        ↑
                                          Mock (TEST) or DynamoDB (DEV/PROD)
```

- **Presenter** (`*_presenter.py`): Lambda entry point. Instantiates repo/usecase/controller from `Environments`, wraps the raw Lambda event into `LambdaHttpRequest`, injects `user_from_authorizer` from the API Gateway authorizer context, and returns `LambdaHttpResponse.toDict()`.
- **Controller** (`*_controller.py`): Validates and extracts parameters from the request, calls the usecase, wraps the result in a Viewmodel, and returns an HTTP code object (`Created`, `BadRequest`, etc.).
- **Usecase** (`*_usecase.py`): Business logic. Receives primitive types, raises domain/usecase errors.
- **Viewmodel** (`*_viewmodel.py`): Serializes domain entities to response dicts.
- **Repository interface** (`src/shared/domain/repositories/`): Abstract base classes (`IBookingRepository`, `IReservationRepository`) that define the data contract.
- **Repository implementations** (`src/shared/infra/repositories/`): `*_mock.py` for tests, `*_dynamo.py` for production.

### Environment / repo selection

`Environments.get_envs()` (in `src/shared/environments.py`) reads the `STAGE` env var and returns the correct repository class. When `STAGE=TEST`, mocks are used; otherwise DynamoDB implementations are used. All presenters call this at module load time.

### Authentication

A Lambda Authorizer (`src/shared/authorizer/user_mss_authorizer.py`) validates Bearer tokens against an external User MSS API and injects user data into the API Gateway request context. Controllers receive it via `request.data['user_from_authorizer']` (a dict with `user_id`, role, etc.).

### Key shared paths

| Path | Purpose |
|------|---------|
| `src/shared/domain/entities/` | `Booking` and `Court` domain entities with validation |
| `src/shared/domain/enums/` | `SPORT`, `BOOKING_TYPE`, `STATUS_ENUM` enums |
| `src/shared/helpers/errors/` | `domain_errors`, `usecase_errors`, `controller_errors` — raised by different layers |
| `src/shared/helpers/external_interfaces/` | `LambdaHttpRequest/Response`, HTTP status code wrappers |
| `src/shared/infra/dto/` | DynamoDB ↔ domain entity conversion (`*_dynamo_dto.py`) |
| `src/shared/clients/` | External HTTP clients (e.g., `user_api_client.py`) |
| `iac/` | AWS CDK infrastructure (API Gateway, Lambda, DynamoDB, S3, SSM constructs) |

### Naming conventions

- Files and directories: `snake_case`
- Classes: `PascalCase` with type suffix — `CreateBookingController`, `BookingRepositoryMock`, `IBookingRepository`
- Enums: `UPPER_SNAKE_CASE` with `_ENUM` suffix where applicable
- Tests mirror the `src/` directory structure under `tests/`

### Infrastructure

Defined in `iac/` using AWS CDK (Python). The stack provisions API Gateway, Lambda functions, DynamoDB table, S3 bucket, and SSM parameters. The `STAGE` variable controls deployment target (`DEV`, `HOMOLOG`, `PROD`). Local development uses Docker Compose with DynamoDB Local and MinIO (see `iac/local/`).
