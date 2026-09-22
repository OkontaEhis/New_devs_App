# Property Revenue Dashboard Submission

## Repository

[GitHub repository](https://github.com/OkontaEhis/New_devs_App)

## Loom Video

Replace this with your Loom recording link before submission:

`<LOOM_VIDEO_URL>`

## Summary

I investigated and fixed the reported data accuracy and privacy issues in the property revenue dashboard.

- Scoped cached revenue summaries by tenant and property to prevent cross-tenant data exposure.
- Restored tenant-aware local authentication so dashboard API requests include the authenticated user's JWT.
- Replaced the hard-coded dashboard property list with a tenant-filtered backend query.
- Fixed the async database pool configuration so revenue data is read from PostgreSQL rather than mock fallback values.
- Preserved exact currency handling with `Decimal` rounding and property-local time-zone month boundaries.

## Verification

- Sunset Properties sees only its three properties. `prop-001` shows USD 2,250.00 across 4 reservations.
- Ocean Rentals sees only its three properties. `prop-004` shows USD 1,776.50 across 4 reservations.
- The same `prop-001` ID returns USD 2,250.00 for Sunset and USD 0.00 for Ocean.
- Backend regression suite: `python -m unittest tests.test_revenue_cache -v` (3 passing tests).
- Frontend production build: `npm run build` (passed).

## Files Changed

### Functional fixes

- `backend/app/services/cache.py`: tenant-scoped revenue cache keys.
- `backend/app/services/reservations.py`: decimal currency handling, property-local month boundaries, and database-backed revenue calculations.
- `backend/app/core/database_pool.py`: configured async PostgreSQL connection and session handling.
- `backend/app/api/v1/dashboard.py`: tenant-filtered property endpoint and protected dashboard data access.
- `frontend/src/contexts/AuthContext.new.tsx`: local authentication session and tenant retention.
- `frontend/src/lib/secureApi.ts`: local JWT retrieval and tenant-aware request/cache context.
- `frontend/src/components/Dashboard.tsx`: replaced the hard-coded shared property list with tenant-filtered properties.
- `frontend/src/components/RevenueSummary.tsx`: exact string-based currency display without floating-point conversion.

### Tests and supporting changes

- `backend/tests/test_revenue_cache.py`: revenue cache, rounding, and time-zone regression coverage.
- `docker-compose.yml`: PostgreSQL host port changed to `5434` because `5433` was already occupied locally.
- `.gitignore`: excludes generated dependencies, build output, local environment files, and Python caches.
- `SUBMISSION.md`: submission details and verification record.

## Commit Timeline

All timestamps use ISO 8601 format with the local `+01:00` offset.

| Timestamp | Commit | Description |
| --- | --- | --- |
| 2026-09-22T15:24:51+01:00 | `83b4951` | Fix tenant-isolated revenue dashboard |
| 2026-09-22T15:35:24+01:00 | `cdaafa5` | Add submission template |
| 2026-09-22T15:40:50+01:00 | `446de3d` | Document changed assignment files |
