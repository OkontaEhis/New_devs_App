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
